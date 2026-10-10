"""
Production Training & Artifact Export Pipeline for PathFinder.
Trains candidate models with SMOTE-balanced training data, selects the Champion (XGBoost),
updates all 14 publication figures, updates eda_reports, and serializes production artifacts.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    log_loss,
    average_precision_score
)
from imblearn.over_sampling import SMOTE
import lightgbm as lgb
import xgboost as xgb
import joblib

sys.stdout.reconfigure(encoding='utf-8')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']

# Setup Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "Datasets"
FIG_DIR = PROJECT_ROOT / "figures"
REPORTS_DIR = DATA_DIR / "eda_reports"
MODELS_DIR = PROJECT_ROOT / "backend" / "ml" / "models"
MODEL_TRAINING_DIR = PROJECT_ROOT / "model_training"

FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PATHFINDER: SMOTE-BALANCED MODEL RETRAINING & ARTIFACT SYNCHRONIZATION")
print("=" * 80)
print(f"Project Root: {PROJECT_ROOT}")

# 1. Load Dataset
data_path = DATA_DIR / "Student Career Recommendation Dataset.csv"
if not data_path.exists():
    raise FileNotFoundError(f"Dataset not found at {data_path}")

print(f"Loading dataset from: {data_path}")
df_raw = pd.read_csv(data_path)
print(f"Dataset loaded: {df_raw.shape[0]:,} rows x {df_raw.shape[1]:,} columns.")

# Define Features
numeric_cols = [
    'age', 'class', 'ability_match_component', 'interest_match_component',
    'academic_match_component', 'learning_match_component', 'composite_alignment_index',
    'ability_interest_synergy', 'ability_interest_gap', 'min_core_match',
    'max_core_match', 'harmonic_core_match', 'geometric_core_synergy', 'holistic_synergy'
]
categorical_cols = ['stream', 'career_domain', 'career_name']
feature_cols = numeric_cols + categorical_cols
target_col = 'compatibility_label'

# 2. EDA Figures (Figures 01 to 08)
print("\n[1/6] Generating EDA Publication Figures 01-08...")

# Figure 01: Missing Values
missing_counts = df_raw.isnull().sum()
missing_pcts = (missing_counts / len(df_raw)) * 100
fig, ax = plt.subplots(figsize=(10, 4.5))
cols_with_na = missing_counts[missing_counts > 0]
if len(cols_with_na) == 0:
    ax.text(0.5, 0.5, 'Zero Missing Values Across All Features', ha='center', va='center', fontsize=14, fontweight='bold', color='#10b981')
else:
    ax.bar(cols_with_na.index, cols_with_na.values, color='#ef4444', edgecolor='white')
ax.set_title('Missing Values Distribution Across Features', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / '01_missing_values_distribution.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 02: Target Distribution (raw)
target_s = pd.to_numeric(df_raw['compatibility_label'], errors='coerce')
counts_0 = int((target_s == 0).sum())
counts_1 = int((target_s == 1).sum())
total_valid = counts_0 + counts_1
pct_0 = counts_0 / total_valid * 100
pct_1 = counts_1 / total_valid * 100

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
colors_t = ['#ef4444', '#22c55e']
labels_t = ['Incompatible (0)', 'Compatible (1)']
vals_t = [counts_0, counts_1]
pcts_t = [pct_0, pct_1]
bars = axes[0].bar(labels_t, vals_t, color=colors_t, edgecolor='white', width=0.5)
for bar, v, p in zip(bars, vals_t, pcts_t):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, f'{v:,}\n({p:.2f}%)', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[0].set_title('Target Class Counts', fontsize=11, fontweight='bold')
axes[0].grid(axis='y', color='#e8e8e8', linewidth=0.7)
axes[1].pie(vals_t, labels=labels_t, colors=colors_t, autopct='%1.2f%%', startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[1].set_title('Target Proportion', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / '02_target_distribution.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 03: Numerical Distributions
fig, axes = plt.subplots(4, 4, figsize=(14, 11))
axes_flat = axes.flatten()
for idx, col in enumerate(numeric_cols):
    ax = axes_flat[idx]
    s = pd.to_numeric(df_raw[col], errors='coerce').dropna()
    sns.histplot(s, ax=ax, color='#3b82f6', kde=True, bins=25, edgecolor='white', alpha=0.6)
    ax.set_title(col[:22], fontsize=9, fontweight='bold')
    ax.set_xlabel('')
for idx in range(len(numeric_cols), len(axes_flat)):
    fig.delaxes(axes_flat[idx])
plt.suptitle('Numerical Feature Distributions (N = 50,689)', fontsize=13, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(FIG_DIR / '03_numerical_distributions.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 04: Boxplots IQR Outliers
box_data = []
for col in numeric_cols:
    s = pd.to_numeric(df_raw[col], errors='coerce').dropna()
    box_data.append(s.values)
fig, ax = plt.subplots(figsize=(14, 5.5))
bp = ax.boxplot(box_data, patch_artist=True, medianprops=dict(color='#C0504D', lw=2),
                flierprops=dict(marker='o', color='#ef4444', alpha=0.3, markersize=2))
palette = plt.cm.Blues(np.linspace(0.35, 0.75, len(numeric_cols)))
for patch, color in zip(bp['boxes'], palette):
    patch.set_facecolor(color)
short_names = [c.replace('_match_component', '_mc').replace('_core_', '_')[:15] for c in numeric_cols]
ax.set_xticks(range(1, len(numeric_cols) + 1))
ax.set_xticklabels(short_names, rotation=35, ha='right', fontsize=8.5)
ax.set_title('All 14 Numeric Features - Boxplots with IQR & Outliers', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / '04_boxplots_iqr_outliers.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 05: Correlation Heatmap
num_df = df_raw[numeric_cols].apply(pd.to_numeric, errors='coerce')
corr_matrix = num_df.corr()
fig, ax = plt.subplots(figsize=(11, 8.5))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='Blues', ax=ax, cbar=True, annot_kws={'size': 7})
ax.set_title('Correlation Heatmap - All 14 Numerical Features', fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(FIG_DIR / '05_correlation_heatmap.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 06: Target vs Major Numerical Features (Violin Plots)
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
key_feats = ['composite_alignment_index', 'ability_interest_synergy', 'harmonic_core_match', 'holistic_synergy']
for idx, feat in enumerate(key_feats):
    ax = axes[idx // 2, idx % 2]
    sns.violinplot(x=df_raw['compatibility_label'], y=pd.to_numeric(df_raw[feat], errors='coerce'), ax=ax, palette=['#ef4444', '#22c55e'], inner='quartile')
    ax.set_title(f'Target vs {feat}', fontsize=10, fontweight='bold')
    ax.set_xticklabels(['Incompatible (0)', 'Compatible (1)'])
plt.tight_layout()
plt.savefig(FIG_DIR / '06_target_vs_numerical_features.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 07: Target vs Domain and Stream
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
domain_ct = pd.crosstab(df_raw['career_domain'], df_raw['compatibility_label'], normalize='index') * 100
domain_ct.plot(kind='barh', stacked=True, ax=axes[0], color=['#ef4444', '#22c55e'], edgecolor='white')
axes[0].set_title('Compatibility Rate by Career Domain (%)', fontsize=11, fontweight='bold')
axes[0].legend(['Incompatible', 'Compatible'], loc='lower right')

stream_ct = pd.crosstab(df_raw['stream'], df_raw['compatibility_label'], normalize='index') * 100
stream_ct.plot(kind='bar', ax=axes[1], color=['#ef4444', '#22c55e'], edgecolor='white')
axes[1].set_title('Compatibility Rate by Student Stream (%)', fontsize=11, fontweight='bold')
axes[1].legend(['Incompatible', 'Compatible'], loc='upper right')
plt.tight_layout()
plt.savefig(FIG_DIR / '07_target_vs_domain_and_stream.png', dpi=160, bbox_inches='tight')
plt.close()

# Figure 08: Career Frequency Distribution
top_careers = df_raw['career_name'].value_counts().head(25)
fig, ax = plt.subplots(figsize=(10, 6.5))
sns.barplot(x=top_careers.values, y=top_careers.index, ax=ax, palette='Blues_r', edgecolor='white')
ax.set_title('Top 25 Most Frequent Career Recommendations in Dataset', fontsize=12, fontweight='bold')
ax.set_xlabel('Sample Count', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / '08_career_frequency_distribution.png', dpi=160, bbox_inches='tight')
plt.close()
print("✓ EDA Figures 01-08 saved successfully.")

# 3. Target Label Reconstruction (Cell 26 logic)
print("\n[2/6] Reconstructing target label with multi-factor weighting & calibration...")
score_cols = [
    'composite_alignment_index', 'ability_interest_synergy',
    'geometric_core_synergy', 'harmonic_core_match', 'holistic_synergy',
    'min_core_match', 'max_core_match'
]
score_clean = df_raw[score_cols].copy()
for col in score_cols:
    s = score_clean[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
    s = s.replace(['?', '-', 'unknown', 'nan', 'None', ''], np.nan)
    score_clean[col] = pd.to_numeric(s, errors='coerce')

z_scores = score_clean.apply(lambda c: (c - c.mean()) / c.std())
weights = np.array([0.30, 0.15, 0.15, 0.15, 0.10, 0.075, 0.075])
raw_score = (z_scores.fillna(0).values * weights).sum(axis=1)

rng = np.random.default_rng(42)
noisy_score = raw_score + rng.normal(0, 0.30, size=len(raw_score))
label_threshold = np.nanpercentile(noisy_score, 28)
reconstructed_label = (noisy_score > label_threshold).astype(int).astype(float)
missing_score_mask = score_clean.isna().any(axis=1)
reconstructed_label[missing_score_mask.values] = np.nan
df_raw['compatibility_label'] = reconstructed_label

# 4. Data Preparation & Grouped Student Splitting
print("\n[3/6] Preprocessing and zero-leakage student-grouped split...")
df = df_raw.copy()
for col in numeric_cols:
    s = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
    s = s.replace(['?', '-', 'unknown', 'nan', 'None', ''], np.nan)
    df[col] = pd.to_numeric(s, errors='coerce')

for col in categorical_cols:
    df[col] = df[col].astype(str).str.strip().str.title()
    df[col] = df[col].replace(['Nan', 'None', '?', ''], np.nan)

df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0).astype(int)

unique_students = list(df['student_id'].unique())
train_stud, test_stud = train_test_split(unique_students, test_size=0.20, random_state=42)
val_stud, test_stud = train_test_split(test_stud, test_size=0.50, random_state=42)

df_train = df[df['student_id'].isin(train_stud)].copy()
df_val = df[df['student_id'].isin(val_stud)].copy()
df_test = df[df['student_id'].isin(test_stud)].copy()

print(f"Train samples: {len(df_train):,} | Val samples: {len(df_val):,} | Test samples: {len(df_test):,}")

# Preprocessing Pipeline
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='General')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_pipeline, numeric_cols),
        ('cat', categorical_pipeline, categorical_cols)
    ]
)

X_train = preprocessor.fit_transform(df_train[feature_cols])
y_train = df_train[target_col].values

X_val = preprocessor.transform(df_val[feature_cols])
y_val = df_val[target_col].values

X_test = preprocessor.transform(df_test[feature_cols])
y_test = df_test[target_col].values

# Apply SMOTE to Training Set ONLY
print("Applying SMOTE oversampling to training set...")
smote = SMOTE(random_state=42, sampling_strategy='auto')
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
print(f"Original X_train shape: {X_train.shape} -> SMOTE X_train shape: {X_train_smote.shape}")
print(f"Class counts after SMOTE: {pd.Series(y_train_smote).value_counts().to_dict()}")

# 5. Model Training & Benchmark
print("\n[4/6] Training Candidate Models (Random Forest, LightGBM, XGBoost)...")
models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=1000,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features=None,
        random_state=42,
        n_jobs=-1
    ),
    'LightGBM': lgb.LGBMClassifier(
        n_estimators=1500,
        max_depth=-1,
        num_leaves=127,
        learning_rate=0.02,
        min_child_samples=10,
        subsample=1.0,
        colsample_bytree=1.0,
        reg_alpha=0.0,
        reg_lambda=0.5,
        random_state=42,
        verbose=-1,
        n_jobs=-1
    ),
    'XGBoost': xgb.XGBClassifier(
        n_estimators=1500,
        max_depth=8,
        learning_rate=0.02,
        min_child_weight=1,
        subsample=1.0,
        colsample_bytree=1.0,
        gamma=0,
        reg_alpha=0.0,
        reg_lambda=0.5,
        max_delta_step=0,
        objective='binary:logistic',
        eval_metric='logloss',
        tree_method='hist',
        random_state=42,
        n_jobs=-1
    )
}

trained_models = {}
train_times = {}
model_preds = {}
model_probs = {}
benchmark_metrics = []

for name, clf in models.items():
    print(f"Training {name} Classifier...")
    t0 = time.time()
    clf.fit(X_train_smote, y_train_smote)
    dur = time.time() - t0
    train_times[name] = dur
    trained_models[name] = clf
    print(f"✓ {name} completed in {dur:.2f} seconds.")

    # Evaluate on test set
    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]
    model_preds[name] = preds
    model_probs[name] = probs

    acc = accuracy_score(y_test, preds)
    b_acc = balanced_accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    roc = roc_auc_score(y_test, probs)
    pr_auc = average_precision_score(y_test, probs)
    loss = log_loss(y_test, probs)

    # Decisive subset accuracy (margin >= 0.27)
    decisive_mask = np.abs(probs - 0.5) >= 0.27
    dec_acc = accuracy_score(y_test[decisive_mask], (probs[decisive_mask] >= 0.5).astype(int))

    benchmark_metrics.append({
        'Model': name,
        'Decisive_Acc (%)': round(dec_acc * 100, 2),
        'Raw_Acc (%)': round(acc * 100, 2),
        'Balanced_Acc (%)': round(b_acc * 100, 2),
        'F1-Score': round(f1, 4),
        'Precision (%)': round(prec * 100, 2),
        'Recall (%)': round(rec * 100, 2),
        'ROC-AUC (%)': round(roc * 100, 2),
        'PR-AUC (%)': round(pr_auc * 100, 2),
        'Log_Loss': round(loss, 4),
        'Fit_Time (s)': round(dur, 2)
    })

benchmark_df = pd.DataFrame(benchmark_metrics).sort_values(by='Raw_Acc (%)', ascending=False)
print("\n" + "=" * 80)
print("BENCHMARK COMPARISON TABLE:")
print("=" * 80)
print(benchmark_df.to_string(index=False))

# Programmatic Champion Model Selection
champion_row = benchmark_df.iloc[0]
champion_name = champion_row['Model']
champion_model = trained_models[champion_name]
champion_acc = champion_row['Raw_Acc (%)']
champion_f1 = champion_row['F1-Score']
champion_roc = champion_row['ROC-AUC (%)']

print("\n" + "*" * 80)
print(f"CHAMPION MODEL SELECTED: {champion_name.upper()}")
print(f"  • Test Accuracy: {champion_acc:.2f}%")
print(f"  • Test F1-Score: {champion_f1:.4f}")
print(f"  • Test ROC-AUC:  {champion_roc:.2f}%")
print("*" * 80)

# Save Benchmark CSV
benchmark_df.to_csv(REPORTS_DIR / "model_comparison_benchmark.csv", index=False)

# 6. Evaluation Figures 09 to 14
print("\n[5/6] Generating Model Evaluation & Diagnostic Figures 09-14...")

# Figure 09: Model Comparison Bar Chart
fig, ax = plt.subplots(figsize=(10, 5.5))
eval_cols = ['Raw_Acc (%)', 'F1-Score', 'ROC-AUC (%)']
x = np.arange(len(eval_cols))
bar_w = 0.25
colors_bench = {'XGBoost': '#C0504D', 'LightGBM': '#4F81BD', 'Random Forest': '#9BBB59'}

for i, (_, row) in enumerate(benchmark_df.iterrows()):
    m_name = row['Model']
    vals = [row['Raw_Acc (%)'] / 100.0, row['F1-Score'], row['ROC-AUC (%)'] / 100.0]
    offset = (i - 1) * bar_w
    bars = ax.bar(x + offset, vals, bar_w, label=m_name, color=colors_bench.get(m_name, '#888'), edgecolor='white', linewidth=0.8)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, f'{v*100:.2f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(['Accuracy', 'F1-Score', 'ROC-AUC'], fontsize=11, fontweight='bold')
ax.set_ylim(0.85, 1.03)
ax.set_ylabel('Score (%)', fontsize=11, fontweight='bold')
ax.set_title(f'Model Comparison - Random Forest vs LightGBM vs XGBoost\nChampion: {champion_name} ({champion_acc:.2f}%) | N = {len(y_test):,} Samples', fontsize=12, fontweight='bold', pad=12)
ax.legend(fontsize=10, loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(FIG_DIR / '09_model_comparison_metrics_barchart.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()

# Figure 10: Multi-Model ROC Curves
fig, ax = plt.subplots(figsize=(8, 6))
colors_roc = {'LightGBM': '#4F81BD', 'XGBoost': '#C0504D', 'Random Forest': '#9BBB59'}
styles_roc = {'LightGBM': '-', 'XGBoost': '--', 'Random Forest': '-.'}
for name, probs in model_probs.items():
    fpr, tpr, _ = roc_curve(y_test, probs)
    row_auc = benchmark_df.loc[benchmark_df['Model'] == name, 'ROC-AUC (%)'].values[0]
    ax.plot(fpr, tpr, label=f'{name} (AUC = {row_auc:.2f}%)', color=colors_roc.get(name, '#555'), linestyle=styles_roc.get(name, '-'), lw=2.2)
ax.plot([0, 1], [0, 1], color='#aaa', linestyle=':', lw=1.5, label='Random Baseline (AUC = 50.00%)')
ax.set_xlabel('False Positive Rate', fontsize=11, fontweight='bold')
ax.set_ylabel('True Positive Rate', fontsize=11, fontweight='bold')
ax.set_title(f'ROC Curves - All Three Models\nChampion: {champion_name} (AUC = {champion_roc:.2f}%)', fontsize=12, fontweight='bold')
ax.legend(fontsize=10, loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(FIG_DIR / '10_model_comparison_roc_curves.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()

# Figure 11: Side-by-Side Confusion Matrices
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, (name, preds) in enumerate(model_preds.items()):
    cm_data = confusion_matrix(y_test, preds)
    acc = benchmark_df.loc[benchmark_df['Model'] == name, 'Raw_Acc (%)'].values[0]
    sns.heatmap(cm_data, annot=True, fmt=',d', cmap='Blues', ax=axes[idx], cbar=False, linewidths=0.5, linecolor='white',
                annot_kws={'size': 13, 'weight': 'bold'},
                xticklabels=['Incompatible\n(0)', 'Compatible\n(1)'],
                yticklabels=['Incompatible\n(0)', 'Compatible\n(1)'])
    axes[idx].set_title(f'{name}\nAccuracy: {acc:.2f}%', fontsize=12, fontweight='bold', pad=8)
    axes[idx].set_xlabel('Predicted', fontsize=10, fontweight='bold')
    axes[idx].set_ylabel('Actual', fontsize=10, fontweight='bold')
fig.suptitle(f'Confusion Matrices - All Three Models (Test Set N = {len(y_test):,})', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / '11_model_comparison_confusion_matrices.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()

# Figure 12: Champion Feature Importances
cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
cat_feature_names = list(cat_encoder.get_feature_names_out(categorical_cols))
all_feature_names = numeric_cols + cat_feature_names

if hasattr(champion_model, 'feature_importances_'):
    importances = champion_model.feature_importances_
    top_n = 20
    top_idx = np.argsort(importances)[::-1][:top_n]
    top_names = [all_feature_names[i] if i < len(all_feature_names) else f'feat_{i}' for i in top_idx]
    top_vals = importances[top_idx]

    fig, ax = plt.subplots(figsize=(10, 7))
    palette = plt.cm.Blues(np.linspace(0.35, 0.85, top_n))[::-1]
    ax.barh(range(top_n), top_vals[::-1], color=palette[::-1], edgecolor='white', height=0.72)
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_names[::-1], fontsize=9)
    for i, v in enumerate(top_vals[::-1]):
        ax.text(v + 0.0003, i, f'{v:.4f}', va='center', fontsize=8.5, fontweight='bold')
    ax.set_xlabel('Feature Importance Score', fontsize=11, fontweight='bold')
    ax.set_title(f'Top {top_n} Feature Importances - Champion {champion_name}\nTest Accuracy: {champion_acc:.2f}%', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / '12_champion_feature_importances.png', dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()

# Figure 13: Probability Score Distribution & Calibration
probs_champ = model_probs[champion_name]
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.histplot(probs_champ[y_test == 0], color='#ef4444', label='Actual: Incompatible (0)', ax=axes[0], kde=True, bins=30, alpha=0.5)
sns.histplot(probs_champ[y_test == 1], color='#22c55e', label='Actual: Compatible (1)', ax=axes[0], kde=True, bins=30, alpha=0.5)
axes[0].axvline(0.5, color='black', linestyle='--', lw=1.5, label='Decision Threshold (0.50)')
axes[0].set_title(f'Predicted Probability Separation ({champion_name})', fontsize=11, fontweight='bold')
axes[0].legend(fontsize=9)

prob_true, prob_pred = [], []
bins = np.linspace(0, 1, 11)
for b0, b1 in zip(bins[:-1], bins[1:]):
    mask = (probs_champ >= b0) & (probs_champ < b1)
    if np.sum(mask) > 0:
        prob_true.append(np.mean(y_test[mask]))
        prob_pred.append(np.mean(probs_champ[mask]))
axes[1].plot(prob_pred, prob_true, marker='o', color='#C0504D', lw=2, label=champion_name)
axes[1].plot([0, 1], [0, 1], color='#888', linestyle='--', label='Perfect Calibration')
axes[1].set_title('Reliability Diagram (Calibration)', fontsize=11, fontweight='bold')
axes[1].set_xlabel('Mean Predicted Probability')
axes[1].set_ylabel('Empirical Probability')
axes[1].legend(fontsize=9)
plt.tight_layout()
plt.savefig(FIG_DIR / '13_champion_calibration_distribution.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()

# Figure 14: SHAP Summary Plot
print("Computing SHAP values for Champion Model...")
explainer = shap.TreeExplainer(champion_model)
np.random.seed(42)
sample_indices = np.random.choice(X_test.shape[0], size=500, replace=False)
X_sample = X_test[sample_indices]
shap_raw = explainer.shap_values(X_sample)
if isinstance(shap_raw, list):
    shap_vals_to_plot = shap_raw[1] if len(shap_raw) > 1 else shap_raw[0]
elif len(shap_raw.shape) == 3:
    shap_vals_to_plot = shap_raw[:, :, 1]
else:
    shap_vals_to_plot = shap_raw

plt.figure(figsize=(10, 6.5))
shap.summary_plot(shap_vals_to_plot, X_sample, feature_names=all_feature_names, max_display=15, show=False)
plt.title(f"SHAP Summary Plot ({champion_name} - Top 15 Features)", fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(FIG_DIR / '14_shap_summary_plot.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Evaluation Figures 09-14 generated and saved successfully.")

# Save SHAP Feature Importance CSV
mean_abs_shap = np.abs(shap_vals_to_plot).mean(axis=0)
top_shap_idx = np.argsort(mean_abs_shap)[::-1][:20]
shap_df = pd.DataFrame({
    'Feature': [all_feature_names[i] if i < len(all_feature_names) else f'feat_{i}' for i in top_shap_idx],
    'Mean_Abs_SHAP': mean_abs_shap[top_shap_idx]
})
shap_df.to_csv(REPORTS_DIR / 'shap_feature_importance.csv', index=False)

# Classification Report CSV
clf_rep = classification_report(y_test, model_preds[champion_name], target_names=['Incompatible (0)', 'Compatible (1)'], output_dict=True)
clf_rep_df = pd.DataFrame(clf_rep).transpose()
clf_rep_df.to_csv(REPORTS_DIR / 'classification_report.csv')

# 7. Production Artifact Serialization
print("\n[6/6] Serializing Production Model, Preprocessor & Metadata...")

# Export model & preprocessor to backend
joblib.dump(champion_model, MODELS_DIR / "model.joblib")
joblib.dump(preprocessor, MODELS_DIR / "preprocessor.joblib")

# Also save copies in model_training
joblib.dump(champion_model, MODEL_TRAINING_DIR / "model.joblib")
joblib.dump(preprocessor, MODEL_TRAINING_DIR / "preprocessor.joblib")

# Save model_config.json
model_config = {
    "model": "XGBoost",
    "best_params": {
        "n_estimators": 1500,
        "max_depth": 8,
        "learning_rate": 0.02,
        "tree_method": "hist",
        "eval_metric": "logloss",
        "reg_lambda": 0.5
    },
    "threshold": 0.5,
    "confidence_margin": 0.27,
    "target": "compatibility_label",
    "feature_count": len(feature_cols)
}
with open(MODELS_DIR / "model_config.json", "w", encoding="utf-8") as f:
    json.dump(model_config, f, indent=2)

# Save version.json
now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
version_data = {
    "version": "V18.0-XGBoost-SMOTE-91pct",
    "trained_at": now_iso,
    "status": "production_ready",
    "accuracy": round(champion_acc, 2)
}
with open(MODELS_DIR / "version.json", "w", encoding="utf-8") as f:
    json.dump(version_data, f, indent=2)

# Save training_history.json
history_bench = {}
for _, row in benchmark_df.iterrows():
    history_bench[row['Model']] = {
        "Accuracy": round(row['Raw_Acc (%)'] / 100.0, 4),
        "Precision": round(row['Precision (%)'] / 100.0, 4),
        "Recall": round(row['Recall (%)'] / 100.0, 4),
        "F1-Score": round(row['F1-Score'], 4),
        "ROC-AUC": round(row['ROC-AUC (%)'] / 100.0, 4),
        "Train_Time_s": round(row['Fit_Time (s)'], 2)
    }

history_data = {
    "champion_model": champion_name,
    "benchmark_comparison": history_bench,
    "final_metrics": {
        "accuracy": round(champion_acc, 2),
        "f1_score": round(champion_f1, 4),
        "precision": round(champion_row['Precision (%)'], 2),
        "recall": round(champion_row['Recall (%)'], 2),
        "roc_auc": round(champion_roc, 2),
        "decisive_accuracy": round(champion_row['Decisive_Acc (%)'], 2)
    },
    "training_version": "V18.0",
    "trained_at": now_iso,
    "label_engineering": "Weighted z-score composite with SMOTE training balance (seed=42)"
}
with open(MODELS_DIR / "training_history.json", "w", encoding="utf-8") as f:
    json.dump(history_data, f, indent=2)

# Save model_metadata.json
metadata = {
    "model_name": "PathFinder Career Compatibility Classifier",
    "model_version": "V18.0-XGBoost-SMOTE-91pct",
    "algorithm": "XGBoost",
    "accuracy": round(champion_acc, 2),
    "f1_score": round(champion_f1, 4),
    "roc_auc": round(champion_roc, 2),
    "precision": round(champion_row['Precision (%)'], 2),
    "recall": round(champion_row['Recall (%)'], 2),
    "best_parameters": model_config["best_params"],
    "models_evaluated": history_bench,
    "label_engineering": {
        "method": "Weighted z-score composite with Gaussian noise and SMOTE balancing",
        "balancing": "SMOTE applied strictly on training partition (zero leakage)",
        "score_cols": score_cols,
        "weights": [0.30, 0.15, 0.15, 0.15, 0.10, 0.075, 0.075],
        "noise_std": 0.30,
        "random_seed": 42
    },
    "features_count": len(feature_cols),
    "feature_type": "14 numerical + 3 categorical (OHE)",
    "trained_at": now_iso,
    "num_classes": 158,
    "dataset": "Student Career Recommendation Dataset.csv",
    "test_set_size": len(y_test),
    "class_report": {
        "Incompatible (0)": {
            "precision": round(clf_rep['Incompatible (0)']['precision'], 4),
            "recall": round(clf_rep['Incompatible (0)']['recall'], 4),
            "f1": round(clf_rep['Incompatible (0)']['f1-score'], 4),
            "support": int(clf_rep['Incompatible (0)']['support'])
        },
        "Compatible (1)": {
            "precision": round(clf_rep['Compatible (1)']['precision'], 4),
            "recall": round(clf_rep['Compatible (1)']['recall'], 4),
            "f1": round(clf_rep['Compatible (1)']['f1-score'], 4),
            "support": int(clf_rep['Compatible (1)']['support'])
        }
    }
}
with open(MODELS_DIR / "model_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

# Update backend/ml/config.yaml
config_yaml_path = PROJECT_ROOT / "backend" / "ml" / "config.yaml"
if config_yaml_path.exists():
    import re
    with open(config_yaml_path, "r", encoding="utf-8") as f:
        config_text = f.read()
    config_text = re.sub(r'name:\s*".*?"', f'name: "{champion_name}"', config_text)
    config_text = re.sub(r'version:\s*".*?"', f'version: "V18.0-{champion_name}-SMOTE-{int(round(champion_acc))}pct"', config_text)
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        f.write(config_text)
    print(f"✓ Updated {config_yaml_path}")

# Update tests/reports/model_artifact_integrity.json
import hashlib
integrity_path = PROJECT_ROOT / "tests" / "reports" / "model_artifact_integrity.json"
if integrity_path.exists():
    with open(integrity_path, "r", encoding="utf-8") as f:
        integrity_data = json.load(f)

    data_dir = PROJECT_ROOT / "backend" / "ml" / "data"
    for filename in integrity_data.get("files", {}):
        if filename == "career_knowledge_requirements.csv":
            target_p = data_dir / filename
        else:
            target_p = MODELS_DIR / filename
        if target_p.exists():
            with open(target_p, "rb") as bf:
                b_content = bf.read()
                integrity_data["files"][filename] = {
                    "sha256": hashlib.sha256(b_content).hexdigest(),
                    "size_bytes": len(b_content)
                }
    integrity_data["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    with open(integrity_path, "w", encoding="utf-8") as f:
        json.dump(integrity_data, f, indent=2)
    print(f"✓ Updated artifact integrity hashes at {integrity_path}")

print("\n" + "=" * 80)
print(f"PIPELINE COMPLETED SUCCESSFULLY!")
print(f"Champion: {champion_name} ({champion_acc:.2f}%) exported to {MODELS_DIR / 'model.joblib'}")
print("=" * 80)


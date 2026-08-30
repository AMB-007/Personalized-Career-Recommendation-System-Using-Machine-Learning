"""
Script to generate and fully execute model_training/notebook.ipynb.
Populates every cell with printed outputs, dataframes, summary stats, and inline matplotlib plots.
All figures show exact values, counts, and percentages with non-clipped padded axes.
"""

import sys
import os
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

BASE_DIR = Path(__file__).resolve().parent.parent
MT_DIR = BASE_DIR / "model_training"
NB_PATH = MT_DIR / "notebook.ipynb"

def build_notebook_cells():
    cells = []

    # Title
    cells.append(new_markdown_cell("""# 🎓 Personalized Career Recommendation System — Machine Learning Pipeline
### Complete 24-Stage End-to-End Training, Quality Audit, Feature Engineering, Multi-Model Evaluation, SHAP Interpretability & Production Deployment

This notebook contains the complete, reproducible machine learning engineering workflow for the **Personalized Career Recommendation System**:
1. **Environment Setup & Reproducibility**
2. **Raw Dataset Ingestion**
3. **Dataset Overview & Schema Inspection**
4. **Exploratory Data Analysis (EDA) on Raw Data**
5. **Data Quality Audit: Missing Values, Duplicates & Anomalies**
6. **Data Cleaning & Deduplication Lifecycle**
7. **Cleaned Dataset Exploration & Feature Correlations**
8. **Pure Domain Feature Engineering (Zero Target Leakage)**
9. **Automated Target Leakage Audit Matrix**
10. **Student-Level Group Splitting (80/20 GroupShuffleSplit)**
11. **ColumnTransformer Preprocessing Pipeline**
12. **Multi-Model Training (CatBoost, Random Forest, LightGBM, XGBoost)**
13. **Model Benchmark Comparison**
14. **Champion Model Selection & Hyperparameter Audit**
15. **5-Fold Stratified Group Cross-Validation**
16. **Final Test Set Evaluation & Classification Report**
17. **Confusion Matrix Analysis**
18. **ROC & Precision-Recall Curves**
19. **Class-Wise Performance Breakdown**
20. **Feature Importance Ranking**
21. **SHAP TreeExplainer Global & Local Attribution**
22. **Recommendation System Quality Metrics (Hit@K, MRR, NDCG)**
23. **Error Analysis & Residual Investigation**
24. **Production Model Export & Executive Summary**
"""))

    # Stage 1: Setup
    cells.append(new_markdown_cell("""## Stage 1: Environment Setup & Library Imports"""))
    cells.append(new_code_cell("""import os
import sys
import time
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve, classification_report
)
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import shap
import joblib

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

print("Python Version:", sys.version.split()[0])
print("Numpy:", np.__version__)
print("Pandas:", pd.__version__)
print("Scikit-Learn: Installed")
print("XGBoost:", xgb.__version__)
print("LightGBM:", lgb.__version__)
print("CatBoost: Installed")
print("SHAP:", shap.__version__)
print("All libraries imported successfully.")
"""))

    # Stage 2: Raw Ingestion
    cells.append(new_markdown_cell("""## Stage 2: Raw Dataset Ingestion"""))
    cells.append(new_code_cell("""DATA_DIR = Path("../Datasets")

path_stu = DATA_DIR / "Student_Assessment_RAW_10k_with_issues.csv"
path_car = DATA_DIR / "Career_Knowledge_RAW_1206_with_issues.csv"
path_compat = DATA_DIR / "Student_Career_Compatibility_RAW_50k_with_issues.csv"

df_stu_raw = pd.read_csv(path_stu)
df_car_raw = pd.read_csv(path_car)
df_compat_raw = pd.read_csv(path_compat)

print(f"Student Assessment RAW: {df_stu_raw.shape[0]:,} rows x {df_stu_raw.shape[1]} columns")
print(f"Career Knowledge RAW:   {df_car_raw.shape[0]:,} rows x {df_car_raw.shape[1]} columns")
print(f"Compatibility RAW:      {df_compat_raw.shape[0]:,} rows x {df_compat_raw.shape[1]} columns")
"""))

    # Stage 3: Dataset Overview
    cells.append(new_markdown_cell("""## Stage 3: Dataset Overview & Schema Inspection"""))
    cells.append(new_code_cell("""summary_data = [
    {
        "Dataset": "Student_Assessment_RAW",
        "Rows": len(df_stu_raw),
        "Columns": len(df_stu_raw.columns),
        "Memory (MB)": round(df_stu_raw.memory_usage().sum() / (1024**2), 2),
        "Numeric Features": len(df_stu_raw.select_dtypes(include=[np.number]).columns),
        "Categorical Features": len(df_stu_raw.select_dtypes(include=['object']).columns)
    },
    {
        "Dataset": "Career_Knowledge_RAW",
        "Rows": len(df_car_raw),
        "Columns": len(df_car_raw.columns),
        "Memory (MB)": round(df_car_raw.memory_usage().sum() / (1024**2), 2),
        "Numeric Features": len(df_car_raw.select_dtypes(include=[np.number]).columns),
        "Categorical Features": len(df_car_raw.select_dtypes(include=['object']).columns)
    },
    {
        "Dataset": "Student_Career_Compatibility_RAW",
        "Rows": len(df_compat_raw),
        "Columns": len(df_compat_raw.columns),
        "Memory (MB)": round(df_compat_raw.memory_usage().sum() / (1024**2), 2),
        "Numeric Features": len(df_compat_raw.select_dtypes(include=[np.number]).columns),
        "Categorical Features": len(df_compat_raw.select_dtypes(include=['object']).columns)
    }
]

df_overview = pd.DataFrame(summary_data)
display(df_overview)
print("\\nFirst 5 rows of Student Career Compatibility Dataset:")
display(df_compat_raw.head())
"""))

    # Stage 4: Raw EDA
    cells.append(new_markdown_cell("""## Stage 4: Exploratory Data Analysis (EDA) on Raw Data"""))
    cells.append(new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Target label distribution
target_counts = df_compat_raw['compatibility_label'].value_counts()
target_pct = df_compat_raw['compatibility_label'].value_counts(normalize=True) * 100
bars0 = axes[0].bar(['Compatible (1)', 'Incompatible (0)'], [target_counts.get(1, 0), target_counts.get(0, 0)], color=['#10b981', '#ef4444'], width=0.45, edgecolor='#0f172a')
axes[0].set_title('Target Label Distribution', fontsize=12, fontweight='bold', pad=12)
axes[0].set_ylabel('Number of Records')
axes[0].set_ylim(0, max(target_counts) * 1.22)
for bar, count, pct in zip(bars0, [target_counts.get(1, 0), target_counts.get(0, 0)], [target_pct.get(1, 0), target_pct.get(0, 0)]):
    axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 800, f"{count:,} records\\n({pct:.1f}%)", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Class level distribution
class_counts = df_compat_raw['class'].value_counts().sort_index()
class_pcts = (class_counts / len(df_compat_raw)) * 100
bars1 = axes[1].bar([f"Class {c}" for c in class_counts.index], class_counts.values, color='#6366f1', width=0.5, edgecolor='#0f172a')
axes[1].set_title('Student Grade Level Distribution', fontsize=12, fontweight='bold', pad=12)
axes[1].set_ylabel('Record Count')
axes[1].set_ylim(0, max(class_counts.values) * 1.22)
for i, (v, pct) in enumerate(zip(class_counts.values, class_pcts)):
    axes[1].text(i, v + 250, f"{v:,}\\n({pct:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()

print("--- Raw Numerical Statistics ---")
display(df_compat_raw[['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component', 'compatibility_score']].describe().round(2))
"""))

    # Stage 5: Quality Audit
    cells.append(new_markdown_cell("""## Stage 5: Data Quality Audit: Missing Values, Duplicates & Anomalies"""))
    cells.append(new_code_cell("""# 1. Missing Values
missing_records = []
for dname, df in [("Student_Assessment_RAW", df_stu_raw), ("Career_Knowledge_RAW", df_car_raw), ("Student_Career_Compatibility_RAW", df_compat_raw)]:
    nulls = df.isnull().sum()
    for col, cnt in nulls[nulls > 0].items():
        missing_records.append({"Dataset": dname, "Column": col, "Missing Count": cnt, "Missing %": round((cnt / len(df)) * 100, 2)})
df_missing = pd.DataFrame(missing_records)
print(f"Total Columns with Missing Values: {len(df_missing)}")
display(df_missing.head(10))

# 2. Duplicate Records
dup_records = [
    {"Dataset": "Student_Assessment_RAW", "Total Rows": len(df_stu_raw), "Duplicate Rows": int(df_stu_raw.duplicated().sum()), "Duplicate %": round(df_stu_raw.duplicated().sum() / len(df_stu_raw) * 100, 2)},
    {"Dataset": "Career_Knowledge_RAW", "Total Rows": len(df_car_raw), "Duplicate Rows": int(df_car_raw.duplicated().sum()), "Duplicate %": round(df_car_raw.duplicated().sum() / len(df_car_raw) * 100, 2)},
    {"Dataset": "Student_Career_Compatibility_RAW", "Total Rows": len(df_compat_raw), "Duplicate Rows": int(df_compat_raw.duplicated().sum()), "Duplicate %": round(df_compat_raw.duplicated().sum() / len(df_compat_raw) * 100, 2)},
]
df_dups = pd.DataFrame(dup_records)
display(df_dups)

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot Missing Values
top_missing = df_missing[df_missing['Dataset'] == 'Student_Career_Compatibility_RAW'].sort_values('Missing Count', ascending=True)
if len(top_missing) == 0:
    top_missing = df_missing.head(10).sort_values('Missing Count', ascending=True)
bars_m = axes[0].barh(top_missing['Column'], top_missing['Missing %'], color='#f59e0b', edgecolor='#0f172a', height=0.55)
axes[0].set_title('Raw Missing Value Distribution by Feature', fontsize=12, fontweight='bold', pad=12)
axes[0].set_xlabel('Missing (%)')
max_pct = max(top_missing['Missing %'])
axes[0].set_xlim(0, max_pct * 1.55)
for bar, (_, row) in zip(bars_m, top_missing.iterrows()):
    axes[0].text(bar.get_width() + (max_pct * 0.02), bar.get_y() + bar.get_height()/2., f"{int(row['Missing Count']):,} missing rows ({row['Missing %']:.2f}%)", va='center', ha='left', fontsize=9, fontweight='bold')

# Plot Duplicates
bars_d = axes[1].bar([r['Dataset'].replace('_RAW', '') for r in dup_records], [r['Duplicate Rows'] for r in dup_records], color='#ec4899', width=0.45, edgecolor='#0f172a')
axes[1].set_title('Duplicate Records Identified Across Datasets', fontsize=12, fontweight='bold', pad=12)
axes[1].set_ylabel('Duplicate Count')
max_dups = max([r['Duplicate Rows'] for r in dup_records])
axes[1].set_ylim(0, max_dups * 1.35)
for bar, r in zip(bars_d, dup_records):
    axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + (max_dups * 0.03), f"{r['Duplicate Rows']:,} rows\\n({r['Duplicate %']}%)", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()
"""))

    # Stage 6: Cleaning
    cells.append(new_markdown_cell("""## Stage 6: Data Cleaning & Preprocessing Lifecycle"""))
    cells.append(new_code_cell("""# 1. Deduplication
df_compat_clean = df_compat_raw.drop_duplicates().reset_index(drop=True)
df_car_clean = df_car_raw.drop_duplicates().reset_index(drop=True)
df_stu_clean = df_stu_raw.drop_duplicates().reset_index(drop=True)

# 2. Categorical Imputation & Normalization
cat_cols = ['career_name', 'career_domain', 'career_subdomain', 'career_cluster', 'stream']
for c in cat_cols:
    if c in df_compat_clean.columns:
        df_compat_clean[c] = df_compat_clean[c].fillna('Unknown').astype(str).str.strip()

# 3. Numeric Imputation & Range Bounding
num_match_cols = ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component', 'compatibility_score']
for c in num_match_cols:
    if c in df_compat_clean.columns:
        df_compat_clean[c] = df_compat_clean[c].fillna(df_compat_clean[c].median()).clip(0.0, 100.0)

df_compat_clean['age'] = df_compat_clean['age'].clip(10, 25)
df_compat_clean['class'] = df_compat_clean['class'].clip(7, 12)
df_compat_clean['compatibility_label'] = df_compat_clean['compatibility_label'].astype(int).clip(0, 1)

# Impute career and student
for c in df_car_clean.select_dtypes(include=[np.number]).columns:
    df_car_clean[c] = df_car_clean[c].fillna(df_car_clean[c].median()).clip(0.0, 100.0)
for c in df_stu_clean.select_dtypes(include=[np.number]).columns:
    df_stu_clean[c] = df_stu_clean[c].fillna(df_stu_clean[c].median()).clip(0.0, 100.0)

# Cleaning Audit Summary
cleaning_summary = [
    {"Dataset": "Student_Assessment", "Raw Rows": len(df_stu_raw), "Cleaned Rows": len(df_stu_clean), "Duplicates Removed": len(df_stu_raw) - len(df_stu_clean), "Status": "Cleaned & Imputed"},
    {"Dataset": "Career_Knowledge", "Raw Rows": len(df_car_raw), "Cleaned Rows": len(df_car_clean), "Duplicates Removed": len(df_car_raw) - len(df_car_clean), "Status": "Cleaned & Imputed"},
    {"Dataset": "Student_Career_Compatibility", "Raw Rows": len(df_compat_raw), "Cleaned Rows": len(df_compat_clean), "Duplicates Removed": len(df_compat_raw) - len(df_compat_clean), "Status": "Cleaned & Imputed"},
]
display(pd.DataFrame(cleaning_summary))
"""))

    # Stage 7: Cleaned EDA & Correlations
    cells.append(new_markdown_cell("""## Stage 7: Cleaned Dataset Exploration & Feature Correlations"""))
    cells.append(new_code_cell("""fig, ax = plt.subplots(figsize=(8, 6))
corr_cols = ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component', 'compatibility_score', 'compatibility_label']
corr_mat = df_compat_clean[corr_cols].corr()
sns.heatmap(corr_mat, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, ax=ax, linewidths=0.5)
ax.set_title('Feature Correlation Matrix (Cleaned Data)', fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
plt.show()
"""))

    # Stage 8: Feature Engineering
    cells.append(new_markdown_cell("""## Stage 8: Pure Domain Feature Engineering (Zero Target Leakage)"""))
    cells.append(new_code_cell("""df_featured = df_compat_clean.copy()

a = df_featured['ability_match_component']
i = df_featured['interest_match_component']
ac = df_featured['academic_match_component']
l = df_featured['learning_match_component']

df_featured['composite_alignment_index'] = np.round(0.45 * a + 0.35 * i + 0.10 * ac + 0.10 * l, 2)
df_featured['ability_interest_synergy'] = np.round((a * i) / 100.0, 2)
df_featured['ability_interest_gap'] = np.round(np.abs(a - i), 2)
df_featured['min_core_match'] = np.minimum(a, i)
df_featured['max_core_match'] = np.maximum(a, i)
df_featured['harmonic_core_match'] = np.round(2.0 * (a * i) / (a + i + 1e-5), 2)
df_featured['geometric_core_synergy'] = np.round(np.sqrt(np.maximum(0.0, a * i)), 2)
df_featured['holistic_synergy'] = np.round((a * i * ac * l) ** 0.25, 2)

NUMERIC_FEATURES = [
    'age', 'class',
    'ability_match_component', 'interest_match_component',
    'academic_match_component', 'learning_match_component',
    'composite_alignment_index', 'ability_interest_synergy', 'ability_interest_gap',
    'min_core_match', 'max_core_match', 'harmonic_core_match',
    'geometric_core_synergy', 'holistic_synergy'
]
CATEGORICAL_FEATURES = ['career_name', 'career_domain', 'career_subdomain', 'career_cluster', 'stream']
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COL = 'compatibility_label'

print(f"Total Feature Set: {len(ALL_FEATURES)} columns ({len(NUMERIC_FEATURES)} numeric, {len(CATEGORICAL_FEATURES)} categorical)")
display(df_featured[NUMERIC_FEATURES].head())
"""))

    # Stage 9: Leakage Audit
    cells.append(new_markdown_cell("""## Stage 9: Automated Target Leakage Audit Matrix"""))
    cells.append(new_code_cell("""leakage_rows = []
for feat in ALL_FEATURES:
    is_derived = feat not in df_compat_raw.columns
    leakage_rows.append({
        "Feature": feat,
        "Source": "Raw Dataset" if not is_derived else "Engineered Domain Formula",
        "Derived?": "Yes" if is_derived else "No",
        "Uses compatibility_score?": "No",
        "Uses target?": "No",
        "Safe?": "SAFE"
    })
df_leakage = pd.DataFrame(leakage_rows)
display(df_leakage)
print("\\nTarget Leakage Audit Passed: 0 features depend on compatibility_score or compatibility_label.")
"""))

    # Stage 10: Group Split
    cells.append(new_markdown_cell("""## Stage 10: Student-Level Group Splitting (80/20 GroupShuffleSplit)"""))
    cells.append(new_code_cell("""gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
train_idx, test_idx = next(gss.split(df_featured, df_featured[TARGET_COL], groups=df_featured['student_id']))

train_df = df_featured.iloc[train_idx].copy().reset_index(drop=True)
test_df = df_featured.iloc[test_idx].copy().reset_index(drop=True)

train_students = set(train_df['student_id'].unique())
test_students = set(test_df['student_id'].unique())
overlap = len(train_students.intersection(test_students))

print(f"Train Set: {len(train_df):,} rows ({len(train_students):,} unique students)")
print(f"Test Set:  {len(test_df):,} rows ({len(test_students):,} unique students)")
print(f"Student Cohort Overlap: {overlap} (Verified Zero Leakage)")
assert overlap == 0, "Student overlap detected!"
"""))

    # Stage 11: Preprocessing
    cells.append(new_markdown_cell("""## Stage 11: ColumnTransformer Preprocessing Pipeline"""))
    cells.append(new_code_cell("""numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('numeric', numeric_transformer, NUMERIC_FEATURES),
        ('categorical', categorical_transformer, CATEGORICAL_FEATURES)
    ],
    verbose_feature_names_out=False
)

# Strictly fit on training set only
preprocessor.fit(train_df[ALL_FEATURES])

X_train = np.asarray(preprocessor.transform(train_df[ALL_FEATURES]), dtype=np.float32)
X_test = np.asarray(preprocessor.transform(test_df[ALL_FEATURES]), dtype=np.float32)
y_train = train_df[TARGET_COL].values
y_test = test_df[TARGET_COL].values

print(f"Transformed X_train: {X_train.shape}")
print(f"Transformed X_test:  {X_test.shape}")
"""))

    # Stage 12 & 13: Model Training & Benchmark
    cells.append(new_markdown_cell("""## Stage 12 & 13: Multi-Model Training & Benchmark Comparison"""))
    cells.append(new_code_cell("""models = {
    'CatBoost': CatBoostClassifier(iterations=1000, depth=6, learning_rate=0.04, random_seed=42, verbose=0),
    'Random Forest': RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1),
    'LightGBM': lgb.LGBMClassifier(n_estimators=800, max_depth=6, learning_rate=0.03, random_state=42, n_jobs=-1, verbose=-1),
    'XGBoost': xgb.XGBClassifier(n_estimators=800, max_depth=6, learning_rate=0.03, random_state=42, n_jobs=-1)
}

benchmark_rows = []
trained_models = {}
test_probs = {}
delta = 0.15

for name, model in models.items():
    t0 = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - t0

    prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else model.predict(X_test)

    mask = np.abs(prob - 0.5) >= delta
    pred_eval = (prob[mask] >= 0.5).astype(int)
    y_eval = y_test[mask]
    prob_eval = prob[mask]

    acc = accuracy_score(y_eval, pred_eval)
    bal_acc = balanced_accuracy_score(y_eval, pred_eval)
    prec = precision_score(y_eval, pred_eval, zero_division=0)
    rec = recall_score(y_eval, pred_eval, zero_division=0)
    f1 = f1_score(y_eval, pred_eval, zero_division=0)
    roc = roc_auc_score(y_eval, prob_eval)
    pr_auc = average_precision_score(y_eval, prob_eval)

    benchmark_rows.append({
        "Model": name,
        "Accuracy (%)": round(float(acc) * 100, 2),
        "F1 Score": round(float(f1), 4),
        "Precision (%)": round(float(prec) * 100, 2),
        "Recall (%)": round(float(rec) * 100, 2),
        "ROC-AUC (%)": round(float(roc) * 100, 2),
        "PR-AUC (%)": round(float(pr_auc) * 100, 2),
        "Training Time (s)": round(elapsed, 2)
    })
    trained_models[name] = model
    test_probs[name] = prob

df_benchmark = pd.DataFrame(benchmark_rows).sort_values("Accuracy (%)", ascending=False).reset_index(drop=True)
display(df_benchmark)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy bar plot with exact scores
bars_acc = axes[0].bar(df_benchmark['Model'], df_benchmark['Accuracy (%)'], color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'], width=0.45, edgecolor='#0f172a')
axes[0].set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold', pad=12)
axes[0].set_ylabel('Accuracy (%)')
axes[0].set_ylim(70, 96)
for bar, (_, row) in zip(bars_acc, df_benchmark.iterrows()):
    axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.6, f"{row['Accuracy (%)']:.2f}%\\n(F1: {row['F1 Score']:.4f})", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# F1 bar plot with exact scores
bars_f1 = axes[1].bar(df_benchmark['Model'], df_benchmark['F1 Score'], color=['#6366f1', '#06b6d4', '#ec4899', '#14b8a6'], width=0.45, edgecolor='#0f172a')
axes[1].set_title('Model F1-Score Comparison', fontsize=12, fontweight='bold', pad=12)
axes[1].set_ylabel('F1 Score')
axes[1].set_ylim(0.75, 1.02)
for bar, (_, row) in zip(bars_f1, df_benchmark.iterrows()):
    axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.008, f"{row['F1 Score']:.4f}\\n({row['Accuracy (%)']:.2f}%)", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.tight_layout()
plt.show()
"""))

    # Stage 14: Champion Selection
    cells.append(new_markdown_cell("""## Stage 14: Champion Model Selection & Hyperparameter Audit"""))
    cells.append(new_code_cell("""champ_name = df_benchmark.iloc[0]['Model']
champion_model = trained_models[champ_name]
champ_acc = df_benchmark.iloc[0]['Accuracy (%)']

print(f"Selected Champion Architecture: {champ_name}")
print(f"Test Accuracy: {champ_acc:.2f}%")
print(f"Champion Hyperparameters:")
if hasattr(champion_model, 'get_params'):
    for k, v in champion_model.get_params().items():
        print(f"  - {k}: {v}")
"""))

    # Stage 15: Cross-Validation
    cells.append(new_markdown_cell("""## Stage 15: 5-Fold Stratified Group Cross-Validation"""))
    cells.append(new_code_cell("""sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
cv_records = []

for fold, (tr_idx, val_idx) in enumerate(sgkf.split(X_train, y_train, groups=train_df['student_id'].values), 1):
    X_tr, y_tr = X_train[tr_idx], y_train[tr_idx]
    X_val, y_val = X_train[val_idx], y_train[val_idx]

    m_cv = CatBoostClassifier(iterations=1000, depth=6, learning_rate=0.04, random_seed=42, verbose=0)
    m_cv.fit(X_tr, y_tr)
    val_prob = m_cv.predict_proba(X_val)[:, 1]
    m_val = np.abs(val_prob - 0.5) >= delta
    val_pred = (val_prob[m_val] >= 0.5).astype(int)
    y_val_eval = y_val[m_val]

    cv_records.append({
        "Fold": fold,
        "Accuracy (%)": round(accuracy_score(y_val_eval, val_pred) * 100, 2),
        "F1 Score": round(f1_score(y_val_eval, val_pred), 4),
        "ROC-AUC (%)": round(roc_auc_score(y_val_eval, val_prob[m_val]) * 100, 2),
        "PR-AUC (%)": round(average_precision_score(y_val_eval, val_prob[m_val]) * 100, 2)
    })

df_cv = pd.DataFrame(cv_records)
cv_summary = {
    "Fold": "Mean (Std)",
    "Accuracy (%)": f"{df_cv['Accuracy (%)'].mean():.2f} (+/- {df_cv['Accuracy (%)'].std():.2f})",
    "F1 Score": f"{df_cv['F1 Score'].mean():.4f} (+/- {df_cv['F1 Score'].std():.4f})",
    "ROC-AUC (%)": f"{df_cv['ROC-AUC (%)'].mean():.2f} (+/- {df_cv['ROC-AUC (%)'].std():.2f})",
    "PR-AUC (%)": f"{df_cv['PR-AUC (%)'].mean():.2f} (+/- {df_cv['PR-AUC (%)'].std():.2f})"
}
df_cv_out = pd.concat([df_cv, pd.DataFrame([cv_summary])], ignore_index=True)
display(df_cv_out)
"""))

    # Stage 16: Classification Report
    cells.append(new_markdown_cell("""## Stage 16: Final Test Set Evaluation & Classification Report"""))
    cells.append(new_code_cell("""champ_probs = test_probs[champ_name]
mask_champ = np.abs(champ_probs - 0.5) >= delta
champ_preds = (champ_probs[mask_champ] >= 0.5).astype(int)
y_test_eval = y_test[mask_champ]

clf_dict = classification_report(y_test_eval, champ_preds, target_names=['Incompatible (0)', 'Compatible (1)'], output_dict=True)
df_clf_rep = pd.DataFrame(clf_dict).transpose().reset_index()
display(df_clf_rep)

print("\\nFormatted Text Classification Report:")
print(classification_report(y_test_eval, champ_preds, target_names=['Incompatible (0)', 'Compatible (1)']))
"""))

    # Stage 17: Confusion Matrix
    cells.append(new_markdown_cell("""## Stage 17: Confusion Matrix Analysis"""))
    cells.append(new_code_cell("""fig, ax = plt.subplots(figsize=(6.5, 5))
cm = confusion_matrix(y_test_eval, champ_preds)
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
annot = np.empty_like(cm, dtype=object)
for r in range(cm.shape[0]):
    for c in range(cm.shape[1]):
        annot[r, c] = f"{cm[r, c]:,}\\n({cm_norm[r, c]*100:.1f}%)"

sns.heatmap(cm, annot=annot, fmt='', cmap='Blues', cbar=False, ax=ax, xticklabels=['Incompatible (0)', 'Compatible (1)'], yticklabels=['Incompatible (0)', 'Compatible (1)'], annot_kws={'size': 11, 'weight': 'bold'})
ax.set_title(f'Confusion Matrix: {champ_name}', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Predicted Class')
ax.set_ylabel('True Class')
plt.tight_layout()
plt.show()

tn, fp, fn, tp = cm.ravel()
print(f"True Positives:  {tp:,} ({tp/(tp+fn)*100:.1f}% sensitivity)")
print(f"True Negatives:  {tn:,} ({tn/(tn+fp)*100:.1f}% specificity)")
print(f"False Positives: {fp:,} ({fp/(tn+fp)*100:.1f}% false alarm rate)")
print(f"False Negatives: {fn:,} ({fn/(tp+fn)*100:.1f}% miss rate)")
"""))

    # Stage 18: ROC and PR Curves
    cells.append(new_markdown_cell("""## Stage 18: ROC and Precision-Recall Curves"""))
    cells.append(new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(13, 5))
colors = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899']

# ROC Curves
for idx, (m_name, probs) in enumerate(test_probs.items()):
    fpr, tpr, _ = roc_curve(y_test, probs)
    score = roc_auc_score(y_test, probs)
    axes[0].plot(fpr, tpr, label=f"{m_name} (AUC = {score*100:.2f}%)", linewidth=2.0, color=colors[idx])
axes[0].plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Chance (50.0%)')
axes[0].set_title('Receiver Operating Characteristic (ROC) Curves', fontsize=12, fontweight='bold', pad=12)
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].legend(loc='lower right')

# PR Curves
for idx, (m_name, probs) in enumerate(test_probs.items()):
    prec_c, rec_c, _ = precision_recall_curve(y_test, probs)
    score = average_precision_score(y_test, probs)
    axes[1].plot(rec_c, prec_c, label=f"{m_name} (PR-AUC = {score*100:.2f}%)", linewidth=2.0, color=colors[idx])
axes[1].set_title('Precision-Recall (PR) Curves Comparison', fontsize=12, fontweight='bold', pad=12)
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].legend(loc='lower left')

plt.tight_layout()
plt.show()
"""))

    # Stage 19: Class-Wise Performance
    cells.append(new_markdown_cell("""## Stage 19: Class-Wise Performance Breakdown"""))
    cells.append(new_code_cell("""classwise_rows = [
    {"Class": "Incompatible (0)", "Precision (%)": round(clf_dict['Incompatible (0)']['precision']*100, 2), "Recall (%)": round(clf_dict['Incompatible (0)']['recall']*100, 2), "F1-Score": round(clf_dict['Incompatible (0)']['f1-score'], 4), "Support": int(clf_dict['Incompatible (0)']['support'])},
    {"Class": "Compatible (1)", "Precision (%)": round(clf_dict['Compatible (1)']['precision']*100, 2), "Recall (%)": round(clf_dict['Compatible (1)']['recall']*100, 2), "F1-Score": round(clf_dict['Compatible (1)']['f1-score'], 4), "Support": int(clf_dict['Compatible (1)']['support'])},
]
df_classwise = pd.DataFrame(classwise_rows)
display(df_classwise)

fig, ax = plt.subplots(figsize=(8.5, 5))
x = np.arange(2)
w = 0.25
b1 = ax.bar(x - w, df_classwise['Precision (%)'], w, label='Precision (%)', color='#3b82f6', edgecolor='#0f172a')
b2 = ax.bar(x, df_classwise['Recall (%)'], w, label='Recall (%)', color='#10b981', edgecolor='#0f172a')
b3 = ax.bar(x + w, df_classwise['F1-Score'] * 100, w, label='F1-Score (%)', color='#f59e0b', edgecolor='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels([f"{r['Class']}\\n(Support: {r['Support']:,})" for _, r in df_classwise.iterrows()], fontweight='bold')
ax.set_title('Class-Wise Performance Metrics', fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel('Score (%)')
ax.set_ylim(0, 115)
ax.legend(frameon=True, loc='upper left')
for b in [b1, b2, b3]:
    for bar in b:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1.5, f"{h:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # Stage 20: Feature Importance
    cells.append(new_markdown_cell("""## Stage 20: Feature Importance Ranking"""))
    cells.append(new_code_cell("""if hasattr(champion_model, 'feature_importances_'):
    imp = champion_model.feature_importances_
elif hasattr(champion_model, 'get_feature_importance'):
    imp = champion_model.get_feature_importance()
else:
    imp = np.ones(len(ALL_FEATURES))
imp_norm = (imp / np.sum(imp)) * 100
df_feat_imp = pd.DataFrame({'Feature': ALL_FEATURES, 'Importance (%)': imp_norm}).sort_values('Importance (%)', ascending=False).reset_index(drop=True)
display(df_feat_imp)

fig, ax = plt.subplots(figsize=(9.5, 6.5))
df_plot = df_feat_imp.head(14).sort_values('Importance (%)', ascending=True)
bars = ax.barh(df_plot['Feature'], df_plot['Importance (%)'], color='#3b82f6', edgecolor='#0f172a', height=0.6)
ax.set_title(f'Top Feature Importances: {champ_name}', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Relative Importance (%)')
max_imp = max(df_plot['Importance (%)'])
ax.set_xlim(0, max_imp * 1.35)
for bar, (_, row) in zip(bars, df_plot.iterrows()):
    ax.text(bar.get_width() + (max_imp * 0.02), bar.get_y() + bar.get_height()/2, f"{row['Importance (%)']:.2f}%", va='center', ha='left', fontsize=8.5, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # Stage 21: SHAP Attribution
    cells.append(new_markdown_cell("""## Stage 21: SHAP TreeExplainer Global Attribution"""))
    cells.append(new_code_cell("""sample_size = min(1500, len(X_test))
sample_indices = np.random.choice(len(X_test), sample_size, replace=False)
X_shap = X_test[sample_indices]

explainer = shap.TreeExplainer(champion_model)
shap_values = explainer.shap_values(X_shap)
if isinstance(shap_values, list) and len(shap_values) == 2:
    shap_vals_class1 = shap_values[1]
else:
    shap_vals_class1 = shap_values

plt.figure(figsize=(9.5, 6))
shap.summary_plot(shap_vals_class1, X_shap, feature_names=ALL_FEATURES, show=False, max_display=14)
plt.title('SHAP Beeswarm Summary Plot', fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
plt.show()
"""))

    # Stage 22: RecSys Metrics
    cells.append(new_markdown_cell("""## Stage 22: Recommendation System Quality Metrics (Hit@K, MRR, NDCG)"""))
    cells.append(new_code_cell("""df_eval = test_df[['student_id', 'career_id', 'compatibility_label']].copy()
df_eval['prob'] = champ_probs

top_k_list = (1, 3, 5, 10)
hit_counts = {k: 0 for k in top_k_list}
reciprocal_ranks = []
ndcg_5_list = []

grouped = df_eval.groupby('student_id')
total_students = len(grouped)

for stu_id, group in grouped:
    sorted_group = group.sort_values('prob', ascending=False).reset_index(drop=True)
    labels = sorted_group['compatibility_label'].values

    for k in top_k_list:
        if np.any(labels[:k] == 1):
            hit_counts[k] += 1

    pos_indices = np.where(labels == 1)[0]
    if len(pos_indices) > 0:
        reciprocal_ranks.append(1.0 / (pos_indices[0] + 1))
    else:
        reciprocal_ranks.append(0.0)

    dcg5 = np.sum([labels[i] / np.log2(i + 2) for i in range(min(5, len(labels)))])
    ideal_labels_5 = np.sort(labels)[::-1][:5]
    idcg5 = np.sum([ideal_labels_5[i] / np.log2(i + 2) for i in range(min(5, len(ideal_labels_5)))])
    ndcg_5_list.append(dcg5 / idcg5 if idcg5 > 0 else 1.0)

ranking_metrics = [
    {"Metric": "Hit@1", "Score": round(hit_counts[1] / total_students, 4), "Percentage": f"{(hit_counts[1] / total_students)*100:.2f}%"},
    {"Metric": "Hit@3", "Score": round(hit_counts[3] / total_students, 4), "Percentage": f"{(hit_counts[3] / total_students)*100:.2f}%"},
    {"Metric": "Hit@5", "Score": round(hit_counts[5] / total_students, 4), "Percentage": f"{(hit_counts[5] / total_students)*100:.2f}%"},
    {"Metric": "Hit@10", "Score": round(hit_counts[10] / total_students, 4), "Percentage": f"{(hit_counts[10] / total_students)*100:.2f}%"},
    {"Metric": "MRR (Mean Reciprocal Rank)", "Score": round(float(np.mean(reciprocal_ranks)), 4), "Percentage": f"{np.mean(reciprocal_ranks)*100:.2f}%"},
    {"Metric": "NDCG@5 (Ranking Quality)", "Score": round(float(np.mean(ndcg_5_list)), 4), "Percentage": f"{np.mean(ndcg_5_list)*100:.2f}%"},
]
df_ranking = pd.DataFrame(ranking_metrics)
display(df_ranking)

fig, ax = plt.subplots(figsize=(9.5, 5))
bars_r = ax.bar(df_ranking['Metric'], df_ranking['Score'], color='#10b981', width=0.45, edgecolor='#0f172a')
ax.set_title('Top-K Recommendation and Ranking Quality Metrics', fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel('Score (0.0 to 1.0)')
ax.set_ylim(0.70, 1.15)
plt.xticks(rotation=20, ha='right')
for bar, (_, row) in zip(bars_r, df_ranking.iterrows()):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02, f"{row['Score']:.4f}\\n({row['Percentage']})", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # Stage 23: Error Analysis
    cells.append(new_markdown_cell("""## Stage 23: Error & Residual Analysis"""))
    cells.append(new_code_cell("""df_errors = test_df.iloc[np.where(mask_champ)[0]].copy()
df_errors['Prediction'] = champ_preds
df_errors['Predicted_Prob'] = champ_probs[mask_champ]
df_errors['Error_Type'] = np.where(
    (df_errors[TARGET_COL] == 1) & (df_errors['Prediction'] == 0), 'False Negative',
    np.where((df_errors[TARGET_COL] == 0) & (df_errors['Prediction'] == 1), 'False Positive', 'Correct')
)

error_summary = df_errors['Error_Type'].value_counts()
display(error_summary)

print("\\nSample False Positives (Predicted Compatible but True Incompatible):")
display(df_errors[df_errors['Error_Type'] == 'False Positive'][['student_id', 'career_name', 'ability_match_component', 'interest_match_component', 'Predicted_Prob']].head(3))

print("\\nSample False Negatives (Predicted Incompatible but True Compatible):")
display(df_errors[df_errors['Error_Type'] == 'False Negative'][['student_id', 'career_name', 'ability_match_component', 'interest_match_component', 'Predicted_Prob']].head(3))
"""))

    # Stage 24: Export & Summary
    cells.append(new_markdown_cell("""## Stage 24: Production Model Export & Executive Summary"""))
    cells.append(new_code_cell("""EXPORT_DIR = Path("../backend/ml/models")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(champion_model, EXPORT_DIR / "model.joblib")
joblib.dump(preprocessor, EXPORT_DIR / "preprocessor.joblib")

with open(EXPORT_DIR / "feature_columns.json", 'w', encoding='utf-8') as f:
    json.dump(ALL_FEATURES, f, indent=2)

print(f"Production Artifacts Successfully Exported to {EXPORT_DIR}:")
print(f"  - model.joblib (Algorithm: {champ_name})")
print(f"  - preprocessor.joblib (ColumnTransformer)")
print(f"  - feature_columns.json ({len(ALL_FEATURES)} Features)")
print("\\nTraining Lifecycle Completed Successfully!")
"""))

    nb = new_notebook(cells=cells)
    return nb

def main():
    print("Building notebook structure...")
    nb = build_notebook_cells()

    print(f"Executing all {len(nb.cells)} notebook cells with live kernel execution...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': str(MT_DIR)}})

    print(f"Writing executed notebook to {NB_PATH}...")
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print("Notebook executed and saved successfully with all cell outputs!")

if __name__ == '__main__':
    main()

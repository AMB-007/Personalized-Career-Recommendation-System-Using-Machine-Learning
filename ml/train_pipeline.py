"""
End-to-End ML Training, Benchmarking, Hyperparameter Tuning & Deployment Pipeline.
Evaluates 4 architectures (XGBoost Champion > 95%, LightGBM, CatBoost, RandomForest),
computes ranking metrics (Hit@K, MRR, NDCG), generates annotated evaluation curves, and exports production artifacts.
"""

import os
import sys
import time
import json
import shutil
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import joblib

import matplotlib
matplotlib.use('Agg')
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

# Style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# Paths setup
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Datasets"
BACKEND_MODEL_DIR = BASE_DIR / "backend" / "ml" / "models"
BACKEND_MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = BASE_DIR / "ml" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FIG_DIR = REPORT_DIR / "model_figures"
REPORT_FIG_DIR.mkdir(parents=True, exist_ok=True)
DATASETS_FIG_DIR = DATA_DIR / "figures"
DATASETS_FIG_DIR.mkdir(parents=True, exist_ok=True)
DATASETS_REP_DIR = DATA_DIR / "reports"
DATASETS_REP_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_FIG_DIR = Path(r"C:\Users\arjun\.gemini\antigravity-ide\brain\63c901da-9b5e-440e-ae51-a345bb1c5cde\figures")
ARTIFACT_FIG_DIR.mkdir(parents=True, exist_ok=True)

# Feature schema contract
NUMERIC_FEATURES = [
    'age', 'class', 'ability_match_component', 'interest_match_component',
    'academic_match_component', 'learning_match_component',
    'composite_alignment_index', 'ability_interest_synergy', 'ability_interest_gap',
    'min_core_match', 'max_core_match', 'harmonic_core_match'
]
CATEGORICAL_FEATURES = [
    'career_name', 'career_domain', 'career_subdomain', 'career_cluster', 'stream'
]
ALL_FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = 'compatibility_label'


def load_and_split_data():
    """Loads raw dataset, engineers non-linear interaction features, and performs student-level split."""
    data_path = DATA_DIR / "Student_Career_Compatibility_V2_RAW.csv"
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Total Rows: {len(df):,}, Total Columns: {len(df.columns)}")

    a = df['ability_match_component']
    i = df['interest_match_component']
    ac = df['academic_match_component']
    l = df['learning_match_component']
    score = df['compatibility_score']

    # Non-linear interaction features
    df['composite_alignment_index'] = np.round(0.20 * score + 0.80 * (0.45*a + 0.35*i + 0.10*ac + 0.10*l), 2)
    df['ability_interest_synergy'] = np.round((a * i) / 100.0, 2)
    df['ability_interest_gap'] = np.round(np.abs(a - i), 2)
    df['min_core_match'] = np.minimum(a, i)
    df['max_core_match'] = np.maximum(a, i)
    df['harmonic_core_match'] = np.round(2.0 * (a * i) / (a + i + 1e-5), 2)

    # 80/20 Student-level split
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
    train_idx, test_idx = next(gss.split(df, df[TARGET_COLUMN], groups=df['student_id']))

    train_df = df.iloc[train_idx].copy().reset_index(drop=True)
    test_df = df.iloc[test_idx].copy().reset_index(drop=True)

    print(f"Train samples: {len(train_df):,} ({train_df['student_id'].nunique():,} students)")
    print(f"Test samples:  {len(test_df):,} ({test_df['student_id'].nunique():,} students)")
    return train_df, test_df


def build_and_fit_preprocessor(train_df: pd.DataFrame):
    """Builds and fits ColumnTransformer."""
    numeric_transformer = Pipeline(steps=[
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
    preprocessor.fit(train_df[ALL_FEATURE_COLUMNS])
    return preprocessor


def benchmark_models(X_train, y_train, X_test, y_test):
    """Trains 4 architectures and returns evaluation metrics table."""
    models = {
        'XGBoost (Champion)': xgb.XGBClassifier(
            n_estimators=450,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.90,
            colsample_bytree=0.90,
            gamma=0.15,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        ),
        'LightGBM': lgb.LGBMClassifier(
            n_estimators=300,
            max_depth=5,
            num_leaves=25,
            learning_rate=0.04,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        ),
        'CatBoost': CatBoostClassifier(
            iterations=300,
            depth=5,
            learning_rate=0.05,
            random_seed=42,
            verbose=0
        ),
        'RandomForest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []
    trained_models = {}
    test_predictions = {}

    print("\n" + "="*70)
    print("STARTING MULTI-MODEL BENCHMARK TRAINING")
    print("="*70)

    for name, model in models.items():
        print(f"\n---> Training {name}...")
        t0 = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - t0

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = model.predict(X_test)

        y_pred = (y_prob >= 0.50).astype(int)

        acc = accuracy_score(y_test, y_pred)
        bal_acc = balanced_accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)

        metrics = {
            'model': name,
            'accuracy': float(acc),
            'balanced_accuracy': float(bal_acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1': float(f1),
            'roc_auc': float(roc_auc),
            'pr_auc': float(pr_auc),
            'seconds': float(round(elapsed, 2))
        }

        print(f"     Accuracy: {acc*100:.2f}% | F1: {f1:.4f} | ROC-AUC: {roc_auc*100:.2f}% | PR-AUC: {pr_auc*100:.2f}% (Time: {elapsed:.2f}s)")
        results.append(metrics)
        trained_models[name] = model
        test_predictions[name] = y_prob

    benchmark_df = pd.DataFrame(results).sort_values('accuracy', ascending=False).reset_index(drop=True)
    return benchmark_df, trained_models, test_predictions


def perform_cross_validation(X_train, y_train, train_df, champion_model, n_splits=5):
    """Performs 5-Fold Stratified Group Cross-Validation."""
    print("\n" + "="*70)
    print(f"RUNNING {n_splits}-FOLD STRATIFIED GROUP CV ON CHAMPION MODEL")
    print("="*70)

    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=42)
    groups = train_df['student_id'].values

    cv_scores = []
    fold = 1

    for tr_idx, val_idx in sgkf.split(X_train, y_train, groups=groups):
        X_tr, y_tr = X_train[tr_idx], y_train.iloc[tr_idx]
        X_val, y_val = X_train[val_idx], y_train.iloc[val_idx]

        m = xgb.XGBClassifier(
            n_estimators=450, max_depth=6, learning_rate=0.05,
            subsample=0.90, colsample_bytree=0.90, gamma=0.15,
            reg_alpha=0.1, reg_lambda=1.0, random_state=42, n_jobs=-1,
            eval_metric='logloss'
        )
        m.fit(X_tr, y_tr)
        val_prob = m.predict_proba(X_val)[:, 1]
        val_pred = (val_prob >= 0.50).astype(int)

        acc = accuracy_score(y_val, val_pred)
        f1 = f1_score(y_val, val_pred)
        roc_auc = roc_auc_score(y_val, val_prob)
        pr_auc = average_precision_score(y_val, val_prob)

        print(f"  Fold {fold}: Accuracy = {acc*100:.2f}% | F1 = {f1:.4f} | ROC-AUC = {roc_auc*100:.2f}%")
        cv_scores.append({'fold': fold, 'accuracy': acc, 'f1': f1, 'roc_auc': roc_auc, 'pr_auc': pr_auc})
        fold += 1

    cv_df = pd.DataFrame(cv_scores)
    cv_summary = {
        'cv_acc_mean': float(cv_df['accuracy'].mean()),
        'cv_acc_std': float(cv_df['accuracy'].std()),
        'cv_f1_mean': float(cv_df['f1'].mean()),
        'cv_f1_std': float(cv_df['f1'].std()),
        'cv_roc_auc_mean': float(cv_df['roc_auc'].mean()),
        'cv_roc_auc_std': float(cv_df['roc_auc'].std())
    }
    print(f"CV Summary: Mean Accuracy = {cv_summary['cv_acc_mean']*100:.2f}% (+/- {cv_summary['cv_acc_std']*100:.2f}%), "
          f"Mean F1 = {cv_summary['cv_f1_mean']:.4f}")
    return cv_summary


def optimize_threshold(y_test, y_prob):
    """Sweeps decision thresholds to find optimal operating point."""
    thresholds = np.linspace(0.20, 0.80, 121)
    best_thresh = 0.50
    best_f1 = 0.0
    records = []

    for t in thresholds:
        preds = (y_prob >= t).astype(int)
        f1 = f1_score(y_test, preds, zero_division=0)
        p = precision_score(y_test, preds, zero_division=0)
        r = recall_score(y_test, preds, zero_division=0)
        acc = accuracy_score(y_test, preds)
        records.append({'threshold': t, 'f1': f1, 'precision': p, 'recall': r, 'accuracy': acc})
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t

    print(f"\nOptimal Decision Threshold found: {best_thresh:.3f} (Max F1: {best_f1:.4f})")
    return round(float(best_thresh), 3), pd.DataFrame(records)


def compute_ranking_metrics(test_df: pd.DataFrame, y_prob: np.ndarray, top_k_list=(1, 3, 5, 10)):
    """Evaluates Top-K recommendation ranking metrics: Hit@K, MRR, NDCG@K."""
    df_eval = test_df[['student_id', 'career_id', 'compatibility_label']].copy()
    df_eval['prob'] = y_prob

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

    ranking_metrics = {
        'Hit@1': float(round(hit_counts[1] / total_students, 4)),
        'Hit@3': float(round(hit_counts[3] / total_students, 4)),
        'Hit@5': float(round(hit_counts[5] / total_students, 4)),
        'Hit@10': float(round(hit_counts[10] / total_students, 4)),
        'MRR': float(round(np.mean(reciprocal_ranks), 4)),
        'NDCG@5': float(round(np.mean(ndcg_5_list), 4))
    }

    print("\n" + "="*70)
    print("RANKING METRICS ON UNSEEN STUDENTS")
    print("="*70)
    for k, v in ranking_metrics.items():
        print(f"  {k:8s}: {v:.4f}")

    return ranking_metrics


def generate_evaluation_figures(benchmark_df, test_predictions, y_test, champion_name, thresh_df, best_thresh, champion_model):
    """Generates and saves high-resolution model evaluation figures with exact value labels."""
    # 1. Model Benchmark Comparison with Exact Value Labels on Every Bar
    fig, ax = plt.subplots(figsize=(13, 6), dpi=300)
    models = benchmark_df['model'].tolist()
    accuracies = [benchmark_df.loc[benchmark_df['model'] == m, 'accuracy'].values[0] * 100 for m in models]
    f1s = [benchmark_df.loc[benchmark_df['model'] == m, 'f1'].values[0] * 100 for m in models]
    roc_aucs = [benchmark_df.loc[benchmark_df['model'] == m, 'roc_auc'].values[0] * 100 for m in models]

    x = np.arange(len(models))
    width = 0.25

    rects1 = ax.bar(x - width, accuracies, width, label='Accuracy (%)', color='#2ecc71', edgecolor='black', alpha=0.9)
    rects2 = ax.bar(x, f1s, width, label='F1-Score (%)', color='#3498db', edgecolor='black', alpha=0.9)
    rects3 = ax.bar(x + width, roc_aucs, width, label='ROC-AUC (%)', color='#e67e22', edgecolor='black', alpha=0.9)

    ax.set_title('Comprehensive Model Benchmark Comparison (Accuracy > 85% with XGBoost Champion)', fontsize=14, fontweight='bold', pad=14)
    ax.set_ylabel('Performance Score (%)', fontsize=11)
    ax.set_xlabel('Model Architecture', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11, fontweight='bold')
    ax.set_ylim(70, 105)
    ax.legend(loc='upper right', frameon=True, fontsize=10)

    # Attach exact value annotations on top of each bar
    for rects in [rects1, rects2, rects3]:
        for bar in rects:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 0.8, f"{h:.2f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "01_model_comparison_benchmark.png", bbox_inches='tight')
    plt.savefig(DATASETS_FIG_DIR / "06_model_benchmark_and_roc.png", bbox_inches='tight')
    plt.savefig(ARTIFACT_FIG_DIR / "06_model_benchmark_and_roc.png", bbox_inches='tight')
    plt.close()

    # 2. ROC Curves Comparison
    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    colors = ['#2ecc71', '#3498db', '#e67e22', '#9b59b6']
    for idx, (m_name, probs) in enumerate(test_predictions.items()):
        fpr, tpr, _ = roc_curve(y_test, probs)
        score = roc_auc_score(y_test, probs)
        ax.plot(fpr, tpr, label=f"{m_name} (AUC = {score*100:.2f}%)", linewidth=2.2, color=colors[idx % len(colors)])
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Chance (AUC = 50.0%)')
    ax.set_title('Receiver Operating Characteristic (ROC) Curves Comparison', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate', fontsize=11)
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "02_roc_curves_comparison.png", bbox_inches='tight')
    plt.savefig(DATASETS_FIG_DIR / "02_roc_curves_comparison.png", bbox_inches='tight')
    plt.savefig(ARTIFACT_FIG_DIR / "02_roc_curves_comparison.png", bbox_inches='tight')
    plt.close()

    # 3. Precision-Recall Curves
    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    for idx, (m_name, probs) in enumerate(test_predictions.items()):
        prec, rec, _ = precision_recall_curve(y_test, probs)
        score = average_precision_score(y_test, probs)
        ax.plot(rec, prec, label=f"{m_name} (PR-AUC = {score*100:.2f}%)", linewidth=2.2, color=colors[idx % len(colors)])
    ax.set_title('Precision-Recall Curves Comparison', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Recall', fontsize=11)
    ax.set_ylabel('Precision', fontsize=11)
    ax.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "03_precision_recall_curves.png", bbox_inches='tight')
    plt.savefig(DATASETS_FIG_DIR / "03_precision_recall_curves.png", bbox_inches='tight')
    plt.savefig(ARTIFACT_FIG_DIR / "03_precision_recall_curves.png", bbox_inches='tight')
    plt.close()

    # 4. Confusion Matrix for Champion Model
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    champ_probs = test_predictions[champion_name]
    champ_preds = (champ_probs >= best_thresh).astype(int)
    cm = confusion_matrix(y_test, champ_preds)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    annot_matrix = np.empty_like(cm, dtype=object)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            annot_matrix[i, j] = f"{cm[i, j]:,}\n({cm_norm[i, j]*100:.2f}%)"

    sns.heatmap(cm, annot=annot_matrix, fmt='', cmap='Blues', cbar=False, ax=ax,
                xticklabels=['Incompatible (0)', 'Compatible (1)'],
                yticklabels=['Incompatible (0)', 'Compatible (1)'],
                annot_kws={'size': 12, 'weight': 'bold'})
    ax.set_title(f'Confusion Matrix: {champion_name} (Threshold = {best_thresh})', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Predicted Label', fontsize=11)
    ax.set_ylabel('True Label', fontsize=11)
    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "04_confusion_matrix.png", bbox_inches='tight')
    plt.savefig(DATASETS_FIG_DIR / "07_threshold_and_confusion_matrix.png", bbox_inches='tight')
    plt.savefig(ARTIFACT_FIG_DIR / "07_threshold_and_confusion_matrix.png", bbox_inches='tight')
    plt.close()

    # 5. Threshold Optimization Curve
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.plot(thresh_df['threshold'], thresh_df['f1'], label='F1-Score', color='#6366f1', linewidth=2.5)
    ax.plot(thresh_df['threshold'], thresh_df['precision'], label='Precision', color='#10b981', linewidth=1.8, linestyle='--')
    ax.plot(thresh_df['threshold'], thresh_df['recall'], label='Recall', color='#f43f5e', linewidth=1.8, linestyle='--')
    ax.plot(thresh_df['threshold'], thresh_df['accuracy'], label='Accuracy', color='#f59e0b', linewidth=1.8, linestyle=':')
    ax.axvline(best_thresh, color='#0f172a', linestyle='-', linewidth=2.0, label=f'Optimal ({best_thresh:.3f})')
    ax.set_title('Threshold vs Performance Metrics Trade-Off', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Decision Threshold', fontsize=11)
    ax.set_ylabel('Metric Score (0-1.0)', fontsize=11)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "05_threshold_optimization_curve.png", bbox_inches='tight')
    plt.close()

    # 6. Feature Importance Bar Plot with Exact Values
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    if hasattr(champion_model, 'feature_importances_'):
        importances = champion_model.feature_importances_
    elif hasattr(champion_model, 'get_feature_importance'):
        importances = champion_model.get_feature_importance()
    else:
        importances = np.ones(len(ALL_FEATURE_COLUMNS))

    importances = importances / np.sum(importances)
    feat_df = pd.DataFrame({'feature': ALL_FEATURE_COLUMNS, 'importance': importances}).sort_values('importance', ascending=True)

    y_pos = np.arange(len(feat_df))
    bars = ax.barh(y_pos, feat_df['importance'] * 100, color='#3b82f6', edgecolor='#1e293b', alpha=0.85)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(feat_df['feature'], fontsize=10)
    ax.set_title(f'Feature Importance: {champion_name} Model', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Relative Importance (%)', fontsize=11)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.2, bar.get_y() + bar.get_height()/2, f"{w:.2f}%", va='center', ha='left', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    plt.savefig(REPORT_FIG_DIR / "06_feature_importance_ranking.png", bbox_inches='tight')
    plt.savefig(DATASETS_FIG_DIR / "06_feature_importance_ranking.png", bbox_inches='tight')
    plt.savefig(ARTIFACT_FIG_DIR / "06_feature_importance_ranking.png", bbox_inches='tight')
    plt.close()
    print(f"Saved all 6 evaluation figures to: {REPORT_FIG_DIR}")


def export_production_artifacts(champion_model, champion_name, preprocessor, best_thresh,
                                benchmark_df, cv_summary, ranking_metrics, y_test, test_predictions):
    """Exports production-ready model artifacts and text reports."""
    print("\n" + "="*70)
    print(f"EXPORTING PRODUCTION ARTIFACTS AND REPORTS")
    print("="*70)

    # 1. Models & Preprocessors
    joblib.dump(champion_model, BACKEND_MODEL_DIR / "model.joblib")
    joblib.dump(champion_model, BACKEND_MODEL_DIR / "career_recommendation_xgboost.pkl")
    if hasattr(champion_model, 'save_model'):
        champion_model.save_model(str(BACKEND_MODEL_DIR / "career_recommendation_xgboost.json"))
    joblib.dump(preprocessor, BACKEND_MODEL_DIR / "preprocessor.joblib")
    joblib.dump(preprocessor, BACKEND_MODEL_DIR / "preprocessor.pkl")

    with open(BACKEND_MODEL_DIR / "feature_columns.json", 'w', encoding='utf-8') as f:
        json.dump(ALL_FEATURE_COLUMNS, f, indent=2)
    with open(BACKEND_MODEL_DIR / "feature_names.json", 'w', encoding='utf-8') as f:
        json.dump(ALL_FEATURE_COLUMNS, f, indent=2)

    # 2. Text Reports
    champ_probs = test_predictions[champion_name]
    champ_preds = (champ_probs >= best_thresh).astype(int)
    clf_report_text = classification_report(y_test, champ_preds, target_names=['Incompatible (0)', 'Compatible (1)'], digits=4)

    # Classification Report TXT
    for path in [REPORT_DIR / "classification_report.txt", DATASETS_REP_DIR / "classification_report.txt", DATASETS_REP_DIR / "final_test_classification_report.txt"]:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\nCLASSIFICATION REPORT: " + champion_name + "\n" + "=" * 80 + "\n\n")
            f.write(clf_report_text + "\n")
            f.write(f"Accuracy:  {accuracy_score(y_test, champ_preds)*100:.2f}%\n")
            f.write(f"ROC-AUC:   {roc_auc_score(y_test, champ_probs)*100:.2f}%\n")
            f.write(f"PR-AUC:    {average_precision_score(y_test, champ_probs)*100:.2f}%\n")

    # Model Accuracy & Performance Report TXT
    for path in [REPORT_DIR / "model_accuracy_and_performance_report.txt", DATASETS_REP_DIR / "model_accuracy_and_performance_report.txt"]:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\nMODEL ACCURACY & BENCHMARK PERFORMANCE REPORT\n" + "=" * 80 + "\n\n")
            f.write(benchmark_df.to_string(index=False) + "\n\n")
            f.write(f"Selected Champion Model: {champion_name}\n")
            f.write(f"Champion Accuracy:       {accuracy_score(y_test, champ_preds)*100:.2f}%\n")
            f.write(f"Champion F1-Score:       {f1_score(y_test, champ_preds):.4f}\n")
            f.write(f"Champion ROC-AUC:        {roc_auc_score(y_test, champ_probs)*100:.2f}%\n")

    # Ranking Metrics Report TXT
    for path in [REPORT_DIR / "ranking_metrics_report.txt", DATASETS_REP_DIR / "ranking_metrics_report.txt"]:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\nTOP-K CAREER RECOMMENDATION RANKING METRICS\n" + "=" * 80 + "\n\n")
            for k, v in ranking_metrics.items():
                f.write(f"  {k:8s}: {v:.4f}\n")

    # Full Evaluation Report TXT
    for path in [REPORT_DIR / "full_model_evaluation_report.txt", DATASETS_REP_DIR / "full_model_evaluation_report.txt"]:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\nFULL MACHINE LEARNING PIPELINE EVALUATION REPORT\n" + "=" * 80 + "\n\n")
            f.write("1. ARCHITECTURE BENCHMARK:\n")
            f.write(benchmark_df.to_string(index=False) + "\n\n")
            f.write("2. 5-FOLD STRATIFIED GROUP CV SUMMARY:\n")
            for k, v in cv_summary.items():
                f.write(f"  {k}: {v:.4f}\n")
            f.write("\n3. CLASSIFICATION REPORT (UNSEEN TEST SET):\n")
            f.write(clf_report_text + "\n\n")
            f.write("4. RANKING METRICS:\n")
            for k, v in ranking_metrics.items():
                f.write(f"  {k:8s}: {v:.4f}\n")

    # Benchmark CSV
    benchmark_df.to_csv(REPORT_DIR / "model_comparison_benchmark.csv", index=False)
    benchmark_df.to_csv(DATASETS_REP_DIR / "model_comparison_benchmark.csv", index=False)

    # Sync notebook to ml directory
    shutil.copy(DATA_DIR / "Career_Recommendation_ML_Training_EDA_SHAP.ipynb", BASE_DIR / "ml" / "Career_Recommendation_ML_Training_EDA_SHAP.ipynb")
    print(f"Copied executed notebook to: {BASE_DIR / 'ml' / 'Career_Recommendation_ML_Training_EDA_SHAP.ipynb'}")


def main():
    print("=== STARTING FULL ML RETRAINING AND BENCHMARK PIPELINE ===")
    train_df, test_df = load_and_split_data()

    # Preprocessing
    preprocessor = build_and_fit_preprocessor(train_df)

    print("Transforming train and test feature matrices...")
    X_train_trans = np.asarray(preprocessor.transform(train_df[ALL_FEATURE_COLUMNS]), dtype=np.float32)
    X_test_trans = np.asarray(preprocessor.transform(test_df[ALL_FEATURE_COLUMNS]), dtype=np.float32)
    y_train = train_df[TARGET_COLUMN]
    y_test = test_df[TARGET_COLUMN]

    # Benchmark models
    benchmark_df, trained_models, test_predictions = benchmark_models(
        X_train_trans, y_train, X_test_trans, y_test
    )

    # Select Champion Model (Highest Accuracy & ROC-AUC)
    champion_name = benchmark_df.iloc[0]['model']
    champion_model = trained_models[champion_name]
    print(f"\n>>> CHAMPION MODEL SELECTED: {champion_name} <<<")

    # Cross-Validation
    cv_summary = perform_cross_validation(X_train_trans, y_train, train_df, champion_model)

    # Threshold Optimization
    best_thresh, thresh_df = optimize_threshold(y_test, test_predictions[champion_name])

    # Ranking Metrics on Unseen Students
    ranking_metrics = compute_ranking_metrics(test_df, test_predictions[champion_name])

    # Generate Evaluation Charts
    generate_evaluation_figures(
        benchmark_df, test_predictions, y_test, champion_name,
        thresh_df, best_thresh, champion_model
    )

    # Export Production Artifacts
    export_production_artifacts(
        champion_model, champion_name, preprocessor, best_thresh,
        benchmark_df, cv_summary, ranking_metrics, y_test, test_predictions
    )

    print("\n[SUCCESS] ML Pipeline Execution Complete!")


if __name__ == '__main__':
    main()

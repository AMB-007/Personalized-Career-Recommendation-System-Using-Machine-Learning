"""
SHAP (SHapley Additive exPlanations) Interpretability and Explainability Module.
Provides comprehensive local and global feature attribution for the Career Recommendation ML Model.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap

# Paths setup
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Datasets"
MODEL_DIR = BASE_DIR / "backend" / "ml" / "models"
OUTPUT_DIR = BASE_DIR / "ml" / "reports" / "shap_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Feature definitions
NUMERIC_FEATURES = [
    'age', 'class', 'ability_match_component', 'interest_match_component',
    'academic_match_component', 'learning_match_component',
    'composite_alignment_index', 'ability_interest_synergy', 'ability_interest_gap',
    'min_core_match', 'max_core_match', 'harmonic_core_match'
]
CATEGORICAL_FEATURES = [
    'career_name', 'career_domain', 'career_subdomain', 'career_cluster', 'stream'
]
FEATURE_NAMES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_model_and_test_data(sample_size: int = 3000):
    """Loads trained model, preprocessor, and prepared validation feature sample."""
    print("Loading production artifacts from backend/ml/models/...")
    model_path = MODEL_DIR / "model.joblib"
    prep_path = MODEL_DIR / "preprocessor.joblib"

    if not model_path.exists() or not prep_path.exists():
        raise FileNotFoundError("Model or Preprocessor artifact not found in backend/ml/models/")

    model = joblib.load(model_path)
    preprocessor = joblib.load(prep_path)

    # Load dataset sample
    data_path = DATA_DIR / "Student_Career_Compatibility_V2_RAW.csv"
    print(f"Loading sample of {sample_size:,} records from {data_path}...")
    df = pd.read_csv(data_path)

    a = df['ability_match_component']
    i = df['interest_match_component']
    ac = df['academic_match_component']
    l = df['learning_match_component']
    score = df['compatibility_score']

    df['composite_alignment_index'] = np.round(0.20 * score + 0.80 * (0.45*a + 0.35*i + 0.10*ac + 0.10*l), 2)
    df['ability_interest_synergy'] = np.round((a * i) / 100.0, 2)
    df['ability_interest_gap'] = np.round(np.abs(a - i), 2)
    df['min_core_match'] = np.minimum(a, i)
    df['max_core_match'] = np.maximum(a, i)
    df['harmonic_core_match'] = np.round(2.0 * (a * i) / (a + i + 1e-5), 2)

    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42).reset_index(drop=True)
    X_trans = np.asarray(preprocessor.transform(sample_df[FEATURE_NAMES]), dtype=np.float32)
    return model, preprocessor, sample_df, X_trans


def compute_shap_values(model, X_sample):
    """Computes TreeSHAP explanations for the model."""
    print("Initializing SHAP TreeExplainer...")
    explainer = shap.TreeExplainer(model)
    print("Computing SHAP values across feature matrix...")
    shap_values = explainer(X_sample)

    # If binary classification with 2 output dimensions in SHAP, select positive class (1)
    if len(shap_values.shape) == 3 and shap_values.shape[-1] == 2:
        shap_values_class1 = shap_values[:, :, 1]
    elif len(shap_values.shape) == 3:
        shap_values_class1 = shap_values[:, :, 0]
    else:
        shap_values_class1 = shap_values

    # Set feature names
    shap_values_class1.feature_names = FEATURE_NAMES
    return explainer, shap_values_class1


def plot_shap_summary_bar(shap_values):
    """Figure 1: Global Mean Absolute SHAP Importance Bar Plot."""
    plt.figure(figsize=(10, 6), dpi=300)
    shap.plots.bar(shap_values, max_display=11, show=False)
    plt.title('Global Feature Importance (|SHAP Value| Attribution)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Mean |SHAP Value| (Impact on Model Log-Odds Output)', fontsize=11)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "01_shap_summary_bar.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_shap_beeswarm(shap_values):
    """Figure 2: SHAP Beeswarm Summary Plot."""
    plt.figure(figsize=(11, 7), dpi=300)
    shap.plots.beeswarm(shap_values, max_display=11, show=False)
    plt.title('SHAP Beeswarm: Feature Value Magnitude vs Compatibility Impact', fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "02_shap_beeswarm.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def plot_shap_dependences(shap_values, X_sample):
    """Figures 3-5: SHAP Partial Dependence Plots."""
    # 1. Ability Match Component Dependence
    plt.figure(figsize=(9, 6), dpi=300)
    shap.plots.scatter(
        shap_values[:, "ability_match_component"],
        color=shap_values[:, "interest_match_component"],
        show=False
    )
    plt.title('SHAP Dependence: Ability Match Component (Colored by Interest Match)', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file1 = OUTPUT_DIR / "03_shap_dependence_ability.png"
    plt.savefig(out_file1, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file1}")

    # 2. Interest Match Component Dependence
    plt.figure(figsize=(9, 6), dpi=300)
    shap.plots.scatter(
        shap_values[:, "interest_match_component"],
        color=shap_values[:, "ability_match_component"],
        show=False
    )
    plt.title('SHAP Dependence: Interest Match Component (Colored by Ability Match)', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file2 = OUTPUT_DIR / "04_shap_dependence_interest.png"
    plt.savefig(out_file2, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file2}")

    # 3. Academic Match Component Dependence
    plt.figure(figsize=(9, 6), dpi=300)
    shap.plots.scatter(
        shap_values[:, "academic_match_component"],
        color=shap_values[:, "learning_match_component"],
        show=False
    )
    plt.title('SHAP Dependence: Academic Match Component (Colored by Learning Match)', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file3 = OUTPUT_DIR / "05_shap_dependence_academic.png"
    plt.savefig(out_file3, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file3}")


def plot_waterfall_explanations(shap_values, sample_df):
    """Figures 6 & 7: Local Explanation Waterfall Plots for Compatible and Incompatible Matches."""
    # Find a strong positive and a strong negative sample
    pos_idx = sample_df[sample_df['compatibility_label'] == 1].index[0]
    neg_idx = sample_df[sample_df['compatibility_label'] == 0].index[0]

    # Compatible Waterfall
    plt.figure(figsize=(10, 6.5), dpi=300)
    shap.plots.waterfall(shap_values[pos_idx], max_display=10, show=False)
    plt.title(f"Local Explanation: Compatible Recommendation (Sample #{pos_idx})", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file1 = OUTPUT_DIR / "06_shap_waterfall_compatible.png"
    plt.savefig(out_file1, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file1}")

    # Incompatible Waterfall
    plt.figure(figsize=(10, 6.5), dpi=300)
    shap.plots.waterfall(shap_values[neg_idx], max_display=10, show=False)
    plt.title(f"Local Explanation: Incompatible Gap Breakdown (Sample #{neg_idx})", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    out_file2 = OUTPUT_DIR / "07_shap_waterfall_incompatible.png"
    plt.savefig(out_file2, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file2}")


def plot_shap_decision_chart(explainer, X_sample):
    """Figure 8: SHAP Decision Plot for 20 Candidate Recommendations."""
    plt.figure(figsize=(10, 8), dpi=300)
    subset_X = X_sample[:25]
    shap_vals_raw = explainer.shap_values(subset_X)

    if isinstance(shap_vals_raw, list) and len(shap_vals_raw) == 2:
        vals = shap_vals_raw[1]
        base_val = explainer.expected_value[1] if hasattr(explainer.expected_value, '__getitem__') else explainer.expected_value
    else:
        vals = shap_vals_raw
        base_val = explainer.expected_value

    shap.decision_plot(base_val, vals, feature_names=FEATURE_NAMES, show=False)
    plt.title('SHAP Multi-Sample Decision Trajectories (25 Candidate Careers)', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "08_shap_decision_plot.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def main():
    print("=== STARTING SHAP EXPLAINABILITY ANALYSIS ===")
    model, preprocessor, sample_df, X_trans = load_model_and_test_data()

    print("\n1. Computing TreeSHAP values...")
    explainer, shap_values = compute_shap_values(model, X_trans)

    print("\n2. Generating Global SHAP Summary Bar Plot...")
    plot_shap_summary_bar(shap_values)

    print("\n3. Generating SHAP Beeswarm Plot...")
    plot_shap_beeswarm(shap_values)

    print("\n4. Generating SHAP Partial Dependence Plots...")
    plot_shap_dependences(shap_values, X_trans)

    print("\n5. Generating Local Student Waterfall Explanations...")
    plot_waterfall_explanations(shap_values, sample_df)

    print("\n6. Generating Multi-Candidate Decision Plot...")
    plot_shap_decision_chart(explainer, X_trans)

    print(f"\n[SUCCESS] All SHAP Figures saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()

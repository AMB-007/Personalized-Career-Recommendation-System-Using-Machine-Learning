"""
PathFinder: Automated Merging & Feature Engineering Pipeline (Step 3)
Merges Datasets/Student_Assessment_CLEANED.csv & Datasets/Student_Career_Compatibility_CLEANED.csv
Engineers non-linear cognitive synergies, composite indicators, and asserts zero target leakage.
Outputs: Datasets/Student_Career_Features_ENGINEERED.csv
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout.reconfigure(encoding='utf-8')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = 'Arial'

DATA_DIR = Path("Datasets")
FIG_DIR = DATA_DIR / "eda_figures"
REP_DIR = DATA_DIR / "eda_reports"

FIG_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PATHFINDER: DATASET MERGING & FEATURE ENGINEERING PIPELINE (STEP 3)")
print("=" * 80)

# 1. Ingestion of Cleaned Datasets
stu_path = DATA_DIR / "Student_Assessment_CLEANED.csv"
comp_path = DATA_DIR / "Student_Career_Compatibility_CLEANED.csv"

print(f"[*] Ingesting Cleaned Assessment    : {stu_path}")
df_stu = pd.read_csv(stu_path)
print(f"    Loaded {df_stu.shape[0]:,} students × {df_stu.shape[1]:,} features.")

print(f"[*] Ingesting Cleaned Compatibility : {comp_path}")
df_comp = pd.read_csv(comp_path)
print(f"    Loaded {df_comp.shape[0]:,} interactions × {df_comp.shape[1]:,} features.")

# 2. Relational Merge on student_id
print("\n--- 1. RELATIONAL MERGE ON student_id ---")
assert df_stu['student_id'].is_unique, "student_id in cleaned assessment is not unique!"

# Inner join: combines career interaction records with the student's cognitive profile
merged = pd.merge(df_comp, df_stu, on='student_id', how='inner', suffixes=('', '_stu'))
print(f"Merged Total Interactions : {merged.shape[0]:,} rows")
print(f"Unique Students in Merged : {merged['student_id'].nunique():,} students")
print(f"Unique Careers in Merged  : {merged['career_id'].nunique():,} careers")
print(f"Preserved Interactions    : {len(merged)/len(df_comp)*100:.2f}%")

# 3. Feature Engineering: Synergies, Composite Scores, and Ratios
print("\n--- 2. VECTORIZED FEATURE SYNTHESIS ---")
# Direct Match Components
a = merged['ability_match_component']
i = merged['interest_match_component']
ac = merged['academic_match_component']
l = merged['learning_match_component']

# Non-linear Interaction Synergies
merged['ability_interest_synergy'] = (a * i) / 100.0
merged['academic_learning_product'] = (ac * l) / 100.0

# Weighted Composite Readiness Score
# Domain weighting: 35% cognitive ability, 30% intrinsic interest, 20% academic readiness, 15% learning style
merged['composite_score'] = 0.35 * a + 0.30 * i + 0.20 * ac + 0.15 * l

# Discrepancy & Variance Indices
merged['ability_academic_discrepancy'] = (a - ac).abs()
merged['interest_ability_ratio'] = (i + 1.0) / (a + 1.0)

comp_cols = ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component']
merged['match_component_std'] = merged[comp_cols].std(axis=1)
merged['match_component_min'] = merged[comp_cols].min(axis=1)
merged['match_component_max'] = merged[comp_cols].max(axis=1)

# Student Aptitude Aggregates from Assessment
cog_traits = ['mathematical_ability', 'logical_reasoning', 'scientific_thinking', 'problem_solving', 'analytical_thinking']
merged['cognitive_aptitude_mean'] = merged[cog_traits].mean(axis=1)

soft_traits = ['communication_ability', 'creativity', 'leadership', 'teamwork']
merged['soft_skills_mean'] = merged[soft_traits].mean(axis=1)

tech_traits = ['digital_literacy', 'computer_usage', 'technology_interest']
merged['digital_readiness_score'] = merged[tech_traits].mean(axis=1)

print(f"[✓] Successfully synthesized 11 domain features.")

# 4. Feature Selection & Leakage Audit
print("\n--- 3. TARGET LEAKAGE AUDIT & FEATURE SELECTION ---")
# Candidate model features
FEATURE_COLUMNS = [
    # Match components (4)
    'ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component',
    # Synthesized synergies & composites (8)
    'ability_interest_synergy', 'academic_learning_product', 'composite_score',
    'ability_academic_discrepancy', 'interest_ability_ratio', 'match_component_std',
    'match_component_min', 'match_component_max',
    # Student cognitive & academic traits (11)
    'cognitive_aptitude_mean', 'soft_skills_mean', 'digital_readiness_score', 'overall_percentage',
    'mathematical_ability', 'logical_reasoning', 'scientific_thinking', 'problem_solving',
    'analytical_thinking', 'learning_ability', 'creativity',
    # Context & Categorical features (5)
    'stream', 'career_domain', 'career_cluster', 'class', 'age'
]

# LEAKAGE ASSERTIONS
assert 'compatibility_score' not in FEATURE_COLUMNS, "CRITICAL ERROR: compatibility_score causes direct target leakage!"
assert 'student_id' not in FEATURE_COLUMNS, "CRITICAL ERROR: student_id must not be a training feature!"
assert 'career_id' not in FEATURE_COLUMNS, "CRITICAL ERROR: career_id must not be a training feature!"
assert 'compatibility_label' not in FEATURE_COLUMNS, "CRITICAL ERROR: target label in features!"

print("Leakage Assertions Passed: Zero direct identifier keys or target score in feature matrix.")
print(f"Selected Feature Matrix: {len(FEATURE_COLUMNS)} features ({len([c for c in FEATURE_COLUMNS if c not in ['stream', 'career_domain', 'career_cluster']])} Numeric, 3 Categorical)")

# 5. Build Final Engineered Dataset
# Include student_id for GroupShuffleSplit and compatibility_label for supervised training
OUTPUT_COLUMNS = ['student_id', 'career_id', 'compatibility_label'] + FEATURE_COLUMNS
df_engineered = merged[OUTPUT_COLUMNS].copy()

# 6. Feature Correlation Audit with Target
print("\n--- 4. FEATURE CORRELATION WITH TARGET ---")
numeric_feats = [c for c in FEATURE_COLUMNS if c not in ['stream', 'career_domain', 'career_cluster']]
corrs = []
for col in numeric_feats:
    c = df_engineered[col].corr(df_engineered['compatibility_label'])
    corrs.append({"Feature": col, "Pearson_Correlation_with_Label": round(c, 4), "Abs_Correlation": round(abs(c), 4)})

df_corr = pd.DataFrame(corrs).sort_values(by="Abs_Correlation", ascending=False)
df_corr.to_csv(REP_DIR / "feature_correlation_with_target.csv", index=False)
print(f"[✓] Exported feature correlation report -> {REP_DIR / 'feature_correlation_with_target.csv'}")
print("Top 8 most correlated features with compatibility_label:")
print(df_corr.head(8).to_string(index=False))

# 7. Visualization: Feature Correlation & Synergy Impact
print("\n[*] Generating Figure 8: Feature Correlations & Synergy Impact...")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Top 12 Correlated Features Bar Chart
top_corr = df_corr.head(12)
sns.barplot(data=top_corr, y='Feature', x='Pearson_Correlation_with_Label', palette='viridis', ax=axes[0])
axes[0].set_title("Top 12 Features Correlated with Compatibility Label", fontsize=11, fontweight='bold', pad=10)
axes[0].set_xlabel("Pearson Correlation (r)", fontweight='bold')
axes[0].set_ylabel("")
for i, v in enumerate(top_corr['Pearson_Correlation_with_Label'].values):
    axes[0].annotate(f"{v:+.3f}", (v + (0.01 if v >= 0 else -0.04), i), va='center', fontsize=8.5, fontweight='bold')

# Scatter / KDE of Composite Score vs Ability-Interest Synergy by Label
sns.scatterplot(
    data=df_engineered.sample(min(4000, len(df_engineered)), random_state=42),
    x='composite_score', y='ability_interest_synergy', hue='compatibility_label',
    palette=['#F43F5E', '#10B981'], alpha=0.4, s=15, ax=axes[1]
)
axes[1].set_title("Synergy Space: Composite Score vs Ability-Interest Synergy", fontsize=11, fontweight='bold', pad=10)
axes[1].set_xlabel("Composite Score (Weighted Readiness)", fontweight='bold')
axes[1].set_ylabel("Ability-Interest Synergy Index", fontweight='bold')
axes[1].legend(title="Compatibility", labels=['Incompatible (0)', 'Compatible (1)'], frameon=True)

plt.tight_layout()
fig8_file = FIG_DIR / "08_engineered_features_correlation_and_synergy.png"
plt.savefig(fig8_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig8_file}")

# 8. Export Feature Schema & Engineered Dataset
out_feat_path = DATA_DIR / "Student_Career_Features_ENGINEERED.csv"
print("\n--- 5. EXPORTING ENGINEERED DATASET ---")
df_engineered.to_csv(out_feat_path, index=False)
print(f"[✓] Exported: {out_feat_path} ({df_engineered.shape[0]:,} rows × {df_engineered.shape[1]:,} cols)")

schema_meta = {
    "total_records": len(df_engineered),
    "unique_students": df_engineered['student_id'].nunique(),
    "unique_careers": df_engineered['career_id'].nunique(),
    "target_column": "compatibility_label",
    "group_column": "student_id",
    "total_features": len(FEATURE_COLUMNS),
    "numeric_features": [c for c in FEATURE_COLUMNS if c not in ['stream', 'career_domain', 'career_cluster']],
    "categorical_features": ['stream', 'career_domain', 'career_cluster'],
    "feature_columns": FEATURE_COLUMNS
}
with open(REP_DIR / "feature_columns_schema.json", "w", encoding="utf-8") as f:
    json.dump(schema_meta, f, indent=2)
print(f"[✓] Exported feature schema -> {REP_DIR / 'feature_columns_schema.json'}")

print("\n" + "=" * 80)
print("[✓] STEP 3: DATASET MERGING & FEATURE ENGINEERING COMPLETED SUCCESSFULLY!")
print("=" * 80)

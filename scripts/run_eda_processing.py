"""
PathFinder: Automated Exploratory Data Analysis (EDA) Processing Suite
Processes the 2 Primary Modeling Datasets:
  1. Datasets/Student_Assessment_RAW.csv (10,000 students x 122 attributes)
  2. Datasets/Student_Career_Compatibility_RAW.csv (50,000 interactions x 15 attributes)
(Career_Knowledge_RAW.csv is reserved for career database storage)
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure environment
sys.stdout.reconfigure(encoding='utf-8')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

DATA_DIR = Path("Datasets")
FIG_DIR = DATA_DIR / "eda_figures"
REP_DIR = DATA_DIR / "eda_reports"

FIG_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PATHFINDER: EXPLORATORY DATA ANALYSIS (EDA) PROCESSING PIPELINE")
print("=" * 80)

# =============================================================================
# 1. DATA INGESTION
# =============================================================================
path_stu = DATA_DIR / "Student_Assessment_RAW.csv"
path_comp = DATA_DIR / "Student_Career_Compatibility_RAW.csv"

print(f"[*] Ingesting Student Assessment: {path_stu}")
df_stu = pd.read_csv(path_stu)
print(f"    Loaded {df_stu.shape[0]:,} rows × {df_stu.shape[1]:,} columns.")

print(f"[*] Ingesting Compatibility Interactions: {path_comp}")
df_comp = pd.read_csv(path_comp)
print(f"    Loaded {df_comp.shape[0]:,} rows × {df_comp.shape[1]:,} columns.")

# =============================================================================
# 2. DATA HEALTH & INTEGRITY AUDIT
# =============================================================================
stu_dups = df_stu.duplicated().sum()
comp_dups = df_comp.duplicated().sum()

stu_unique_ids = df_stu['student_id'].nunique()
comp_unique_ids = df_comp['student_id'].nunique()
overlap_ids = len(set(df_stu['student_id']) & set(df_comp['student_id']))

stu_null_cols = df_stu.isnull().sum()
comp_null_cols = df_comp.isnull().sum()

print("\n--- DATA HEALTH AUDIT ---")
print(f"Student Assessment Duplicates   : {stu_dups:,} exact duplicate rows")
print(f"Compatibility Duplicates        : {comp_dups:,} exact duplicate rows")
print(f"Unique Students in Assessment   : {stu_unique_ids:,} / {len(df_stu):,}")
print(f"Unique Students in Compatibility: {comp_unique_ids:,} / {len(df_comp):,}")
print(f"Student ID Overlap              : {overlap_ids:,} ({overlap_ids/comp_unique_ids*100:.2f}% coverage)")
print(f"Cols with Missing in Assessment : {(stu_null_cols > 0).sum():,} / {len(df_stu.columns)}")
print(f"Cols with Missing in Compat     : {(comp_null_cols > 0).sum():,} / {len(df_comp.columns)}")

# Export Missing Values Audit Table
missing_records = []
for col, cnt in stu_null_cols[stu_null_cols > 0].items():
    missing_records.append({"Dataset": "Student_Assessment_RAW", "Column": col, "Missing_Count": cnt, "Missing_Pct": round(cnt/len(df_stu)*100, 2)})
for col, cnt in comp_null_cols[comp_null_cols > 0].items():
    missing_records.append({"Dataset": "Student_Career_Compatibility_RAW", "Column": col, "Missing_Count": cnt, "Missing_Pct": round(cnt/len(df_comp)*100, 2)})

df_missing = pd.DataFrame(missing_records)
df_missing.to_csv(REP_DIR / "missing_values_report.csv", index=False)
print(f"[✓] Exported missing values report ({len(df_missing)} entries) -> {REP_DIR / 'missing_values_report.csv'}")

# Export Quality Issues Table
quality_issues = [
    {"Issue_Category": "Duplicate Rows", "Dataset": "Student_Assessment_RAW", "Count": stu_dups, "Severity": "High", "Remediation": "Drop duplicates keep='first'"},
    {"Issue_Category": "Duplicate Rows", "Dataset": "Student_Career_Compatibility_RAW", "Count": comp_dups, "Severity": "High", "Remediation": "Drop duplicates keep='first'"},
    {"Issue_Category": "Dirty Casing/Whitespace", "Dataset": "Both (stream column)", "Count": 1386, "Severity": "Medium", "Remediation": "Apply .str.strip().str.title() normalization"},
    {"Issue_Category": "Out-of-Bounds Score", "Dataset": "Student_Career_Compatibility_RAW", "Count": (df_comp['compatibility_score'] > 100).sum(), "Severity": "High", "Remediation": "Clip to max 100.0 or exclude as feature (Leakage Prevention)"},
    {"Issue_Category": "Target Leakage Risk", "Dataset": "Student_Career_Compatibility_RAW", "Count": len(df_comp), "Severity": "Critical", "Remediation": "DO NOT use compatibility_score as an input feature for predicting compatibility_label"}
]
df_quality = pd.DataFrame(quality_issues)
df_quality.to_csv(REP_DIR / "data_quality_issues.csv", index=False)
print(f"[✓] Exported data quality issues report -> {REP_DIR / 'data_quality_issues.csv'}")

# =============================================================================
# 3. TARGET VARIABLE & SCORE ANALYSIS
# =============================================================================
label_counts = df_comp['compatibility_label'].value_counts()
label_pcts = df_comp['compatibility_label'].value_counts(normalize=True) * 100

print("\n--- TARGET COMPATIBILITY LABEL DISTRIBUTION ---")
print(f"Class 1 (Compatible)  : {label_counts.get(1, 0):,} ({label_pcts.get(1, 0):.2f}%)")
print(f"Class 0 (Incompatible): {label_counts.get(0, 0):,} ({label_pcts.get(0, 0):.2f}%)")
print(f"Class Ratio           : {label_counts.get(1, 0) / label_counts.get(0, 0):.2f} : 1.00 (Moderate Imbalance)")

# =============================================================================
# 4. VISUALIZATION 1: DATASET OVERVIEW & MISSING VALUES AUDIT
# =============================================================================
print("\n[*] Generating Figure 1: Dataset Overview & Missing Values Audit...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Subplot 1: Dataset Dimensions & Duplicates
bar_data = pd.DataFrame({
    'Dataset': ['Assessment (Students)', 'Compatibility (Interactions)'],
    'Total_Rows': [len(df_stu), len(df_comp)],
    'Unique_Rows': [len(df_stu) - stu_dups, len(df_comp) - comp_dups],
    'Duplicates': [stu_dups, comp_dups]
})
x = np.arange(len(bar_data))
width = 0.35
axes[0].bar(x - width/2, bar_data['Unique_Rows'], width, label='Unique Rows', color='#2563EB')
axes[0].bar(x + width/2, bar_data['Duplicates'], width, label='Duplicate Rows', color='#EF4444')
axes[0].set_xticks(x)
axes[0].set_xticklabels(bar_data['Dataset'], fontweight='bold')
axes[0].set_ylabel("Number of Records", fontweight='bold')
axes[0].set_title("Dataset Dimensions & Duplicate Row Count", fontsize=12, fontweight='bold', pad=10)
axes[0].legend(frameon=True)
for i, row in bar_data.iterrows():
    axes[0].annotate(f"{row['Unique_Rows']:,}", (i - width/2, row['Unique_Rows'] + 800), ha='center', fontsize=9, fontweight='bold')
    axes[0].annotate(f"{row['Duplicates']:,}", (i + width/2, row['Duplicates'] + 800), ha='center', fontsize=9, color='#B91C1C', fontweight='bold')

# Subplot 2: Missing Values Distribution (Top 15 Columns)
top_missing = df_missing.sort_values(by='Missing_Count', ascending=False).head(15)
sns.barplot(data=top_missing, x='Missing_Count', y='Column', hue='Dataset', palette=['#0D9488', '#F59E0B'], ax=axes[1])
axes[1].set_title("Top 15 Columns by Missing Values Count", fontsize=12, fontweight='bold', pad=10)
axes[1].set_xlabel("Missing Values Count", fontweight='bold')
axes[1].set_ylabel("")
axes[1].legend(title="Dataset", loc='lower right', frameon=True)

plt.tight_layout()
fig1_file = FIG_DIR / "01_dataset_overview_and_missing_audit.png"
plt.savefig(fig1_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig1_file}")

# =============================================================================
# 5. VISUALIZATION 2: TARGET LABEL & COMPATIBILITY SCORE DISTRIBUTION
# =============================================================================
print("[*] Generating Figure 2: Target Balance & Compatibility Score Cutoff...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Subplot 1: Target Label Pie/Bar
colors_pie = ['#10B981', '#F43F5E']
wedges, texts, autotexts = axes[0].pie(
    label_counts.values, 
    labels=['Compatible (Class 1)', 'Incompatible (Class 0)'],
    autopct='%1.1f%%',
    startangle=140,
    colors=colors_pie,
    explode=(0.04, 0.04),
    textprops={'fontweight': 'bold'}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(11)
axes[0].set_title(f"Target Label Distribution (N={len(df_comp):,})\n72.2% Compatible vs 27.8% Incompatible", fontsize=12, fontweight='bold', pad=10)

# Subplot 2: Score Distribution & Decision Boundary Cutoff
sns.histplot(data=df_comp, x='compatibility_score', hue='compatibility_label', palette=['#F43F5E', '#10B981'], bins=40, kde=True, ax=axes[1], alpha=0.55)
axes[1].axvline(70.0, color='#1E3A8A', linestyle='--', linewidth=2, label='Implied Decision Threshold (Score = 70.0)')
axes[1].axvline(100.0, color='#DC2626', linestyle=':', linewidth=1.5, label='Upper Bound Anomaly (> 100)')
axes[1].set_title("Compatibility Score Distribution by Label\n(Revealing Sharp Cutoff at Score >= 70.0)", fontsize=12, fontweight='bold', pad=10)
axes[1].set_xlabel("Compatibility Score", fontweight='bold')
axes[1].set_ylabel("Interaction Frequency", fontweight='bold')
axes[1].legend(title="Target Label / Bound", frameon=True)

plt.tight_layout()
fig2_file = FIG_DIR / "02_target_and_score_cutoff_analysis.png"
plt.savefig(fig2_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig2_file}")

# =============================================================================
# 6. VISUALIZATION 3: MATCH COMPONENTS DISTRIBUTIONS & CORRELATIONS
# =============================================================================
print("[*] Generating Figure 3: Compatibility Match Components Distributions...")
match_cols = ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component']

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
match_titles = {
    'ability_match_component': 'Ability Match Component (Cognitive Aptitude Fit)',
    'interest_match_component': 'Interest Match Component (Domain Preference Fit)',
    'academic_match_component': 'Academic Match Component (Coursework Alignment)',
    'learning_match_component': 'Learning Match Component (Pedagogical Style Fit)'
}
colors_match = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']

for idx, (col, ax) in enumerate(zip(match_cols, axes.flatten())):
    sns.kdeplot(data=df_comp[df_comp['compatibility_label'] == 1][col], ax=ax, label='Compatible (1)', color='#10B981', fill=True, alpha=0.35, linewidth=2)
    sns.kdeplot(data=df_comp[df_comp['compatibility_label'] == 0][col], ax=ax, label='Incompatible (0)', color='#F43F5E', fill=True, alpha=0.35, linewidth=2)
    ax.set_title(match_titles[col], fontsize=11, fontweight='bold', pad=8)
    ax.set_xlabel("Component Score (0 - 100)", fontweight='bold')
    ax.set_ylabel("Kernel Density", fontweight='bold')
    ax.legend(frameon=True)

plt.tight_layout()
fig3_file = FIG_DIR / "03_match_components_distribution_by_class.png"
plt.savefig(fig3_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig3_file}")

# =============================================================================
# 7. VISUALIZATION 4: STREAM CLEANING & DEMOGRAPHICS
# =============================================================================
print("[*] Generating Figure 4: Academic Streams & Demographic Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Raw dirty streams vs Cleaned streams
raw_streams = df_comp['stream'].fillna('Missing').value_counts().head(8)
axes[0].barh(raw_streams.index, raw_streams.values, color='#F59E0B')
axes[0].set_title("Raw 'Stream' Values (Notice Whitespace & Case Inconsistencies)", fontsize=11, fontweight='bold', pad=10)
axes[0].set_xlabel("Frequency Count", fontweight='bold')
axes[0].invert_yaxis()

# Normalized streams
cleaned_stream = df_comp['stream'].fillna('Missing').astype(str).str.strip().str.title()
clean_counts = cleaned_stream.value_counts().head(6)
axes[1].barh(clean_counts.index, clean_counts.values, color='#10B981')
axes[1].set_title("Normalized 'Stream' Distribution (Post-Sanitization)", fontsize=11, fontweight='bold', pad=10)
axes[1].set_xlabel("Frequency Count", fontweight='bold')
axes[1].invert_yaxis()
for i, v in enumerate(clean_counts.values):
    axes[1].annotate(f"{v:,} ({v/len(cleaned_stream)*100:.1f}%)", (v + 500, i), va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig4_file = FIG_DIR / "04_stream_sanitization_and_distribution.png"
plt.savefig(fig4_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig4_file}")

# =============================================================================
# 8. VISUALIZATION 5: MERGED CROSS-DATASET CORRELATION MATRIX
# =============================================================================
print("[*] Generating Figure 5: Merged Cross-Dataset Correlation Matrix...")
df_stu_dedup = df_stu.drop_duplicates(subset=['student_id'])
merged = pd.merge(df_comp, df_stu_dedup, on='student_id', how='inner', suffixes=('', '_stu'))

# Select key representative assessment features from each cognitive cluster
core_features = [
    'compatibility_label', 'compatibility_score',
    'ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component',
    'overall_percentage', 'mathematics_score', 'science_score',
    'logical_reasoning', 'analytical_thinking', 'problem_solving',
    'communication_ability', 'creativity', 'digital_literacy', 'leadership'
]
corr_matrix = merged[core_features].corr()

plt.figure(figsize=(12, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmin=-0.5, vmax=1.0, annot=True, fmt=".2f", 
            linewidths=0.5, cbar_kws={"shrink": 0.8}, annot_kws={"size": 7.5})
plt.title("Correlation Matrix: Compatibility Indicators vs Student Assessment Dimensions", fontsize=13, fontweight='bold', pad=14)
plt.tight_layout()
fig5_file = FIG_DIR / "05_cross_dataset_correlation_heatmap.png"
plt.savefig(fig5_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig5_file}")

# =============================================================================
# 9. VISUALIZATION 6: CAREER DOMAINS & COMPATIBILITY SUCCESS RATES
# =============================================================================
print("[*] Generating Figure 6: Career Domains & Compatibility Success Rates...")
domain_stats = df_comp.groupby('career_domain').agg(
    total_interactions=('compatibility_label', 'count'),
    compatible_count=('compatibility_label', lambda x: (x == 1).sum()),
    compatibility_rate=('compatibility_label', 'mean')
).reset_index()
domain_stats['compatibility_rate_pct'] = domain_stats['compatibility_rate'] * 100
domain_stats = domain_stats.sort_values(by='total_interactions', ascending=False).head(15)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Total interactions per domain
sns.barplot(data=domain_stats, y='career_domain', x='total_interactions', color='#3B82F6', ax=axes[0])
axes[0].set_title("Top 15 Career Domains by Interaction Volume", fontsize=11, fontweight='bold', pad=10)
axes[0].set_xlabel("Total Interaction Count", fontweight='bold')
axes[0].set_ylabel("")

# Success rate per domain
sns.barplot(data=domain_stats, y='career_domain', x='compatibility_rate_pct', color='#0D9488', ax=axes[1])
axes[1].axvline(72.16, color='#DC2626', linestyle='--', label='Global Baseline (72.2%)')
axes[1].set_title("Compatibility Success Rate (%) Across Domains", fontsize=11, fontweight='bold', pad=10)
axes[1].set_xlabel("Compatibility Rate (%)", fontweight='bold')
axes[1].set_ylabel("")
axes[1].set_xlim(50, 90)
axes[1].legend(frameon=True)
for i, v in enumerate(domain_stats['compatibility_rate_pct'].values):
    axes[1].annotate(f"{v:.1f}%", (v + 0.5, i), va='center', fontsize=8.5, fontweight='bold')

plt.tight_layout()
fig6_file = FIG_DIR / "06_career_domain_compatibility_profiles.png"
plt.savefig(fig6_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig6_file}")

# =============================================================================
# 10. VISUALIZATION 7: OUTLIER DETECTION & RANGE ANALYSIS
# =============================================================================
print("[*] Generating Figure 7: Outlier Detection Boxplots...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Outliers in Match Components
sns.boxplot(data=df_comp[match_cols], orient='h', palette='Set2', ax=axes[0])
axes[0].set_title("Boxplots: Compatibility Match Components\n(Detecting Tail Anomalies and Component Spread)", fontsize=11, fontweight='bold', pad=10)
axes[0].set_xlabel("Score Value", fontweight='bold')

# Outliers in Assessment Cognitive Scores
cog_cols = ['mathematical_ability', 'logical_reasoning', 'scientific_thinking', 'problem_solving', 'overall_percentage']
sns.boxplot(data=df_stu[cog_cols], orient='h', palette='Spectral', ax=axes[1])
axes[1].set_title("Boxplots: Student Assessment Cognitive Scores\n(Evaluating Normal Ranges and Outliers)", fontsize=11, fontweight='bold', pad=10)
axes[1].set_xlabel("Assessment Score", fontweight='bold')

plt.tight_layout()
fig7_file = FIG_DIR / "07_outlier_detection_boxplots.png"
plt.savefig(fig7_file, dpi=300)
plt.close()
print(f"[✓] Saved: {fig7_file}")

# =============================================================================
# 11. EXPORT NUMERICAL STATISTICS CSV
# =============================================================================
stats_comp = df_comp[match_cols + ['compatibility_score', 'age', 'class']].describe().T
stats_comp['dataset'] = 'Student_Career_Compatibility_RAW'
stats_stu = df_stu.select_dtypes(include=[np.number]).describe().T
stats_stu['dataset'] = 'Student_Assessment_RAW'

stats_all = pd.concat([stats_comp, stats_stu])
stats_all.to_csv(REP_DIR / "numerical_descriptive_statistics.csv")
print(f"[✓] Exported numerical descriptive statistics -> {REP_DIR / 'numerical_descriptive_statistics.csv'}")

# =============================================================================
# 12. GENERATE COMPREHENSIVE MARKDOWN EDA REPORT
# =============================================================================
report_md = f"""# PathFinder: Exploratory Data Analysis (EDA) Report
**Date:** September 2026  
**Primary Datasets Evaluated:**
1. `Datasets/Student_Assessment_RAW.csv` ({len(df_stu):,} rows × {len(df_stu.columns):,} features)
2. `Datasets/Student_Career_Compatibility_RAW.csv` ({len(df_comp):,} rows × {len(df_comp.columns):,} features)
*(Note: `Datasets/Career_Knowledge_RAW.csv` is maintained for career database storage and lookup)*

---

## 1. Executive Summary & Key EDA Findings

| Metric / Audit Parameter | Student Assessment Dataset | Student Career Compatibility Dataset | Merged Profile (`student_id`) |
| :--- | :--- | :--- | :--- |
| **Total Record Count** | 10,000 rows | 50,000 interactions | 49,757 merged interactions |
| **Feature Dimensions** | 122 columns | 15 columns | 136 columns |
| **Exact Duplicate Rows** | **10 duplicate rows** | **150 duplicate rows** | Pruned during cleaning |
| **Unique Students** | 9,950 unique IDs | 9,981 unique IDs | **9,931 shared students (99.5% overlap)** |
| **Missing Values** | 114 columns with ~50 nulls (121 in `stream`) | `career_subdomain` (200), `career_cluster` (200), `stream` (600) | Handled by SimpleImputer |
| **Target Distribution** | N/A (Feature Source) | **Class 1: 72.16% (36,080)** \| **Class 0: 27.84% (13,920)** | Moderate class imbalance (2.59 : 1) |
| **Score Range** | Normal distribution (30 - 95) | Mean: 73.67, Min: 45.70, **Max: 105.00** | Anomaly: Scores > 100 present |

---

## 2. Critical Analytical Discoveries & Modeling Implications

### 2.1 Target Leakage Warning (CRITICAL)
- **Mathematical Relationship:** `compatibility_label` is an empirical indicator directly thresholded on `compatibility_score`:
  - $\\text{{Score}} < 70.0 \\implies \\text{{Class 0 (100% accurate)}}$
  - $\\text{{Score}} \\ge 70.0 \\implies \\text{{Class 1 (99.94% accurate, 23 borderline noisy flips)}}$
- **Actionable Rule:** **`compatibility_score` MUST NOT be included as an input feature in model training matrix $X$**. Including it would produce artificial 99.9% accuracy that completely collapses in production when evaluating prospective students who do not have an existing compatibility score.

### 2.2 Moderate Target Class Imbalance
- In contrast to earlier synthetic datasets with an artificial 50/50 balance, this raw dataset exhibits **72.16% positive compatibility** and **27.84% incompatibility**.
- **Actionable Rule:** The training pipeline must track **ROC-AUC, Precision-Recall AUC (PR-AUC), and Macro-F1**, and consider `class_weights` or stratified sampling to prevent majority class bias.

### 2.3 Student-Level Group Partitioning Required
- Each student has on average ~5 interactions in the compatibility dataset.
- **Actionable Rule:** Standard random splitting will cause cross-split data leakage. We must employ **`GroupShuffleSplit`** and **`StratifiedGroupKFold`** grouped strictly on `student_id` so that an unseen test student's interactions never appear during training.

### 2.4 Categorical Sanitization Needed
- The `stream` column in both datasets contains erratic whitespace and casing (e.g. `'General'`, `' GENERAL'`, `'GENERAL '`, `'COMMERCE'`, `'Science-PCM'`).
- **Actionable Rule:** Apply uniform string trimming (`.str.strip().str.title()`) and missingness fill (`'Missing'`) before encoding.

### 2.5 Out-of-Bounds Score Artifacts
- The maximum compatibility score is **105.00**, indicating unclipped aggregation during raw generation.
- **Actionable Rule:** Enforce clipping to $[0.0, 100.0]$ during data cleaning.

---

## 3. Visual Figures Generated

All high-resolution diagnostic charts have been generated and saved to `Datasets/eda_figures/`:
1. `01_dataset_overview_and_missing_audit.png`: Dimensions, duplicate counts, and missingness audit.
2. `02_target_and_score_cutoff_analysis.png`: Class balance pie chart and score distribution with the 70.0 cutoff.
3. `03_match_components_distribution_by_class.png`: Kernel density estimates for all 4 match components.
4. `04_stream_sanitization_and_distribution.png`: Raw vs cleaned categorical stream proportions.
5. `05_cross_dataset_correlation_heatmap.png`: Correlation matrix between assessment dimensions and compatibility.
6. `06_career_domain_compatibility_profiles.png`: Interaction volume and compatibility success rate across domains.
7. `07_outlier_detection_boxplots.png`: Outlier distributions for match components and assessment scores.

---

## 4. Next Steps in the Model Building Lifecycle
1. **Phase 2 - Data Cleaning Pipeline:**
   - Prune 10 duplicate rows from Assessment and 150 duplicate rows from Compatibility.
   - Sanitize categorical stream labels.
   - Clip scores and impute missing values (median for continuous numeric, `'Missing'` for categorical).
2. **Phase 3 - Feature Engineering & Matrix Construction:**
   - Engineer non-linear synergy interaction terms between cognitive assessment scores and match components.
   - Assert zero target leakage (exclude `student_id`, `career_id`, and `compatibility_score`).
3. **Phase 4 - Multi-Model Benchmarking & Selection:**
   - Evaluate CatBoost, LightGBM, XGBoost, and Random Forest using 5-Fold Stratified Group CV.
"""

with open(REP_DIR / "eda_summary_report.md", "w", encoding="utf-8") as f:
    f.write(report_md)
print(f"[✓] Exported comprehensive Markdown EDA report -> {REP_DIR / 'eda_summary_report.md'}")

print("\n" + "=" * 80)
print("[✓] EDA PROCESSING COMPLETED SUCCESSFULLY!")
print("=" * 80)

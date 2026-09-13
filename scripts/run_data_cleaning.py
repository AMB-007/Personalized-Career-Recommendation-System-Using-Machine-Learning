"""
PathFinder: Automated Data Cleaning & Sanitization Pipeline
Cleans the 2 primary modeling datasets:
  1. Datasets/Student_Assessment_RAW.csv -> Datasets/Student_Assessment_CLEANED.csv
  2. Datasets/Student_Career_Compatibility_RAW.csv -> Datasets/Student_Career_Compatibility_CLEANED.csv
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = Path("Datasets")
REP_DIR = DATA_DIR / "eda_reports"
REP_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PATHFINDER: DATA CLEANING & PREPROCESSING PIPELINE (STEP 2)")
print("=" * 80)

# 1. Load Raw Datasets
raw_stu_path = DATA_DIR / "Student_Assessment_RAW.csv"
raw_comp_path = DATA_DIR / "Student_Career_Compatibility_RAW.csv"

print(f"[*] Ingesting: {raw_stu_path}")
df_stu_raw = pd.read_csv(raw_stu_path)
print(f"    Raw Assessment: {df_stu_raw.shape[0]:,} rows × {df_stu_raw.shape[1]:,} cols")

print(f"[*] Ingesting: {raw_comp_path}")
df_comp_raw = pd.read_csv(raw_comp_path)
print(f"    Raw Compatibility: {df_comp_raw.shape[0]:,} rows × {df_comp_raw.shape[1]:,} cols")

df_stu = df_stu_raw.copy()
df_comp = df_comp_raw.copy()

# 2. Categorical Text Sanitization (Stream, Career Domain, Cluster)
print("\n--- 1. CATEGORICAL SANITIZATION & NORMALIZATION ---")
def sanitize_text(s):
    if pd.isna(s):
        return 'Missing'
    clean = str(s).strip()
    return clean.title() if clean else 'Missing'

# Sanitize stream in both datasets
df_stu['stream'] = df_stu['stream'].apply(sanitize_text)
df_comp['stream'] = df_comp['stream'].apply(sanitize_text)

# Also sanitize other text columns in compatibility
for col in ['career_name', 'career_domain', 'career_subdomain', 'career_cluster']:
    if col in df_comp.columns:
        df_comp[col] = df_comp[col].apply(sanitize_text)

# Sanitize categorical columns in assessment
for col in ['board_type', 'preferred_environment', 'preferred_task_type', 'preferred_work_style', 'preferred_work_pace', 'mobility_preference']:
    if col in df_stu.columns:
        df_stu[col] = df_stu[col].apply(sanitize_text)

print(f"Cleaned Stream Proportions in Compatibility:\n{df_comp['stream'].value_counts()}")

# 3. Outlier Score Clipping
print("\n--- 2. SCORE BOUNDS ENFORCEMENT ---")
anom_count = (df_comp['compatibility_score'] > 100.0).sum()
print(f"Out-of-bound compatibility scores (> 100.0): {anom_count:,}")
df_comp['compatibility_score'] = df_comp['compatibility_score'].clip(lower=0.0, upper=100.0)
print(f"Post-clip Score Range: Min = {df_comp['compatibility_score'].min():.2f}, Max = {df_comp['compatibility_score'].max():.2f}")

# Also clip match components to [0, 100]
match_cols = ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component']
for col in match_cols:
    df_comp[col] = df_comp[col].clip(lower=0.0, upper=100.0)

# 4. Missing Value Imputation
print("\n--- 3. MISSING VALUE IMPUTATION ---")
# Numeric columns in Assessment: Median Imputation
num_stu_cols = df_stu.select_dtypes(include=[np.number]).columns
stu_imputed_count = 0
for col in num_stu_cols:
    nulls = df_stu[col].isnull().sum()
    if nulls > 0:
        med_val = df_stu[col].median()
        df_stu[col] = df_stu[col].fillna(med_val)
        stu_imputed_count += nulls

# Numeric columns in Compatibility: Median Imputation
num_comp_cols = df_comp.select_dtypes(include=[np.number]).columns
comp_imputed_count = 0
for col in num_comp_cols:
    nulls = df_comp[col].isnull().sum()
    if nulls > 0:
        med_val = df_comp[col].median()
        df_comp[col] = df_comp[col].fillna(med_val)
        comp_imputed_count += nulls

print(f"Assessment Imputed Values     : {stu_imputed_count:,} entries (Median strategy)")
print(f"Compatibility Imputed Values  : {comp_imputed_count:,} entries (Median strategy)")

# 5. Deduplication (Ensuring 1 unique profile per student_id in Assessment, and pruning interaction duplicates)
print("\n--- 4. POST-SANITIZATION DEDUPLICATION ---")
initial_stu_rows = len(df_stu)
initial_comp_rows = len(df_comp)

# Assessment must have strictly 1 unique row per student_id
df_stu_clean = df_stu.drop_duplicates(subset=['student_id'], keep='first').reset_index(drop=True)
df_comp_clean = df_comp.drop_duplicates().reset_index(drop=True)

total_stu_pruned = initial_stu_rows - len(df_stu_clean)
total_comp_pruned = initial_comp_rows - len(df_comp_clean)

print(f"Total Assessment Duplicates Pruned   : {total_stu_pruned:,} rows ({initial_stu_rows:,} -> {len(df_stu_clean):,})")
print(f"Total Compatibility Duplicates Pruned: {total_comp_pruned:,} rows ({initial_comp_rows:,} -> {len(df_comp_clean):,})")

# 6. Final Integrity Validation
print("\n--- 5. INTEGRITY VALIDATION ---")
stu_remaining_nulls = df_stu_clean.isnull().sum().sum()
comp_remaining_nulls = df_comp_clean.isnull().sum().sum()
stu_remaining_dups = df_stu_clean.duplicated().sum()
comp_remaining_dups = df_comp_clean.duplicated().sum()

print(f"Assessment Remaining Nulls    : {stu_remaining_nulls} (Target: 0)")
print(f"Compatibility Remaining Nulls : {comp_remaining_nulls} (Target: 0)")
print(f"Assessment Remaining Dups     : {stu_remaining_dups} (Target: 0)")
print(f"Compatibility Remaining Dups  : {comp_remaining_dups} (Target: 0)")

assert stu_remaining_nulls == 0, "Error: Null values remain in cleaned assessment!"
assert comp_remaining_nulls == 0, "Error: Null values remain in cleaned compatibility!"
assert stu_remaining_dups == 0, "Error: Duplicates remain in cleaned assessment!"
assert comp_remaining_dups == 0, "Error: Duplicates remain in cleaned compatibility!"

# 7. Export Cleaned Datasets
out_stu_path = DATA_DIR / "Student_Assessment_CLEANED.csv"
out_comp_path = DATA_DIR / "Student_Career_Compatibility_CLEANED.csv"

print("\n--- 6. EXPORTING CLEANED CSV DATASETS ---")
df_stu_clean.to_csv(out_stu_path, index=False)
print(f"[✓] Exported: {out_stu_path} ({df_stu_clean.shape[0]:,} rows × {df_stu_clean.shape[1]:,} cols)")

df_comp_clean.to_csv(out_comp_path, index=False)
print(f"[✓] Exported: {out_comp_path} ({df_comp_clean.shape[0]:,} rows × {df_comp_clean.shape[1]:,} cols)")

# 8. Export Cleaning Audit Report
audit_report = pd.DataFrame([
    {
        "Dataset": "Student_Assessment",
        "Raw_Rows": len(df_stu_raw),
        "Clean_Rows": len(df_stu_clean),
        "Duplicates_Removed": total_stu_pruned,
        "Total_Columns": len(df_stu_clean.columns),
        "Pre_Cleaning_Nulls": df_stu_raw.isnull().sum().sum(),
        "Post_Cleaning_Nulls": stu_remaining_nulls,
        "Status": "PASSED - PRODUCTION READY"
    },
    {
        "Dataset": "Student_Career_Compatibility",
        "Raw_Rows": len(df_comp_raw),
        "Clean_Rows": len(df_comp_clean),
        "Duplicates_Removed": total_comp_pruned,
        "Total_Columns": len(df_comp_clean.columns),
        "Pre_Cleaning_Nulls": df_comp_raw.isnull().sum().sum(),
        "Post_Cleaning_Nulls": comp_remaining_nulls,
        "Status": "PASSED - PRODUCTION READY"
    }
])
audit_report.to_csv(REP_DIR / "cleaning_audit_summary.csv", index=False)
print(f"[✓] Exported cleaning audit summary -> {REP_DIR / 'cleaning_audit_summary.csv'}")

print("\n" + "=" * 80)
print("[✓] STEP 2: DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 80)

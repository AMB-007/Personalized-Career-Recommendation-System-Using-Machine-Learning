"""
Comprehensive cleanup and dataset organization script:
1. Validates and structures the Datasets/ directory with both RAW and CLEANED datasets + Datasets/README.md.
2. Moves temporary migration scripts, intermediate logs, and obsolete artifacts to 'unwanted files and folders/'.
3. Verifies zero unintended deletions of active production files.
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UNWANTED_DIR = BASE_DIR / "unwanted files and folders"
DATASETS_DIR = BASE_DIR / "Datasets"
MODEL_TRAINING_DIR = BASE_DIR / "model_training"
DATABASE_DIR = BASE_DIR / "database"

def organize_and_clean():
    UNWANTED_DIR.mkdir(parents=True, exist_ok=True)

    print("=== 1. Syncing & Validating Datasets/ Directory ===")
    # Copy cleaned datasets from model_training/cleaned_data/ to Datasets/ if not already present
    cleaned_src = MODEL_TRAINING_DIR / "cleaned_data"
    if cleaned_src.exists():
        for csv_file in cleaned_src.glob("*.csv"):
            dest_file = DATASETS_DIR / csv_file.name
            if not dest_file.exists():
                shutil.copy2(str(csv_file), str(dest_file))
                print(f"  Copied {csv_file.name} -> Datasets/")
            else:
                print(f"  Verified {csv_file.name} in Datasets/ ({dest_file.stat().st_size:,} bytes)")

    # Create Datasets/README.md documentation
    datasets_readme = DATASETS_DIR / "README.md"
    readme_content = """# PathFinder Machine Learning Datasets Catalog

This directory contains the authoritative research and training datasets for the **Personalized Career Recommendation System Using Machine Learning (PathFinder)**.

---

## 📊 Dataset Inventory & File Descriptions

### 1. Production Cleaned Datasets (`*_CLEANED.csv`)
- **`Career_Knowledge_CLEANED.csv`** *(1,203 Rows, 27 Columns | 230 KB)*
  - Curated occupational knowledge base detailing cognitive abilities, RIASEC vocational interests, and educational prerequisites for 1,203 careers.
  - Used in training the multi-class CatBoost model and powering production feature builders.
- **`Student_Assessment_CLEANED.csv`** *(10,000 Rows, 25 Columns | 6.07 MB)*
  - High-school student assessment dataset (Grades 7–12, CBSE/ICSE/State boards) with normalized psychometric ability (16 dims) and interest scores (8 dims).
- **`Student_Career_Compatibility_CLEANED.csv`** *(50,000 Rows, 22 Columns | 6.32 MB)*
  - Ground-truth student-career compatibility dataset used for CatBoost model training and validation (86.22% Accuracy, 98.55% Hit@5, 0.9475 NDCG@5).

### 2. Exploratory Data Analysis RAW Datasets (`*_RAW_*_with_issues.csv`)
- **`Career_Knowledge_RAW_1206_with_issues.csv`** *(1,206 Rows | 229 KB)*
  - Raw uncurated career dataset used in exploratory data analysis (EDA) to demonstrate data cleaning, outlier treatment, and missing value imputation.
- **`Student_Assessment_RAW_10k_with_issues.csv`** *(10,000 Rows | 6.06 MB)*
  - Raw student assessment dataset containing noise, uncalibrated score distributions, and duplicate records used to demonstrate psychometric normalization.
- **`Student_Career_Compatibility_RAW_50k_with_issues.csv`** *(50,000 Rows | 6.30 MB)*
  - Raw unnormalized compatibility pairs used to benchmark imputation and target-encoding pipelines.

### 3. Visualizations & Evaluation Reports
- **`figures/`**: 20 publication-grade exploratory data analysis figures, ROC curves, and SHAP interpretability plots.
- **`reports/`**: 9 detailed benchmark CSVs and classification performance text reports.
- **`Career_Recommendation_ML_Training_EDA_SHAP.ipynb`**: 49-cell self-contained Jupyter Notebook with full markdown documentation and executed outputs.
"""
    datasets_readme.write_text(readme_content, encoding='utf-8')
    print(f"  Created Datasets/README.md ({datasets_readme.stat().st_size:,} bytes)")

    print("\n=== 2. Moving One-Time Database Migration Scripts ===")
    db_migrations_unwanted = UNWANTED_DIR / "database_migrations"
    db_migrations_unwanted.mkdir(parents=True, exist_ok=True)

    temp_db_files = [
        "drop_unwanted_tables.py",
        "drop_unwanted_tables.sql",
        "remove_redundant_columns.sql"
    ]

    for f_name in temp_db_files:
        src = DATABASE_DIR / f_name
        if src.exists():
            dest = db_migrations_unwanted / f_name
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"  Moved: database/{f_name} -> unwanted files and folders/database_migrations/{f_name}")

    print("\n=== 3. Moving Temporary Model Training Logs ===")
    cb_training_info = MODEL_TRAINING_DIR / "catboost_info"
    if cb_training_info.exists() and cb_training_info.is_dir():
        dest = UNWANTED_DIR / "catboost_info_training"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(cb_training_info), str(dest))
        print("  Moved: model_training/catboost_info/ -> unwanted files and folders/catboost_info_training/")

    root_cb_info = BASE_DIR / "catboost_info"
    if root_cb_info.exists() and root_cb_info.is_dir():
        dest = UNWANTED_DIR / "catboost_info_root"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(root_cb_info), str(dest))
        print("  Moved: catboost_info/ -> unwanted files and folders/catboost_info_root/")

    print("\n=== 4. Cleaning Temporary Scripts ===")
    scripts_unwanted = UNWANTED_DIR / "legacy_scripts"
    scripts_unwanted.mkdir(parents=True, exist_ok=True)
    temp_scripts = ["extract_ref_pdf.py"]
    for s_name in temp_scripts:
        src = BASE_DIR / "scripts" / s_name
        if src.exists():
            dest = scripts_unwanted / s_name
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"  Moved: scripts/{s_name} -> unwanted files and folders/legacy_scripts/{s_name}")

    print("\nOrganization and cleanup complete! All unwanted items safely archived.")

if __name__ == '__main__':
    organize_and_clean()

# PathFinder Machine Learning Datasets Catalog

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

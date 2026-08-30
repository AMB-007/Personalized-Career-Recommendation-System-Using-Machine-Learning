# PathFinder Machine Learning Datasets Catalog

This directory contains the authoritative research and training datasets for the **Personalized Career Recommendation System Using Machine Learning (PathFinder)**.

---

## 📊 Dataset Inventory & File Descriptions

### 1. Production Cleaned Datasets (`*_CLEANED.csv`)
- **`Career_Knowledge_CLEANED.csv`** *(1,203 Rows, 27 Columns | 230 KB)*
  - Curated occupational knowledge base detailing cognitive abilities, RIASEC vocational interests, and educational prerequisites for 1,203 careers across 33 industry domains.
  - Used in database seeding (`backend/database/setup.sql`), live career exploration, and feature building.
- **`Student_Career_Compatibility_CLEANED.csv`** *(50,000 Rows, 22 Columns | 6.32 MB)*
  - Ground-truth student-career compatibility dataset used for CatBoost champion model training and validation (86.22% Accuracy, 98.55% Hit@5, 0.9475 NDCG@5).

### 2. Exploratory Data Analysis RAW Datasets (`*_RAW_*_with_issues.csv`)
- **`Career_Knowledge_RAW_1206_with_issues.csv`** *(1,206 Rows | 229 KB)*
  - Raw uncurated career dataset used in exploratory data analysis (EDA) to demonstrate data cleaning, duplicate removal (3 duplicates pruned), and missing value imputation.
- **`Student_Career_Compatibility_RAW_50k_with_issues.csv`** *(50,000 Rows | 6.30 MB)*
  - Raw unnormalized compatibility pairs used to demonstrate deduplication (150 duplicates pruned), imputation, and leak-free feature engineering.

### 3. Visualizations & Evaluation Reports
- **`figures/`**: Publication-grade exploratory data analysis figures, ROC curves, and SHAP interpretability plots.
- **`reports/`**: Detailed benchmark CSVs, cross-validation metrics, and classification performance reports.
- **`Career_Recommendation_ML_Training_EDA_SHAP.ipynb`**: Complete Jupyter Notebook with full markdown documentation and executed outputs for the 2-dataset pipeline.

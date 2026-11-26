<div align="center">

# PathFinder — Personalized Career Recommendation System

### End-to-End Machine Learning Career Guidance & Stream Selection Platform (Classes 7–12)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.2-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.7-2E8B57?style=for-the-badge)](https://lightgbm.readthedocs.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF4B6E?style=for-the-badge)](https://shap.readthedocs.io/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)

![Test Accuracy](https://img.shields.io/badge/Test_Accuracy-91.35%25-10B981?style=flat-square)
![F1 Score](https://img.shields.io/badge/F1_Score-0.9403-2563EB?style=flat-square)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-97.03%25-8B5CF6?style=flat-square)
![Hit@1](https://img.shields.io/badge/Hit@1_Ranking-99.43%25-059669?style=flat-square)
![Careers](https://img.shields.io/badge/Verified_Careers-158-F59E0B?style=flat-square)
![Model Version](https://img.shields.io/badge/Version-V19.0--XGBoost--SMOTE-0F172A?style=flat-square)

[Overview](#-overview) • [Skills & Tech Stack](#-skills--tech-stack) • [ML Pipeline](#-12-step-machine-learning-pipeline) • [Performance](#-model-performance--benchmarks) • [Visual Insights](#-visual-eda--evaluation-insights) • [Architecture](#-project-structure) • [Setup](#-how-to-run-locally)

</div>

---

## 📌 Overview

**PathFinder** is a full-stack, machine learning–powered career recommendation web application built for students in **Classes 7 to 12**. Students register, enter their academic profile and subject marks, and complete a grade-adaptive psychometric assessment. Their responses are normalized across **22 cognitive and interest dimensions**, combined into a **20-feature ML pipeline**, and scored by a trained **XGBoost** classifier across **158 verified career profiles** to deliver ranked Top-5 recommendations, stream guidance, strengths, and skill-gap insights.

### Key Capabilities
- **Adaptive Psychometric Assessment:** Grade-tailored questions (Classes 7–8 foundation, 9–10 stream discovery, 11–12 specialization) with autosave and review workflow.
- **Leakage-Free ML Recommendation Engine:** Predicts student–career compatibility directly on real dataset labels using a Scikit-learn `ColumnTransformer` + `SMOTE`-balanced `XGBoost` classifier (`V19.0-XGBoost-SMOTE-91pct`).
- **Explainable & Transparent AI:** Feature selection validated via correlation + permutation importance, with global and local explanations powered by **SHAP (`TreeExplainer`)**.
- **Full-Stack Web Platform & Admin Hub:** Role-based student/admin authentication, assessment history dashboards, interactive career explorer, and question/career management backed by **MySQL**.

---

## 🛠️ Skills & Tech Stack

### Core Engineering & Data Science Skills
![Machine Learning](https://img.shields.io/badge/Machine_Learning-2563EB?style=for-the-badge)
![Feature Engineering](https://img.shields.io/badge/Feature_Engineering-0EA5E9?style=for-the-badge)
![Exploratory Data Analysis](https://img.shields.io/badge/Exploratory_Data_Analysis-10B981?style=for-the-badge)
![Data Preprocessing](https://img.shields.io/badge/Data_Preprocessing-14B8A6?style=for-the-badge)
![Class Imbalance SMOTE](https://img.shields.io/badge/SMOTE_Balancing-6366F1?style=for-the-badge)
![Cross Validation](https://img.shields.io/badge/Group_Cross--Validation-8B5CF6?style=for-the-badge)
![Explainable AI SHAP](https://img.shields.io/badge/Explainable_AI_(SHAP)-EC4899?style=for-the-badge)
![REST API Design](https://img.shields.io/badge/REST_API_Design-F59E0B?style=for-the-badge)
![Relational Database Design](https://img.shields.io/badge/Database_Modeling-EF4444?style=for-the-badge)

### Technology Stack

| Domain | Technologies & Libraries |
|---|---|
| **Languages** | ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=mysql&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) |
| **ML & Ensemble Modeling** | ![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat-square&logo=xgboost&logoColor=white) ![LightGBM](https://img.shields.io/badge/LightGBM-2E8B57?style=flat-square) ![Random Forest](https://img.shields.io/badge/Random_Forest-228B22?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) ![imbalanced-learn](https://img.shields.io/badge/imbalanced--learn_(SMOTE)-4F46E5?style=flat-square) |
| **Data Analysis & Visualization** | ![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square) ![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=flat-square) ![SHAP](https://img.shields.io/badge/SHAP-FF4B6E?style=flat-square) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white) |
| **Backend & Security** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) ![Flask-Login](https://img.shields.io/badge/Flask--Login-00B4D8?style=flat-square) ![Bcrypt](https://img.shields.io/badge/Bcrypt-6C757D?style=flat-square) ![WTForms](https://img.shields.io/badge/WTForms-0EA5E9?style=flat-square) ![Joblib](https://img.shields.io/badge/Joblib-10B981?style=flat-square) |
| **Database & Frontend** | ![MySQL](https://img.shields.io/badge/MySQL_8.x-4479A1?style=flat-square&logo=mysql&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite_(Testing)-003B57?style=flat-square&logo=sqlite&logoColor=white) ![Bootstrap 5](https://img.shields.io/badge/Bootstrap_5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white) ![Chart.js](https://img.shields.io/badge/Chart.js_4.4-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) |

---

## ⚙️ 12-Step Machine Learning Pipeline

All data inspection, preprocessing, feature engineering, feature selection, training, cross-validation, and evaluation live in [`model_training/model_training.ipynb`](model_training/model_training.ipynb), sharing exact transformation logic with production inference via [`backend/ml/feature_engineering.py`](backend/ml/feature_engineering.py):

| Stage | Step | Implementation Details |
|---|---|---|
| **Inspection** | **1. Load & Inspect** | Audited `50,689 × 22` raw records (`shape`, `info`, `describe`, missingness, and class distribution) using real `compatibility_label` targets. |
| **Cleaning** | **2. Fix Data Types** | Audited temporal columns (`pd.to_datetime`), parsed dirty string numbers (`%`, commas, `?`, `-`, `unknown`) to `float64`, and fixed `stream` typos (`Scienc`, `Sciense`, `Comerce`, `Arst`). |
| **Cleaning** | **3. Deduplication** | Removed missing-target rows, exact duplicates (`df.drop_duplicates()`), and normalized `(student_id, career_id)` duplicate pairs (`50,689` → `49,691` unique interactions). |
| **Cleaning** | **4. Handle Outliers** | Audited IQR (`1.5 × IQR`) & Z-scores (`\|z\| > 3`); replaced impossible error spikes (`age` outside `[10, 20]`, `class` outside `[7, 12]`, scores outside `[0, 100]` such as `-98.9` and `999.0`) with `NaN` while retaining valid `[0, 100]` distributions. |
| **Pruning** | **5. Drop Useless Columns** | Removed ID columns (`student_id` kept only as group split key, `career_id`) and zero-signal placeholders (`career_subdomain`, `career_cluster`), verifying zero target leakage. |
| **Creation** | **6. Feature Engineering** | Constructed domain alignment features (`academic_learning_avg`, `component_mean_4d`, `component_std_4d`, `alignment_to_gap_ratio`, `weighted_synergy_index`, `ability_to_interest_ratio`). |
| **Splitting** | **7. Group Split (80/20)** | Applied `GroupShuffleSplit` on `student_id` (`39,818` train / `9,873` test, **0 overlapping students**) *before* any step that learns statistics from data. |
| **Selection** | **8. Feature Selection** | Combined Pearson correlation & validation `permutation_importance` (on an internal grouped train-val split) to prune `age`, `class`, and `ability_to_interest_ratio`, keeping **20 features** (`17` numerical + `3` categorical). |
| **Encoding & Scaling** | **9. Train-Only Preprocessing** | `ColumnTransformer` fit strictly on training data: `SimpleImputer(median)` + `StandardScaler` for numericals; `SimpleImputer(most_frequent)` + `OneHotEncoder(handle_unknown='ignore')` for nominal categories (`stream`, `career_domain`, `career_name`). |
| **Balancing** | **10. Class Imbalance** | Applied `SMOTE` strictly on the training matrix (`28% / 72%` → `50% / 50%`) and `class_weight='balanced'` for linear/tree baselines. |
| **Modeling** | **11. CV & 6-Model Benchmark** | Executed 5-fold `StratifiedGroupKFold` CV (`imblearn` leakage-free pipeline) and benchmarked 6 diverse architectures on the untouched test set. |
| **Validation** | **12. Explainability & Export** | Generated 16 figures, 12 CSV audit reports, SHAP values, recommendation ranking metrics, and SHA-256 verified production artifacts. |

---

## 📊 Model Performance & Benchmarks

### 6-Model Test Benchmark (`N_test = 9,873` Unseen Student–Career Pairs)

| Model | Balance Strategy | Test Accuracy | Balanced Acc | Decisive Acc (`\|P - 0.5\| ≥ 0.25`) | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Log Loss |
|---|---|---|---|---|---|---|---|---|---|---|
| 🏆 **XGBoost (Champion)** | `SMOTE` (Train-Only) | **91.35%** | **89.87%** | **95.83%** | **95.01%** | **93.06%** | **0.9403** | **97.03%** | **98.91%** | **0.1965** |
| **LightGBM** | `SMOTE` (Train-Only) | 91.06% | 88.91% | 95.42% | 94.19% | 93.55% | 0.9387 | 96.90% | 98.86% | 0.2005 |
| **Random Forest** | `class_weight='balanced'` | 90.57% | 90.51% | 95.55% | 96.25% | 90.64% | 0.9336 | 97.06% | 98.92% | 0.2106 |
| **Logistic Regression** | `class_weight='balanced'` | 90.51% | 90.74% | 95.12% | 96.56% | 90.24% | 0.9329 | 97.11% | 98.94% | 0.2173 |
| **Decision Tree** | `class_weight='balanced'` | 89.45% | 89.49% | 94.01% | 95.90% | 89.39% | 0.9253 | 95.79% | 98.03% | 0.4150 |
| **KNN (`k=15`)** | `SMOTE` (Train-Only) | 87.08% | 89.48% | 93.39% | 97.74% | 84.28% | 0.9051 | 95.92% | 98.37% | 0.5971 |

### 5-Fold `StratifiedGroupKFold` CV (Training Set) & Ranking Performance (Untouched Test Students)

| Cross-Validation Model | CV Accuracy (Mean ± Std) | CV F1 | CV ROC-AUC |
|---|---|---|---|
| **LightGBM** | 90.96% ± 0.24% | 0.9367 | 96.84% |
| **XGBoost** | 90.86% ± 0.44% | 0.9352 | 96.97% |
| **Random Forest** | 90.37% ± 0.37% | 0.9308 | 96.97% |
| **Logistic Regression** | 90.00% ± 0.41% | 0.9278 | 97.03% |

| Recommendation Ranking Metric | Score | Production Latency (158 Candidates) | Measured Time |
|---|---|---|---|
| **Hit@1 (Top-1 Accuracy)** | **99.43%** | Feature Matrix Construction | `100.84 ms` |
| **Hit@3 (Top-3 Accuracy)** | **99.95%** | XGBoost Batch Inference | `85.01 ms` |
| **Hit@5 / Hit@10** | **100.00%** | Full Recommendation Pipeline | `229.36 ms` |
| **MRR / NDCG@5** | **0.9970 / 0.9905** | Artifact Verification | SHA-256 Verified |

---

## 📈 Visual EDA & Evaluation Insights

<table>
  <tr>
    <td width="50%" align="center">
      <b>Outlier Error Spike Removal (Before vs After)</b><br>
      <img src="figures/04_outliers_before_after_boxplots.png" alt="Outliers Before vs After" width="100%"/>
    </td>
    <td width="50%" align="center">
      <b>Feature Selection (Permutation Importance)</b><br>
      <img src="figures/09_feature_selection_importance.png" alt="Feature Selection Importance" width="100%"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <b>6-Model Benchmark Comparison</b><br>
      <img src="figures/10_model_comparison_metrics_barchart.png" alt="6-Model Benchmark" width="100%"/>
    </td>
    <td width="50%" align="center">
      <b>ROC & Precision-Recall Curves</b><br>
      <img src="figures/11_model_comparison_roc_pr_curves.png" alt="ROC and PR Curves" width="100%"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <b>SHAP Global Feature Explainability</b><br>
      <img src="figures/15_shap_summary_plot.png" alt="SHAP Summary Plot" width="100%"/>
    </td>
    <td width="50%" align="center">
      <b>Error Analysis by Class & Domain</b><br>
      <img src="figures/16_error_analysis_by_domain_and_class.png" alt="Error Analysis" width="100%"/>
    </td>
  </tr>
</table>

<details>
<summary><b>Click to view all 16 generated EDA & evaluation artifacts</b></summary>

- `figures/01_missing_values_distribution.png` — Raw vs post-sanitization missing value audit
- `figures/02_target_distribution.png` — Class distribution & imbalance ratio
- `figures/03_numerical_distributions.png` — Cleaned numerical feature histograms & KDE
- `figures/04_outliers_before_after_boxplots.png` — Outlier error spike removal boxplots
- `figures/05_correlation_heatmap.png` — Cross-feature & target Pearson correlation heatmap
- `figures/06_target_vs_numerical_features.png` — Core feature distributions by target label
- `figures/07_target_vs_domain_and_stream.png` — Compatibility rate across career domains & streams
- `figures/08_career_frequency_distribution.png` — Top 25 careers frequency profile
- `figures/09_feature_selection_importance.png` — Kept vs pruned features via permutation importance
- `figures/10_model_comparison_metrics_barchart.png` — 6-model Accuracy, Balanced Accuracy & ROC-AUC
- `figures/11_model_comparison_roc_pr_curves.png` — Multi-model ROC & PR curves
- `figures/12_model_comparison_confusion_matrices.png` — Confusion matrices for all 6 models
- `figures/13_champion_feature_importances.png` — Top 20 XGBoost feature importances
- `figures/14_champion_calibration_distribution.png` — Probability separation & calibration curve
- `figures/15_shap_summary_plot.png` — SHAP TreeExplainer beeswarm summary
- `figures/16_error_analysis_by_domain_and_class.png` — Accuracy across grades 7–12 & career domains

</details>

---

## 📁 Project Structure

```
├── backend/
│   ├── app.py                        # Flask application factory & blueprint wiring
│   ├── config.py                     # Development, Testing & Production configs
│   ├── ml/
│   │   ├── models/                   # Serialized model.joblib, preprocessor.joblib & JSON metadata
│   │   ├── data/                     # career_knowledge_requirements.csv (158 careers)
│   │   ├── feature_engineering.py    # Shared cleaning, dataset match formulas & engineered features
│   │   ├── feature_builder.py        # Student-career candidate matrix construction
│   │   ├── model_loader.py           # Thread-safe singleton model & metadata loader
│   │   ├── prediction_service.py     # Batch compatibility prediction service
│   │   └── recommendation_service.py # Catalogue scoring, threshold checks & Top-K ranking
│   ├── models/                       # SQLAlchemy ORM models
│   ├── routes/                       # Auth, Student, Assessment, Career & Admin Blueprints
│   └── services/                     # Scoring, profile synthesis & persistence services
├── database/
│   ├── setup.sql                     # MySQL schema (6 tables)
│   └── seed.py                       # Database initializer & seeder
├── frontend/
│   ├── templates/                    # Responsive Jinja2 + Bootstrap 5 templates
│   └── static/                       # CSS, JS, Chart.js integrations & brand assets
├── model_training/
│   └── model_training.ipynb          # Complete executed 12-step EDA & ML training notebook
├── Datasets/
│   ├── Student Career Recommendation Dataset.csv
│   ├── cleaned_career_dataset.csv    # Cleaned & feature-engineered pre-split dataset
│   └── eda_reports/                  # 12 CSV audit, benchmark, CV, SHAP & ranking reports
├── figures/                          # 16 EDA & evaluation figures + UML diagrams
├── scripts/
│   ├── train_model.py                # CLI runner executing model_training.ipynb end-to-end
│   └── export_clean_setup_sql.py
├── tests/                            # ML artifact integrity, API, concurrency & E2E suites
├── requirements.txt
└── run.py                            # Application entry point
```

---

## 🚀 How to Run Locally

### Prerequisites
- **Python 3.11+**
- **MySQL 8.x** running locally
- **Git**

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
Create a `.env` file in the repository root:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_recommendation_db
DATABASE_URL=mysql+mysqlconnector://root:your_mysql_password@localhost:3306/career_recommendation_db
```

### 3. Initialize Database & Run App
```bash
mysql -u root -p < database/setup.sql
python database/seed.py
python run.py
```
Visit **`http://127.0.0.1:5000`** in your browser.

### 4. Retrain ML Pipeline & Regenerate Artifacts
```bash
python scripts/train_model.py
```

---

## 🧪 Running Verification Tests

```bash
# Run ML pipeline, SHA-256 integrity, API, concurrency & recommendation tests
python -m unittest discover tests/ -p "test_ml_*.py" -v

# Run full end-to-end student registration -> assessment -> XGBoost -> results flow
python -m unittest tests/test_e2e_real_student_flow.py -v
```

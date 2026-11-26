# PathFinder — Personalized Career Recommendation System

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF6B6B?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

A machine learning–powered web application that recommends the most suitable careers to students (Classes 7–12) based on their cognitive aptitudes, disciplinary interests, and academic profile. Students complete a level-adaptive assessment, and a trained XGBoost classifier ranks all 158 verified career profiles.

---

## What This Project Does

- Students register, fill their academic profile (Class 7–12, stream, subject marks), and complete an adaptive psychometric assessment.
- Their answers are scored across 22 dimensions and combined into a 20-feature pipeline (17 numerical features including 5 engineered alignment/synergy features + 3 nominal One-Hot Encoded categories).
- A trained **XGBoost** classifier predicts compatibility probabilities for each of **158 career profiles** and returns a **personalised Top-5 career list** with match percentages and domain/stream guidance.
- Admins can manage users, inspect test sessions, and manage the question bank and career profiles.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=flat-square&logo=databricks&logoColor=white) |
| **ML Models** | ![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat-square) ![LightGBM](https://img.shields.io/badge/LightGBM-9ACD32?style=flat-square) ![RandomForest](https://img.shields.io/badge/Random_Forest-228B22?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) |
| **Explainability & EDA** | ![SHAP](https://img.shields.io/badge/SHAP-FF6B6B?style=flat-square) ![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![numpy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Auth** | ![Flask-Login](https://img.shields.io/badge/Flask--Login-00B4D8?style=flat-square) ![Bcrypt](https://img.shields.io/badge/Bcrypt-6C757D?style=flat-square) |

---

## ML Model Performance (Real Dataset Labels, 80/20 Student-Grouped Split)

Evaluated on `9,873` untouched test interaction pairs (`N_clean = 49,691`, zero student or `(student_id, career_id)` pair overlap):

| Model | Balance Strategy | Test Accuracy | Balanced Acc | F1-Score | ROC-AUC | PR-AUC | Decisive Acc |
|---|---|---|---|---|---|---|---|
| **XGBoost (Champion)** | SMOTE (Train-Only) | **91.35%** | **89.87%** | **0.9403** | **97.03%** | **98.91%** | **95.83%** |
| LightGBM | SMOTE (Train-Only) | 91.06% | 88.91% | 0.9387 | 96.90% | 98.86% | 95.42% |
| Random Forest | `class_weight='balanced'` | 90.57% | 90.51% | 0.9336 | 97.06% | 98.92% | 95.55% |
| Logistic Regression | `class_weight='balanced'` | 90.51% | 90.74% | 0.9329 | 97.11% | 98.94% | 95.12% |
| Decision Tree | `class_weight='balanced'` | 89.45% | 89.49% | 0.9253 | 95.79% | 98.03% | 94.01% |
| KNN (k=15) | SMOTE (Train-Only) | 87.08% | 89.48% | 0.9051 | 95.92% | 98.37% | 93.39% |

### Downstream Career Ranking Performance (Untouched Test Students)

| Metric | Score |
|---|---|
| **Hit@1 (Top-1 Accuracy)** | **99.43%** |
| **Hit@3 (Top-3 Accuracy)** | **99.95%** |
| **Hit@5 (Top-5 Accuracy)** | **100.00%** |
| **MRR (Mean Reciprocal Rank)** | **0.9970** |
| **NDCG@5** | **0.9905** |

---

## Project Structure

```
├── backend/
│   ├── app.py                      # Flask app factory
│   ├── config.py                   # Environment configs
│   ├── ml/
│   │   ├── models/                 # Trained model artifacts (.joblib & JSON metadata)
│   │   ├── feature_engineering.py  # Single source of truth for cleaning & engineered features
│   │   ├── feature_builder.py      # Multi-dimensional candidate feature matrix builder
│   │   ├── model_loader.py         # Singleton artifact loader & validator
│   │   ├── prediction_service.py   # Batch compatibility inference
│   │   └── recommendation_service.py
│   ├── models/                     # SQLAlchemy ORM models
│   ├── routes/                     # Flask Blueprints
│   └── services/                   # Business logic layer
├── database/
│   ├── setup.sql                   # MySQL schema (6 tables)
│   └── seed.py                     # Seeds questions & career data
├── frontend/
│   ├── templates/                  # Jinja2 HTML templates
│   └── static/                     # CSS, JS, icons
├── model_training/
│   ├── model_training.ipynb        # End-to-end 12-step EDA, preprocessing & training notebook
│   ├── model.joblib                # Exported champion model
│   └── preprocessor.joblib         # Exported ColumnTransformer preprocessor
├── Datasets/
│   ├── Student Career Recommendation Dataset.csv
│   ├── cleaned_career_dataset.csv  # Cleaned & feature-engineered pre-split dataset
│   └── eda_reports/                # Generated EDA, CV, benchmark, ranking & SHAP CSV reports
├── figures/                        # 16 new EDA, preprocessing & evaluation figures + UML diagrams
├── scripts/
│   ├── train_model.py              # Reproducible CLI runner executing model_training.ipynb
│   └── export_clean_setup_sql.py
├── tests/                          # Unit, ML integrity, API & E2E tests
├── requirements.txt
└── run.py                          # App entry point
```

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- MySQL 8.x running locally
- Git

### 1. Clone the repository
```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Create a `.env` file in the project root:
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

### 4. Set up the database
```bash
mysql -u root -p < database/setup.sql
python database/seed.py
```

### 5. Run the application
```bash
python run.py
```

Open your browser at **http://127.0.0.1:5000**

---

## ML Pipeline & Retraining

The complete machine learning pipeline lives in [`model_training/model_training.ipynb`](model_training/model_training.ipynb), implementing all 12 steps cleanly without leakage:

1. Data inspection (`shape`, `info`, `describe`, missingness & class balance)
2. Data type standardization (string-encoded numbers, canonical stream typos, `pd.to_datetime` check)
3. Exact & `(student_id, career_id)` duplicate removal
4. Outlier & impossible-error handling (`age`, `class`, `[0, 100]` domain bounds + IQR/Z-score diagnostics)
5. Useless & identifier column removal (`student_id`, `career_id`, `career_subdomain`, `career_cluster`)
6. Feature engineering (`academic_learning_avg`, `component_mean_4d`, `component_std_4d`, `alignment_to_gap_ratio`, `weighted_synergy_index`)
7. Leakage-free 80/20 `GroupShuffleSplit` by `student_id`
8. Feature selection via Pearson correlation, tree feature importance & validation permutation importance
9. Train-only `SimpleImputer` (median for numbers, mode for text), `OneHotEncoder`, and `StandardScaler`
10. Train-only class imbalance handling (`SMOTE` & `class_weight='balanced'`)
11. 5-fold `StratifiedGroupKFold` CV + 6-model benchmark (Logistic Regression, KNN, Decision Tree, Random Forest, LightGBM, XGBoost)
12. Evaluation figures, SHAP explainability, ranking evaluation & artifact serialization

To retrain from scratch and regenerate all reports, figures, and model artifacts:
```bash
python scripts/train_model.py
```

---

## Running Tests

```bash
python -m unittest discover tests/ -p "test_ml_*.py"
python -m unittest tests/test_e2e_real_student_flow.py
```

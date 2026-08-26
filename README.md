# Personalized Career Recommendation System for Class 7–12 Students

A production-style Career Guidance and Personalized Career Recommendation Web Application powered by an **XGBoost Career Compatibility & Ranking Machine Learning Model (V7.2)**, built with Python, Flask, Flask-SQLAlchemy, MySQL Server 8.x, MySQL Workbench, Bootstrap 5, and Chart.js.

---

## 🌟 Architecture Overview

The application implements a multi-stage Machine Learning Career Recommendation pipeline:

```
Student Assessment Questionnaire (Class 7–12)
                      ↓
  Student Normalized Profile (Cognitive Scores, Interests, Academic Record)
                      ↓
    Feature Builder (backend/ml/feature_builder.py)
    [Computes 8-D Ability Match & 10-D Interest Match against 1,206 Careers]
    [Builds authoritative 11-feature contract DataFrame]
                      ↓
    Model Loader Singleton (backend/ml/model_loader.py)
    [Loads model.joblib + preprocessor.joblib once with thread-safe caching]
                      ↓
    Preprocessor Pipeline (preprocessor.joblib)
    [Imputation, StandardScaler, OrdinalEncoder]
                      ↓
    XGBoost Compatibility Model (model.joblib)
    [Predicts compatibility probabilities p(y=1) for all 1,206 career candidates]
                      ↓
    Career Recommendation Engine (backend/ml/recommendation_service.py)
    [Ranks careers by compatibility score, extracts Top 1, Top 3, Top 5, Top 10]
    [Enriches with prerequisite subjects, top skills, educational roadmaps]
                      ↓
    Database Persistence (MySQL `career_recommendations` table)
                      ↓
    REST APIs / Interactive Frontend (results.html, dashboard.html, explorer.html)
```

---

## 📊 Verified Model Performance

> [!IMPORTANT]
> **Performance Reporting Transparency:**
> Classification performance and ranking recommendation performance are strictly separated:

### 1. Recommendation Ranking Performance (Catalogue of 1,206 Careers)
- **Hit@1:** **96.18%** (Primary recommended career match rate)
- **Hit@3:** **99.68%**
- **Hit@5:** **99.88%**
- **Hit@10:** **99.94%**
- **Mean Reciprocal Rank (MRR):** **97.98%**
- **NDCG@5:** **92.12%**

### 2. Binary Compatibility Classification Performance (Independent Test Set)
- **Accuracy:** **80.99%**
- **Balanced Accuracy:** **71.71%**
- **Precision:** **83.21%**
- **Recall:** **92.40%**
- **F1 Score:** **87.56%**
- **ROC-AUC:** **85.25%**
- **PR-AUC:** **93.48%**
- **Decision Threshold:** **0.495**

---

## 📦 Production ML Model Artifacts

Location: `backend/ml/models/`

| Artifact File | Description |
| :--- | :--- |
| `model.joblib` | Canonical trained `XGBClassifier` model weights |
| `preprocessor.joblib` | Scikit-learn `ColumnTransformer` (StandardScaler + OrdinalEncoder) |
| `feature_columns.json` | Authoritative 11-feature contract schema |
| `classes.json` | Target classes (`[0, 1]`) and label mappings |
| `model_config.json` | Best hyperparameters and decision threshold (0.495) |
| `version.json` | Version identifier (`V7.2`) and timestamp |
| `feature_importance.csv` | Feature importance rankings |
| `training_history.json` | Training cross-validation & benchmark metrics |

### Feature Contract Schema (`feature_columns.json`)
The model expects exactly 11 features in this exact order:
1. `age`: Student age (`int`/`float`, range: 10–25)
2. `class`: School grade level (`int`, range: 7–12)
3. `ability_match_component`: Mean match across 8 cognitive ability dimensions (`float`, 0–100)
4. `interest_match_component`: Mean match across 10 disciplinary interest dimensions (`float`, 0–100)
5. `academic_match_component`: Overall academic percentage (`float`, 0–100)
6. `learning_match_component`: Learning ability score (`float`, 0–100)
7. `career_name`: Name of candidate career (`str`)
8. `career_domain`: Industry / professional domain (`str`)
9. `career_subdomain`: Subdomain track (`str`)
10. `career_cluster`: Functional occupational cluster (`str`)
11. `stream`: Academic stream (`str`: `Science-PCM`, `Science-PCB`, `Commerce`, `Humanities`, `General`)

*Security Rule: `student_id` is never used as an ML feature.*

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, mysql-connector-python, PyMySQL, python-dotenv
- **Machine Learning:** XGBoost 2.0+, scikit-learn 1.4+, joblib, pandas, numpy
- **Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Chart.js 4.4, Bootstrap Icons (Zero Gradients Flat Design with Light & Dark Themes)
- **Database Server:** MySQL Server 8.x (with fallback SQLite for testing isolation)
- **Database Tool:** MySQL Workbench 8.x

---

## 📁 Directory Structure

```
career_recommendation_system/
├── backend/
│   ├── app.py                      # Flask Application Factory & Blueprints
│   ├── config.py                   # Configuration (Dev, Test, Prod)
│   ├── extensions.py               # Database, LoginManager, Bcrypt
│   ├── models/                     # Relational ORM models (MySQL)
│   ├── routes/                     # REST API & Web Blueprints
│   │   ├── auth_routes.py          # /login, /register, /logout
│   │   ├── student_routes.py       # /dashboard, /profile
│   │   ├── assessment_routes.py    # /assessment, /review, /results
│   │   ├── career_routes.py        # /careers, /api/recommendations, /api/model/info
│   │   └── admin_routes.py         # /admin controls
│   ├── services/                   # Business & assessment services
│   └── ml/                         # Production Machine Learning Core
│       ├── models/                 # Canonical V7.2 model artifacts
│       ├── data/                   # Cleaned 1,206 career requirements dataset
│       ├── model_loader.py         # Thread-safe singleton model loader
│       ├── feature_builder.py      # Feature contract & match component builder
│       ├── prediction_service.py   # Pure XGBoost inference service
│       └── recommendation_service.py # Catalogue ranking & Top-K engine
├── frontend/
│   ├── templates/                  # Jinja2 HTML templates
│   └── static/                     # Custom CSS, JS (assessment.js, charts.js, main.js)
├── database/                       # MySQL DDL, seed, and dataset import scripts
├── docs/                           # Architecture, API examples, and reports
├── data/                           # Raw datasets and feature contracts
├── tests/                          # 73 automated unit, integration, and E2E tests
├── requirements.txt
├── run.py                          # Application entry point
└── README.md
```

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System and ML model health status |
| `GET` | `/api/model/info` | Model metadata, feature schema, and verified metrics |
| `POST` | `/api/predictions` | Direct compatibility prediction for candidate feature vectors |
| `POST` | `/api/recommendations` | Generate ranked career recommendations for session or profile |
| `GET` | `/api/recommendations/<int:id>` | Retrieve stored recommendations for assessment session |
| `GET` | `/api/careers` | Search and filter careers with pagination |
| `GET` | `/api/careers/<int:id>` | Full career profile, required skills, and roadmap |
| `GET` | `/api/careers/domains` | List all industry domains |
| `POST` | `/api/assessment/start` | Start new student assessment session |
| `POST` | `/api/assessment/answer` | Record student question response |
| `POST` | `/api/assessment/submit` | Submit completed assessment & trigger ML evaluation |

---

## 🚀 Local Setup & Execution

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and set your credentials:
```powershell
copy .env.example .env
```

### 3. Run the Application
```powershell
python run.py
```
Access in your browser at: **`http://localhost:5000`**

### 4. Run Automated Test Suite
```powershell
python -m unittest discover tests
```
*(All 73 test cases pass with zero failures).*

---

## 🔑 Demo Credentials (Development)

| Role | Username | Password | Class Level |
| :--- | :--- | :--- | :--- |
| **Student** | `rahul_class8` | `Student@123` | Class 8 (CBSE) |
| **Student** | `ananya_class10` | `Student@123` | Class 10 (ICSE) |
| **Student** | `aravind_class12` | `Student@123` | Class 12 (Science-PCM) |
| **Administrator** | `admin` | `Admin@123` | System Admin |

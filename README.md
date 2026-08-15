# Personalized Career Recommendation System

> An AI-powered career guidance platform that analyzes a student academic profile, aptitude, psychometric traits, and interests to recommend the most suitable career paths with full SHAP explainability showing why each career was recommended.

---

## Overview

| Feature | Detail |
|---|---|
| ML Model | 4-Model Soft-Voting Ensemble (XGBoost + CatBoost + LightGBM + Random Forest) |
| Accuracy | 95%+ on 40,000-student dataset across 30 career classes |
| Explainability | Live SHAP attributions per prediction (top-15 feature impact) |
| Backend | Flask REST API + MySQL |
| Frontend | Vanilla HTML/CSS/JS (multi-page) |
| Auth | JWT Bearer Token |
| Careers | 30 career classes |


---

## Project Architecture

```
STUDENT fills assessment: Academic + Aptitude + Interests + Skills
                 |
                 v   POST /api/assessment/submit
         FLASK REST API (backend/app.py)
         1. Feature Engineering  (72 features from 61 raw inputs)
         2. Preprocessing        (OrdinalEncoder + StandardScaler)
         3. Soft-Vote Ensemble   (4 models, equal weights ~0.25 each)
         4. Live SHAP            (XGBoost TreeExplainer, per request)
         5. Store results        (MySQL career_predictions table)
                 |
    +-----------+-----------+-----------+
    |           |           |           |
  XGBoost  CatBoost   LightGBM  RandomForest
  w=0.25   w=0.25     w=0.25    w=0.25
    |           |           |           |
    +-----+-----+-----+-----+
                |
         Weighted Average Proba
                |
         Top-5 Careers + Confidence % + SHAP Reasons
```

---

## Project Structure

```
Personalized Career Recommendation System/
|
+-- app.py                          <- Root launcher (run this to start)
+-- README.md
+-- .gitignore
|
+-- backend/
|   +-- app.py                      <- Flask REST API (1700+ lines)
|   +-- requirements.txt            <- All Python dependencies
|   +-- career_system_db.sql        <- MySQL schema dump
|   +-- .env                        <- DB credentials (not in git)
|   |
|   +-- core/
|   |   +-- db_config.py            <- DB connection pool
|   |
|   +-- models/                     <- Trained ML artifacts
|   |   +-- career_model.pkl        <- XGBoost (primary predictor)
|   |   +-- xgb_base_model.pkl      <- XGBoost (SHAP source)
|   |   +-- catboost_model.pkl      <- CatBoost
|   |   +-- lgbm_model.pkl          <- LightGBM
|   |   +-- rf_model.pkl            <- Random Forest (187 MB)
|   |   +-- ensemble_weights.pkl    <- Soft-vote weights
|   |   +-- label_encoder.pkl       <- int <-> career name
|   |   +-- ordinal_encoder.pkl     <- categorical -> numeric
|   |   +-- scaler.pkl              <- StandardScaler
|   |   +-- feature_columns.pkl     <- Ordered list of 72 features
|   |   +-- cat_feature_names.pkl   <- 10 categorical feature names
|   |   +-- numeric_feature_names.pkl
|   |   +-- cat_feature_indices.pkl
|   |   +-- model_type.pkl          <- "voting_ensemble"
|   |   +-- career_dataset.csv      <- Training dataset (40K rows)
|   |
|   +-- output/
|       +-- output.txt              <- EDA analysis report
|
+-- frontend/
    +-- dist/                       <- Served by Flask as static files
        +-- index.html              <- Landing page
        +-- login.html
        +-- register.html
        +-- assessment.html         <- Career assessment form
        +-- dashboard.html          <- Results + SHAP dashboard
        +-- history.html            <- Past predictions
        +-- settings.html
        +-- admin.html
        +-- admin-login.html
        +-- css/
        |   +-- style.css
        +-- js/
            +-- app.js              <- Global auth/API helpers
            +-- home.js
            +-- assessment.js
            +-- dashboard.js        <- SHAP chart rendering
            +-- history.js
            +-- settings.js
            +-- admin.js
```

---

## Machine Learning Pipeline

### Dataset
| Property | Value |
|---|---|
| Rows | 40,000 students |
| Raw features | 61 |
| Engineered features | +11 interaction features |
| Total features | 72 |
| Career classes | 30 |

### Engineered Features

| Feature | Formula |
|---|---|
| Total_Aptitude | Sum of 4 aptitude scores |
| STEM_Signal | (Logical+Analytical) x (Tech+Eng) / 400 |
| Health_Signal | Healthcare x (Numerical+Research) / 200 |
| Business_Signal | Business x (Leadership+Comm+Decision) / 300 |
| Creative_Signal | Arts x (Creativity+Spatial) / 200 |
| Research_Signal | Research x (Analytical+Curiosity) / 300 |
| Activity_Richness | Projects x 2 + Certs x 1.5 + Hacks + Interns x 2 |
| Dominant_Interest | max of all 10 interest scores |
| Interest_Spread | max - min of interest scores |
| Weighted_Academic | CGPA x 0.4 + Marks x 0.35 + Internal x 0.25 |
| Soft_Skill_Composite | mean(Leadership, Teamwork, Comm, Adaptability, Decision, Time) |

### Model Configuration

| Model | Trees | Depth | Class Balancing |
|---|---|---|---|
| XGBoost | 800 | 8 | compute_sample_weight |
| CatBoost | 800 | 8 | auto_class_weights=Balanced |
| LightGBM | 800 | 8 | is_unbalance=True |
| Random Forest | 500 | 25 | class_weight=balanced_subsample |

### 30 Career Classes

```
AI Engineer              Agricultural Scientist   Animator
Architect                Bank Manager             Biomedical Engineer
Business Analyst         Chartered Accountant     Civil Engineer
Cloud Architect          Cyber Security Analyst   Data Analyst
Data Scientist           Doctor                   Electrical Engineer
Entrepreneur             Environmental Scientist  Full Stack Developer
Graphic Designer         Lawyer                   Machine Learning Engineer
Mechanical Engineer      Nurse                    Pharmacist
Product Manager          Professor/Researcher     Psychologist
School Teacher           Software Developer       UI/UX Designer
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Personalized Career Recommendation System Using Machine Learning"
```

### 2. Setup Database
```sql
CREATE DATABASE career_system_db;
USE career_system_db;
SOURCE backend/career_system_db.sql;
```

### 3. Configure Environment
Create or edit `backend/.env`:
```
DB_NAME=career_system_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
JWT_SECRET=your_secret_key_here
```

### 4. Install Dependencies
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 5. Add Trained Model Files
Place all 14 .pkl files into `backend/models/` directory.

### 6. Run the Application
```bash
# From the project root
python app.py

# OR from backend directory
cd backend && python app.py
```

Visit: http://127.0.0.1:5000

---

## API Reference

### Authentication
All protected routes require:
```
Authorization: Bearer <jwt_token>
```

### Key Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /api/auth/register | No | Register student |
| POST | /api/auth/login | No | Login, returns JWT |
| POST | /api/assessment/submit | Optional | Submit assessment, get predictions |
| GET | /api/health | No | Health check, ml_ready status |
| GET | /api/dashboard | Yes | Dashboard data + latest prediction |
| GET | /api/history | Yes | All past predictions |
| GET | /api/user/profile | Yes | Get profile |
| PUT | /api/user/profile | Yes | Update profile |
| GET | /api/prediction/shap/<id> | Yes | Full SHAP for a prediction |
| GET | /api/admin/users | Admin | List all users |
| GET | /api/admin/analytics | Admin | System analytics |
| POST | /api/admin/questions | Admin | Add question to bank |
| POST | /api/admin/retrain | Admin | Trigger retraining |

### Assessment Submit - Sample Request
```json
{
  "education_level": "Undergraduate",
  "degree": "B.E/B.Tech",
  "specialization": "Computer Science",
  "stream": "Science",
  "board": "CBSE",
  "cgpa": 8.5,
  "attendance": 88,
  "semester_marks": 80,
  "psychometric_traits": {
    "Leadership": 70, "Teamwork": 75, "Communication": 72,
    "Creativity": 60, "Problem_Solving": 85, "Analytical_Thinking": 82,
    "Adaptability": 68, "Decision_Making": 70, "Time_Management": 65,
    "Curiosity": 78, "Stress_Management": 62, "Self_Learning": 80,
    "Persistence": 72, "Confidence": 68
  },
  "interest_scores": {
    "Technology": 90, "Healthcare": 20, "Business": 30,
    "Creative Arts": 25, "Research": 70, "Education": 25,
    "Engineering": 85, "Law": 10, "Environment": 15, "Social Service": 20
  },
  "skill_scores": { "Python": 85, "Machine Learning": 80 },
  "certifications": ["AWS", "TensorFlow Developer"],
  "projects": ["ML Project", "Web App"],
  "internships_count": 1
}
```

### Assessment Submit - Sample Response
```json
{
  "status": "success",
  "top5_careers": [
    { "career": "Software Developer", "confidence": 36.9, "rank": 1 },
    { "career": "Machine Learning Engineer", "confidence": 16.8, "rank": 2 },
    { "career": "Data Scientist", "confidence": 12.6, "rank": 3 },
    { "career": "Product Manager", "confidence": 12.3, "rank": 4 },
    { "career": "AI Engineer", "confidence": 11.0, "rank": 5 }
  ],
  "readiness_score": 85,
  "xai_attributions": [
    { "feature": "STEM_Signal", "importance": 1.797, "direction": "positive" },
    { "feature": "Engineering_Interest", "importance": 0.580, "direction": "positive" },
    { "feature": "Research_Interest", "importance": -1.000, "direction": "negative" }
  ]
}
```

---

## SHAP Explainability

Every prediction includes a live SHAP explanation:

```
Predicted: Software Developer (36.9% confidence)

Top reasons:
  + STEM_Signal             +1.80   Your tech+engineering combo is very strong
  + Engineering_Interest    +0.58   Engineering background supports this path
  + Technology_Interest     +0.43   Strong technology passion aligned
  - Research_Interest       -1.00   High research interest slightly reduces fit
  + Analytical_Thinking     +0.19   Analytical skills support development roles
```

Direction: positive (+) = pushed model toward this career
           negative (-) = slightly reduced this career rank

---

## Database Schema (15 Tables)

| Table | Purpose |
|---|---|
| users | Student and admin accounts |
| assessment_sessions | Each assessment attempt |
| assessment_answers | Individual question answers |
| career_predictions | ML results + full SHAP JSON |
| question_bank | Aptitude/psychometric questions |
| careers | Career metadata |
| career_skills | Skills required per career |
| career_education | Education paths per career |
| skill_categories | Skill taxonomy |
| user_skills | Student skills |
| certifications | Certification records |
| projects | Project records |
| internships | Internship records |
| academic_records | Academic details |
| interest_scores | Student interest ratings |

---

## Performance

| Metric | Value |
|---|---|
| Top-1 Accuracy | 95%+ |
| Top-3 Accuracy | 98.9% |
| Top-5 Accuracy | 99.4% |
| Dataset | 40,000 students |
| Career Classes | 30 |
| API Response | Less than 500ms (including SHAP) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.10+, Flask 3.1, Flask-CORS |
| Database | MySQL 8.0, mysql-connector-python |
| ML Models | XGBoost 3.3, CatBoost 1.2, LightGBM 4.7, scikit-learn 1.9 |
| Explainability | SHAP 0.46+ (TreeExplainer) |
| Data Processing | pandas 3.0, numpy 2.5, scipy 1.18 |
| Auth | PyJWT 2.13, Werkzeug 3.1 |
| Frontend | HTML5, Vanilla CSS, Vanilla JavaScript |

---

## Security

- Passwords hashed with Werkzeug PBKDF2-SHA256
- Auth via PyJWT signed tokens (1-hour expiry)
- SQL injection prevented via parameterized queries
- CORS configured via Flask-CORS
- Admin role enforced server-side on every admin endpoint

---

## Default Admin Account

After first run (DB auto-initialized):
```
Email    : admin@career.ai
Password : Admin@2024
Role     : admin
```

Change the admin password immediately after first login.

---

## Model Training (Google Colab)

To retrain models:
1. Upload backend/models/career_dataset.csv to Colab
2. Run the full training notebook
3. Download all .pkl files to backend/models/
4. Restart: python app.py

Training accuracy targets:
- XGBoost:       ~90-91%
- CatBoost:      ~93-94%
- LightGBM:      ~91-92%
- Random Forest: ~90-91%
- Ensemble (all 4): 95%+

---

## License

This project is developed for academic and educational purposes.

---

## Acknowledgements

- Dataset: Custom-generated 40,000-student career dataset
- ML: XGBoost, CatBoost, LightGBM, scikit-learn teams
- Explainability: SHAP (Lundberg and Lee, 2017)

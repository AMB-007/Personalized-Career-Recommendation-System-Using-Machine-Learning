# 🎓 Personalized Career Recommendation System Using Machine Learning

> An intelligent, full-stack AI career guidance platform that delivers personalized career recommendations through adaptive assessments, a 4-model ML ensemble, and explainable AI — tailored for students from Class 7 all the way through postgraduate level.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [ML Architecture](#-ml-architecture)
- [Assessment Flow](#-assessment-flow)
- [Education Level Adaptations](#-education-level-adaptations)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Setup & Installation](#-setup--installation)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [Supported Careers (30)](#-supported-careers-30)
- [Admin Panel](#-admin-panel)

---

## 🔍 Overview

This system collects a rich multi-dimensional profile from each student — academic marks, aptitude, psychometrics, interests, and verified skills — then feeds it through a **72-feature vector** into a soft-voting ensemble of **XGBoost + CatBoost + LightGBM + RandomForest** to predict the top 5 best-fit career paths with confidence scores.

The frontend is a fully adaptive **8-step assessment** that automatically adjusts questions, subjects, and visible steps based on the student's education level and board (CBSE / Kerala State Board / ICSE).

---

## ✨ Key Features

### 🧠 AI & ML
- **4-Model Ensemble**: XGBoost + CatBoost + LightGBM + RandomForest with soft-vote weighting
- **72-feature vector**: Academic, aptitude, psychometric, interest, skill, and activity signals
- **Live SHAP explainability**: Per-feature attribution shown on the results dashboard
- **30 career classes** predicted with confidence percentages
- **Readiness score**: Composite score indicating how prepared the student is
- **Fallback mock mode**: Graceful degradation when model files are missing

### 📋 Adaptive Assessment (8 Steps)
- **Step 1**: Education profile (level, board, stream, degree)
- **Step 2**: Subject-wise marks (subjects auto-loaded by board: 10 for Kerala, 5 for CBSE)
- **Step 3**: Aptitude quiz (difficulty adapts to class level)
- **Step 4**: Psychometric scenarios (age-appropriate question banks per level)
- **Step 5**: Career interest profiling (20+ paired-choice questions)
- **Step 6**: Skill verification with quizzes (53 skills, 3-question quiz per skill)
- **Step 7**: Certifications / Achievements *(skipped for Class 7–10)*
- **Step 8**: Projects & Portfolio *(skipped for Class 7–10)*
- **Step 9**: Results with top-5 careers, SHAP charts, roadmaps

### 🏫 Education Level Intelligence
- **Class 7–10**: Steps 7 & 8 auto-skipped; CGPA derived from avg marks; age derived from class
- **Class 11–12**: Steps 7 & 8 adapted to "Achievements" and "School Projects"
- **UG / PG / Professional**: Full 9-step flow with all fields
- **Board-aware subjects**: Kerala State Board (10 subjects), CBSE (5 subjects), ICSE (6 subjects)

### 🎯 Skill Verification
- **53 quiz-verified skills** across Technical, Business, Science, Creative, and Soft Skill domains
- Each skill has a **3-question quiz** with scored proficiency: Beginner / Intermediate / Advanced
- Skills not in the quiz bank use a **self-rating modal** as fallback
- Proficiency weights: Beginner=33, Intermediate=66, Advanced=100 (used in `Subject_Knowledge_Score`)

### 👤 User Features
- Registration & Login with JWT authentication
- Personal dashboard with career history, charts, and SHAP visualization
- Assessment history with trend analysis
- Settings page (update profile, change password)

### 🔧 Admin Panel
- Total students, assessments, questions statistics
- Top career distribution chart
- Daily assessment trend chart
- One-click model retraining trigger

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vanilla HTML5, CSS3 (custom design system), JavaScript (ES6+) |
| **Backend** | Python 3.x, Flask 3.1, Flask-CORS |
| **Database** | MySQL 8.x (15 normalized tables) |
| **ML Models** | XGBoost 3.3, CatBoost 1.2, LightGBM 4.7, scikit-learn RandomForest |
| **Explainability** | SHAP (TreeExplainer on XGBoost) |
| **Auth** | JWT (PyJWT 2.x), Werkzeug password hashing (pbkdf2:sha256) |
| **Data** | Pandas 3.x, NumPy 2.x |
| **Model Training** | Jupyter Notebook (`Model_Training.ipynb`) |
| **DB Driver** | mysql-connector-python with connection pooling (pool_size=5) |

---

## 📁 Project Structure

```
Personalized Career Recommendation System/
│
├── README.md                        ← This file
├── Model_Training.ipynb             ← Jupyter notebook for model training
├── app.py                           ← Root launcher (delegates to backend)
├── start.bat                        ← One-click Windows launcher
├── start.ps1                        ← PowerShell launcher
│
├── backend/
│   ├── app.py                       ← Main Flask application (~1984 lines)
│   │                                  · 15 DB tables auto-created on startup
│   │                                  · 4-model ensemble loader + SHAP
│   │                                  · 72-feature vector construction
│   │                                  · All REST API endpoints
│   ├── career_system_db.sql         ← Full database setup script
│   ├── requirements.txt             ← Python dependencies
│   ├── .env                         ← DB credentials & JWT secret
│   │
│   └── models/                      ← Trained ML model artifacts
│       ├── career_model.pkl         ← XGBoost base model
│       ├── catboost_model.pkl       ← CatBoost model
│       ├── lgbm_model.pkl           ← LightGBM model
│       ├── rf_model.pkl             ← RandomForest (~166MB)
│       ├── label_encoder.pkl        ← Career label encoder (30 classes)
│       ├── preprocessor.pkl         ← ColumnTransformer
│       ├── feature_columns.pkl      ← Ordered 72-feature list
│       ├── ensemble_weights.pkl     ← Per-model voting weights
│       ├── scaler.pkl               ← StandardScaler
│       └── career_dataset.csv       ← Training dataset (~12MB)
│
└── frontend/
    └── dist/                        ← Deployable frontend
        ├── index.html               ← Landing page
        ├── login.html               ← Student login
        ├── register.html            ← Student registration
        ├── assessment.html          ← 9-step assessment form
        ├── dashboard.html           ← Career results dashboard
        ├── history.html             ← Assessment history
        ├── settings.html            ← User settings
        ├── admin.html               ← Admin dashboard
        ├── admin-login.html         ← Admin login
        │
        └── js/
            ├── assessment.js        ← Assessment engine (~143KB)
            │                          · BOARD_SUBJECTS (adaptive per board)
            │                          · SKILL_QUIZ_BANK (53 skills × 3 Qs)
            │                          · PSYCH_BANK (per-level scenarios)
            │                          · APTITUDE_BANK (adaptive difficulty)
            │                          · School-level step skipping logic
            ├── dashboard.js         ← Dashboard charts & SHAP visualization
            ├── app.js               ← Auth, API helper, Toast notifications
            ├── home.js              ← Landing page interactions
            ├── admin.js             ← Admin panel logic
            ├── history.js           ← Assessment history charts
            └── settings.js          ← Settings page logic
```

---

## 🤖 ML Architecture

### Model Ensemble

```
Input (72 features)
        │
        ├──► XGBoost      ──► P(career)  × weight w1
        ├──► CatBoost     ──► P(career)  × weight w2
        ├──► LightGBM     ──► P(career)  × weight w3
        └──► RandomForest ──► P(career)  × weight w4
                          │
                          └──► Soft Vote: P_final = Σ(wi × Pi)
                                    │
                                    └──► Top-5 Careers + Confidence %
```

### 72-Feature Vector

| Category | Features | Count |
|---|---|---|
| Academic | CGPA, Avg Marks, Semester Marks, Internal, Practical, Lab, Assignment | 7 |
| Aptitude | Logical, Numerical, Verbal, Spatial | 4 |
| Psychometric | Leadership, Teamwork, Communication, Creativity, Problem Solving, Critical Thinking, Adaptability, Decision Making, Time Management, Curiosity, Analytical, Stress Management, Self Learning, Persistence, Confidence | 15 |
| Career Interest | Technology, Healthcare, Business, Arts/Creative, Research, Education, Engineering, Law, Environment, Social Service | 10 |
| Skills | Num_Technical_Skills, Subject_Knowledge_Score | 2 |
| Activities | Num_Projects, Num_Certifications, Internships, Hackathons, Research Exp, Competitions, Volunteer | 7 |
| Engineered | STEM signal, Health signal, Biz signal, Creative signal, Research signal, Activity richness, Soft composite, Weighted Academic, Interest spread, Dominant Interest, Total Aptitude | 11 |
| Demographics | Age, Year of Study | 2 |
| Derived Scores | Readiness, Activity score, Soft Skill score, Academic composite | 4 |
| Other | Attendance %, Skill verified score, Programming score | 3 |

---

## 📝 Assessment Flow

```
Step 1: Education Profile
  → Level: Class 7 to PhD/Professional
  → Board: Kerala State / CBSE / ICSE / Other
  → Stream (Class 11-12 and UG only)
  → Degree, Specialization (UG/PG only)
  [CGPA hidden for Class 7–12; auto-derived from avg marks]
  [Attendance hidden for all school levels]

Step 2: Academic Marks
  → Subjects auto-loaded by board:
    Kerala Class 10 : 10 subjects (Languages + Core + IT)
    CBSE Class 10   :  5 subjects (English, Math, Science, SST, Hindi)
    ICSE Class 10   :  6 subjects
  → Enter marks (0–100) and grade per subject

Step 3: Aptitude Quiz (10 questions)
  → Class 7–10    : Easy / Medium (logical, numerical, series)
  → Class 11–12   : Medium / Hard (abstract, spatial reasoning)
  → UG / PG       : Hard (data interpretation, critical reasoning)
  → Only shown after all answers selected

Step 4: Psychometric Scenarios (6 questions)
  → School scenarios  : classroom, hobby, social situations
  → College scenarios : career, group project, workplace prep
  → Professional      : leadership, decision-making, management

Step 5: Career Interest Profiling (20+ pairs)
  → Forced-choice between domain pairs
  → Domains: Technology · Healthcare · Business · Arts
             Research · Education · Engineering · Law
             Environment · Social Service

Step 6: Skill Verification
  → Select from 53 available skills
  → Each skill → 3-question quiz → Beginner/Intermediate/Advanced
  → Quiz score feeds Subject_Knowledge_Score in ML

Step 7: Certifications / Achievements
  → [SKIPPED for Class 7–10]
  → Class 11–12: Olympiad medals, school awards, online courses
  → UG/PG: AWS, Google, Microsoft, NPTEL certifications

Step 8: Projects & Portfolio
  → [SKIPPED for Class 7–10]
  → Class 11–12: Science fair, school club activities
  → UG/PG: GitHub projects, internship work

Step 9: Results
  → Top 5 career predictions with confidence %
  → SHAP feature attribution chart
  → 8-step career roadmap per prediction
  → Salary range, required degree, top companies, growth %
```

---

## 🏫 Education Level Adaptations

| Level | Aptitude | Steps 7–8 | CGPA field | Age used |
|---|---|---|---|---|
| Class 7 | Easy | **Skipped** | Hidden (auto: marks÷10) | 12 |
| Class 8 | Easy | **Skipped** | Hidden (auto: marks÷10) | 13 |
| Class 9 | Medium | **Skipped** | Hidden (auto: marks÷10) | 14 |
| Class 10 | Medium | **Skipped** | Hidden (auto: marks÷10) | 15 |
| Class 11–12 | Medium-Hard | Adapted (Achievements/School Projects) | Hidden (auto) | 17 |
| Diploma / ITI | Medium | Visible | Visible | 19 |
| Undergraduate | Hard | Visible | Visible | 21 |
| Postgraduate | Hard | Visible | Visible | 23 |
| Professional | Hard | Visible | Visible | 24 |

---

## 🗃 Database Schema

15 normalized tables in `career_system_db`:

| # | Table | Purpose |
|---|---|---|
| 1 | `users` | All users — auth, demographics, role |
| 2 | `student_profiles` | Bio, LinkedIn, GitHub, portfolio links |
| 3 | `education_profiles` | Degree, CGPA, avg_marks, year_of_study, board, stream |
| 4 | `subject_marks` | Subject-wise marks per assessment |
| 5 | `question_bank` | 200+ MCQs filtered by level/board/stream |
| 6 | `assessment_sessions` | Each assessment attempt record |
| 7 | `assessment_answers` | Individual MCQ answers per session |
| 8 | `feature_scores` | Computed ML feature scores per session |
| 9 | `skills` | Master skills list (53 skills) |
| 10 | `skill_verification` | Quiz-verified skill proficiency per user |
| 11 | `projects` | Student project / school activity portfolio |
| 12 | `certifications` | Certifications / achievements |
| 13 | `career_predictions` | ML output — top-5 careers, SHAP JSON, feature JSON |
| 14 | `career_history` | Historical prediction log (for trend charts) |
| 15 | `roadmaps` | 30 career roadmaps (steps, resources, certs) |

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register new student |
| POST | `/api/auth/login` | Public | Login — returns JWT |
| GET | `/api/auth/me` | JWT | Get current user |
| GET | `/api/questions` | Public | Fetch adaptive aptitude questions |
| POST | `/api/assessment/submit` | JWT | Submit assessment → ML predictions |
| GET | `/api/dashboard` | JWT | Career results + SHAP + history |
| GET | `/api/history` | JWT | All past assessments |
| POST | `/api/skills/verify` | JWT | Save skill quiz result |
| GET | `/api/profile` | JWT | Get user profile |
| PUT | `/api/profile/update` | JWT | Update profile |
| GET | `/api/admin/stats` | Admin | Dashboard statistics |
| POST | `/api/admin/retrain` | Admin | Trigger model retraining |
| GET | `/api/health` | Public | System health check |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- MySQL 8.x (running locally)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/career-recommendation-system.git
cd "Personalized Career Recommendation System Using Machine Learning"
```

### 2. Set Up Database

```bash
mysql -u root -p < backend/career_system_db.sql
```

This creates the `career_system_db` database with all 15 tables, seeds the admin user, and inserts 30 career roadmaps.

### 3. Configure Environment

Edit `backend/.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_system_db
JWT_SECRET=your_secret_key_here
```

### 4. Set Up Python Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Verify ML Models

Ensure `backend/models/` contains all `.pkl` files.  
If models are missing, the system runs in **mock prediction mode** (interest-based fallback).

---

## 🔐 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | MySQL host |
| `DB_USER` | `root` | MySQL username |
| `DB_PASSWORD` | `abc123` | MySQL password |
| `DB_NAME` | `career_system_db` | Database name |
| `JWT_SECRET` | `career_super_secret_key_2026` | JWT signing secret |

> ⚠️ Change `JWT_SECRET` and `DB_PASSWORD` before deploying to production.

---

## 🚀 Running the Project

### Option 1 — One-click (Windows)

```
Double-click start.bat
```

### Option 2 — Manual

```bash
cd backend
venv\Scripts\activate
python app.py
```

App runs at **http://localhost:5000**

| URL | Page |
|---|---|
| `/` | Landing page |
| `/register.html` | Student registration |
| `/login.html` | Student login |
| `/assessment.html` | Career assessment |
| `/dashboard.html` | Results dashboard |
| `/history.html` | Assessment history |
| `/admin-login.html` | Admin login |
| `/admin.html` | Admin panel |

**Default Admin:** `admin@gmail.com` / `Admin@123`

---

## 🎯 Tips for High Confidence Predictions (>90%)

| Step | What to do |
|---|---|
| Step 2 (Marks) | Enter all subject marks ≥ 75 |
| Step 3 (Aptitude) | Score 8/10 or higher |
| Step 4 (Psychometric) | Answer consistently toward one personality type |
| **Step 5 (Interests)** | **Choose 80%+ of pairs toward ONE domain — biggest factor** |
| Step 6 (Skills) | Select 6–10 skills; pass quiz at Intermediate or Advanced |

---

## 🏆 Supported Careers (30)

| Technology | Business | Healthcare | Engineering | Other |
|---|---|---|---|---|
| Software Developer | Business Analyst | Doctor | Mechanical Engineer | School Teacher |
| Data Scientist | Entrepreneur | Nurse | Civil Engineer | Professor / Researcher |
| ML Engineer | Chartered Accountant | Pharmacist | Electrical Engineer | Lawyer |
| AI Engineer | Bank Manager | Biomedical Engineer | Agricultural Scientist | Architect |
| Full Stack Developer | Product Manager | | Environmental Scientist | Animator |
| Data Analyst | | | | Graphic Designer |
| Cyber Security Analyst | | | | UI/UX Designer |
| Cloud Architect | | | | |

---

## 🛡 Admin Panel

Access at `/admin.html` after admin login.

- 📊 Total students, assessments, questions
- 🏆 Top 10 career distribution chart
- 📈 Daily assessment trend (last 30 days)
- 🔄 Model retraining trigger

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| assessment.js size | ~143 KB / ~1,900 lines |
| app.py size | ~1,984 lines |
| ML features | 72 |
| Skill quizzes | 53 skills × 3 questions each |
| Career classes predicted | 30 |
| Database tables | 15 |
| Career roadmaps seeded | 30 |
| Aptitude question bank | 200+ questions |

---

*Built with ❤️ — AI-powered career guidance for every student, from Class 7 to PhD.*

<div align="center">

<h1>🎓 Personalized Career Recommendation System</h1>

<p><b>An intelligent, full-stack AI career guidance platform that delivers personalized career recommendations<br>through adaptive multi-step assessments, a 4-model ML ensemble, and explainable AI (SHAP).</b></p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/XGBoost-189FDD?style=for-the-badge&logo=xgboost&logoColor=white" />
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/github/stars/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning?style=social" />
  <img src="https://img.shields.io/github/forks/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning?style=social" />
  <img src="https://img.shields.io/badge/License-Academic-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" />
</p>

</div>

---

## 📌 Table of Contents

| # | Section |
|---|---|
| 1 | [Overview](#-overview) |
| 2 | [Key Features](#-key-features) |
| 3 | [System Architecture](#-system-architecture) |
| 4 | [Assessment Flow](#-9-step-assessment-flow) |
| 5 | [ML Architecture & Feature Engineering](#-ml-architecture--feature-engineering) |
| 6 | [Education Level Adaptations](#-education-level-adaptations) |
| 7 | [Database Schema](#-database-schema) |
| 8 | [API Endpoints](#-api-endpoints) |
| 9 | [Supported Careers](#-supported-careers-30) |
| 10 | [Setup & Installation](#-setup--installation) |
| 11 | [High Confidence Tips](#-tips-for-90-prediction-confidence) |

---

## 🔍 Overview

The **Personalized Career Recommendation System** is an end-to-end AI-powered platform designed to help students — from **Class 7 through postgraduate** — discover the most suitable careers for them.

It works in three phases:

> **Phase 1 — Assess**: The student completes an adaptive 8-step assessment covering academic marks, aptitude, psychometrics, career interests, and verified skills.

> **Phase 2 — Predict**: A 72-feature vector is constructed and passed through a soft-voting ensemble of **XGBoost + CatBoost + LightGBM + RandomForest**, producing top-5 career predictions with confidence percentages.

> **Phase 3 — Explain**: **SHAP (SHapley Additive exPlanations)** values are computed live and displayed on the dashboard as a feature attribution bar chart, helping students understand *why* a career was recommended.

The system is fully **board-aware** (CBSE, Kerala State, ICSE), **age-aware** (Class 7 → 12yrs, Class 10 → 15yrs), and **school-level adaptive** (automatically skips irrelevant steps for younger students).

---

## ✨ Key Features

### 🧠 Machine Learning & AI
| Feature | Details |
|---|---|
| **4-Model Ensemble** | XGBoost + CatBoost + LightGBM + RandomForest (soft-vote) |
| **Feature Vector** | 72 features spanning 10 categories |
| **SHAP Explainability** | TreeExplainer on XGBoost — live per-prediction attribution |
| **30 Career Classes** | Confidence % for each of the top 5 |
| **Readiness Score** | Composite 0–100 score indicating career preparedness |
| **Mock Mode** | Graceful interest-based fallback if model files are missing |

### 📋 Adaptive Assessment
| Step | Content | School Adaptation |
|---|---|---|
| Step 1 | Education Profile (level, board, stream, degree) | CGPA hidden; auto-derived |
| Step 2 | Subject-wise Marks (auto-loaded by board) | Kerala=10 subjects, CBSE=5 subjects |
| Step 3 | Aptitude Quiz (10 questions) | Difficulty adapts by class level |
| Step 4 | Psychometric Scenarios (6 questions) | Age-appropriate scenario banks |
| Step 5 | Career Interest Profiling (20+ pairs) | Same across all levels |
| Step 6 | Skill Verification Quizzes (53 skills) | Same across all levels |
| Step 7 | Certifications / Achievements | 🛑 SKIPPED for Class 7–10 |
| Step 8 | Projects & Portfolio | 🛑 SKIPPED for Class 7–10 |
| Step 9 | Results — Top 5 Careers + SHAP + Roadmap | Rendered for all levels |

### 🎯 Skill Verification (53 Skills)
- Each selected skill triggers a **3-question quiz** before being accepted
- Proficiency levels: **Beginner (33pts) / Intermediate (66pts) / Advanced (100pts)**
- Skills not in the quiz bank fall back to a **self-rating modal**
- Score feeds directly into `Subject_Knowledge_Score` feature in the ML vector

---

## 🏗 System Architecture

```mermaid
graph TD
    A(["👨‍🎓 Student / User"]):::user -->|"Opens App"| B["🌐 Frontend\nHTML + CSS + JS"]:::frontend
    B -->|"Step 1-8 Data"| C{{"⚙️ Flask\nBackend API"}}:::backend
    C -->|"Store raw data"| D[("🗄️ MySQL\nDatabase\n15 Tables")]:::db
    C -->|"Build 72-feature\nvector"| E["🔢 Feature\nEngineering\nPipeline"]:::ml

    subgraph ML ["🤖 ML Ensemble (Soft Voting)"]
        E --> F["📊 XGBoost"]:::xgb
        E --> G["🐱 CatBoost"]:::cat
        E --> H["💡 LightGBM"]:::lgb
        E --> I["🌲 RandomForest"]:::rf
        F --> J{{"🗳️ Weighted\nSoft Vote"}}:::vote
        G --> J
        H --> J
        I --> J
    end

    J -->|"Top 5 Careers\n+ Confidence %"| C
    F -->|"Live SHAP\nExplainer"| K["📈 SHAP\nAttributions"]:::shap
    K --> C
    C -->|"Predictions +\nSHAP + Roadmap"| B
    B -->|"Career Results\nDashboard"| A

    classDef user fill:#4CAF50,stroke:#2E7D32,color:white,stroke-width:2px
    classDef frontend fill:#2196F3,stroke:#1565C0,color:white,stroke-width:2px
    classDef backend fill:#FF9800,stroke:#E65100,color:white,stroke-width:2px
    classDef db fill:#9C27B0,stroke:#6A1B9A,color:white,stroke-width:2px
    classDef ml fill:#607D8B,stroke:#37474F,color:white,stroke-width:2px
    classDef xgb fill:#189FDD,stroke:#0D7AB5,color:white,stroke-width:2px
    classDef cat fill:#FFCA28,stroke:#F9A825,color:#333,stroke-width:2px
    classDef lgb fill:#66BB6A,stroke:#388E3C,color:white,stroke-width:2px
    classDef rf fill:#8D6E63,stroke:#5D4037,color:white,stroke-width:2px
    classDef vote fill:#EF5350,stroke:#C62828,color:white,stroke-width:2px
    classDef shap fill:#AB47BC,stroke:#7B1FA2,color:white,stroke-width:2px
```

---

## 📝 9-Step Assessment Flow

```mermaid
flowchart TD
    S([🚀 Start Assessment]) --> S1

    S1["📚 Step 1\nEducation Profile\nLevel · Board · Stream · Degree"] --> S2

    S2["📊 Step 2\nSubject Marks\nKerala: 10 Subjects\nCBSE: 5 Subjects\nICBSE: 6 Subjects"] --> S3

    S3["🧮 Step 3\nAptitude Quiz\n10 Questions\nDifficulty = f(Class Level)"] --> S4

    S4["🧠 Step 4\nPsychometric Scenarios\n6 Age-Appropriate Questions\nMaps to 15 Personality Traits"] --> S5

    S5["🎯 Step 5\nCareer Interest Profiling\n20+ Forced-Choice Pairs\n10 Career Domains"] --> S6

    S6["🛠️ Step 6\nSkill Verification\n53 Skills Available\n3-Question Quiz per Skill"] --> CHECK

    CHECK{Education Level?}

    CHECK -->|Class 7–10| SKIP7["⏭️ Skip Step 7\nSkip Step 8"]
    CHECK -->|Class 11–12| S7A["🏅 Step 7\nAchievements\nOlympiads · Awards"]
    CHECK -->|UG / PG| S7B["📜 Step 7\nCertifications\nAWS · Google · NPTEL"]

    SKIP7 --> S9
    S7A --> S8A["🔬 Step 8\nSchool Projects\nScience Fair · Club Activities"]
    S7B --> S8B["💼 Step 8\nProjects & Portfolio\nGitHub · Internships"]

    S8A --> S9
    S8B --> S9

    S9(["🏆 Step 9\nML Prediction\nTop-5 Careers + SHAP + Roadmap"])

    style S fill:#4CAF50,color:white,stroke:#2E7D32
    style S9 fill:#E91E63,color:white,stroke:#880E4F
    style CHECK fill:#FF9800,color:white,stroke:#E65100
    style SKIP7 fill:#F44336,color:white,stroke:#B71C1C
    style S1 fill:#1E88E5,color:white,stroke:#0D47A1
    style S2 fill:#1E88E5,color:white,stroke:#0D47A1
    style S3 fill:#1E88E5,color:white,stroke:#0D47A1
    style S4 fill:#1E88E5,color:white,stroke:#0D47A1
    style S5 fill:#1E88E5,color:white,stroke:#0D47A1
    style S6 fill:#1E88E5,color:white,stroke:#0D47A1
    style S7A fill:#7B1FA2,color:white,stroke:#4A148C
    style S7B fill:#7B1FA2,color:white,stroke:#4A148C
    style S8A fill:#7B1FA2,color:white,stroke:#4A148C
    style S8B fill:#7B1FA2,color:white,stroke:#4A148C
```

---

## 🤖 ML Architecture & Feature Engineering

### Ensemble Weighting
The final prediction is a **weighted soft vote** across all 4 models. Weights are saved in `ensemble_weights.pkl` and loaded at startup.

```
Final Probability = (w_xgb × P_xgb) + (w_cb × P_cb) + (w_lgb × P_lgb) + (w_rf × P_rf)
Confidence %      = max(Final Probability) × 100
```

### 72-Feature Vector Breakdown

| # | Category | Features | Count |
|---|---|---|---|
| 1 | 📚 **Academic** | CGPA, Avg Marks, Semester Marks, Internal Marks, Practical Marks, Lab Score, Assignment Score | 7 |
| 2 | 🧮 **Aptitude** | Logical Reasoning, Numerical Ability, Verbal Ability, Spatial Ability | 4 |
| 3 | 🧠 **Psychometric** | Leadership, Teamwork, Communication, Creativity, Problem Solving, Critical Thinking, Adaptability, Decision Making, Time Management, Curiosity, Analytical, Stress Management, Self Learning, Persistence, Confidence | 15 |
| 4 | 🎯 **Career Interest** | Technology, Healthcare, Business, Arts/Creative, Research, Education, Engineering, Law, Environment, Social Service | 10 |
| 5 | 🛠️ **Skills** | Num_Technical_Skills, Subject_Knowledge_Score | 2 |
| 6 | 🏅 **Activities** | Num_Projects, Num_Certifications, Internships, Hackathons, Research Experience, Competitions, Volunteer Work | 7 |
| 7 | ⚗️ **Engineered** | STEM signal, Health signal, Biz signal, Creative signal, Research signal, Activity richness, Soft composite, Weighted Academic, Interest spread, Dominant Interest, Total Aptitude | 11 |
| 8 | 👤 **Demographics** | Age, Year of Study | 2 |
| 9 | 📈 **Derived Scores** | Readiness Score, Activity Score, Soft Skill Score, Academic Composite | 4 |
| 10 | 📋 **Other** | Attendance %, Skill Verified Score, Programming Score | 3 |
| | | **Total** | **72** |

### School-Level Smart Defaults
When a school student (Class 7–12) submits, the backend automatically:

| Field | School Default | Logic |
|---|---|---|
| `cgpa` | Derived | `avg_marks ÷ 10` |
| `attendance_pct` | 85 | Auto-set |
| `project_score` | 0 | Steps 7–8 skipped |
| `cert_count` | 0 | Steps 7–8 skipped |
| `age` | Class-derived | Class 7→12, Class 10→15, Class 12→17 |
| `year_of_study` | Class-derived | Class 7→1, Class 10→4, Class 12→6 |

---

## 🏫 Education Level Adaptations

| Level | Aptitude | Psychometric Bank | Steps 7–8 | CGPA | Attendance | Age Default |
|---|---|---|---|---|---|---|
| **Class 7** | Easy | School-level | 🛑 Skipped | Hidden (auto) | Hidden (85%) | 12 |
| **Class 8** | Easy | School-level | 🛑 Skipped | Hidden (auto) | Hidden (85%) | 13 |
| **Class 9** | Medium | School-level | 🛑 Skipped | Hidden (auto) | Hidden (85%) | 14 |
| **Class 10** | Medium | School-level | 🛑 Skipped | Hidden (auto) | Hidden (85%) | 15 |
| **Class 11–12** | Medium-Hard | Teen-level | 🔄 Adapted | Hidden (auto) | Hidden (85%) | 17 |
| **Diploma / ITI** | Medium | College-level | ✅ Visible | ✅ Visible | ✅ Visible | 19 |
| **Undergraduate** | Hard | Professional | ✅ Visible | ✅ Visible | ✅ Visible | 21 |
| **Postgraduate** | Hard | Research-level | ✅ Visible | ✅ Visible | ✅ Visible | 23 |
| **Professional** | Hard | Executive | ✅ Visible | ✅ Visible | ✅ Visible | 24 |

---

## 🗃 Database Schema

The project uses a highly normalized relational MySQL database with **15 tables**.

### Entity-Relationship Diagram

```mermaid
erDiagram
    USERS {
        int id PK
        varchar full_name
        varchar email
        varchar password_hash
        varchar role
        int age
        varchar gender
        varchar state
    }
    STUDENT_PROFILES {
        int id PK
        int user_id FK
        text bio
        varchar linkedin_url
        varchar github_url
    }
    EDUCATION_PROFILES {
        int id PK
        int user_id FK
        varchar education_level
        varchar board
        varchar stream
        varchar degree
        float cgpa
        float avg_marks
        int year_of_study
        float attendance_pct
    }
    ASSESSMENT_SESSIONS {
        int id PK
        int user_id FK
        varchar session_token
        varchar status
        timestamp started_at
        timestamp completed_at
    }
    ASSESSMENT_ANSWERS {
        int id PK
        int session_id FK
        int question_id
        varchar category
        tinyint is_correct
    }
    CAREER_PREDICTIONS {
        int id PK
        int user_id FK
        int session_id FK
        varchar top1_career
        float top1_confidence
        longtext top5_careers_json
        longtext shap_json
        longtext feature_scores_json
        float readiness_score
    }
    SKILL_VERIFICATION {
        int id PK
        int user_id FK
        varchar skill_name
        float score
        varchar level
    }
    QUESTION_BANK {
        int id PK
        text question_text
        varchar category
        varchar difficulty
        varchar education_level
        varchar board
        varchar stream
    }
    ROADMAPS {
        int id PK
        varchar career
        longtext steps_json
        text certifications
        text resources
    }

    USERS ||--o{ STUDENT_PROFILES : "has profile"
    USERS ||--o{ EDUCATION_PROFILES : "has education"
    USERS ||--o{ ASSESSMENT_SESSIONS : "starts"
    ASSESSMENT_SESSIONS ||--o{ ASSESSMENT_ANSWERS : "contains"
    USERS ||--o{ CAREER_PREDICTIONS : "receives"
    USERS ||--o{ SKILL_VERIFICATION : "verifies"
    CAREER_PREDICTIONS ||--|| ROADMAPS : "maps to roadmap"
    QUESTION_BANK ||--o{ ASSESSMENT_ANSWERS : "sources"
```

### All 15 Tables

| # | Table | Purpose |
|---|---|---|
| 1 | `users` | All users (students + admins) — auth, demographics, role |
| 2 | `student_profiles` | Bio, LinkedIn, GitHub, portfolio links |
| 3 | `education_profiles` | Degree, CGPA, avg_marks, year_of_study, board, stream |
| 4 | `subject_marks` | Individual subject marks per assessment session |
| 5 | `question_bank` | 200+ MCQs — filtered by education level, board, stream |
| 6 | `assessment_sessions` | Each assessment attempt — token, status, timestamps |
| 7 | `assessment_answers` | Individual MCQ answers (correct / incorrect) |
| 8 | `feature_scores` | Computed ML features per session (stored separately) |
| 9 | `skills` | Master skills catalogue (53 skills seeded on startup) |
| 10 | `skill_verification` | Quiz-verified skill proficiency per user |
| 11 | `projects` | Student projects / school activity portfolio |
| 12 | `certifications` | Certifications and achievements |
| 13 | `career_predictions` | ML output — top-5 careers, SHAP JSON, full feature JSON |
| 14 | `career_history` | Historical career prediction log (for dashboard trend chart) |
| 15 | `roadmaps` | 30 career roadmaps — 8-step paths, resources, certifications |

---

## 🔌 API Endpoints

### Auth Endpoints
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public | Register a new student account |
| `POST` | `/api/auth/login` | Public | Login and receive a JWT token |
| `GET` | `/api/auth/me` | JWT | Get the currently authenticated user |

### Assessment Endpoints
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/questions` | Public | Fetch adaptive aptitude MCQs (filtered by level/board/stream) |
| `POST` | `/api/assessment/submit` | JWT | Submit full 8-step assessment → triggers ML prediction |
| `GET` | `/api/history` | JWT | Retrieve all past assessment sessions |

### Profile & Skills
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/profile` | JWT | Get full user profile |
| `PUT` | `/api/profile/update` | JWT | Update profile information |
| `POST` | `/api/skills/verify` | JWT | Save a skill quiz result |

### Dashboard & Results
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/dashboard` | JWT | Get latest career predictions + SHAP + feature scores |

### Admin Endpoints
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/admin/stats` | Admin JWT | Total students, assessments, top career distribution |
| `POST` | `/api/admin/retrain` | Admin JWT | Trigger ML model retraining in background |

### System
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/health` | Public | System health — DB connection + ML model status |

---

## 🏆 Supported Careers (30)

<table>
<tr>
<th>💻 Technology</th>
<th>💼 Business</th>
<th>🏥 Healthcare</th>
<th>⚙️ Engineering</th>
<th>🎓 Other</th>
</tr>
<tr>
<td>Software Developer</td>
<td>Business Analyst</td>
<td>Doctor</td>
<td>Mechanical Engineer</td>
<td>School Teacher</td>
</tr>
<tr>
<td>Data Scientist</td>
<td>Entrepreneur</td>
<td>Nurse</td>
<td>Civil Engineer</td>
<td>Professor / Researcher</td>
</tr>
<tr>
<td>ML Engineer</td>
<td>Chartered Accountant</td>
<td>Pharmacist</td>
<td>Electrical Engineer</td>
<td>Lawyer</td>
</tr>
<tr>
<td>AI Engineer</td>
<td>Bank Manager</td>
<td>Biomedical Engineer</td>
<td>Agricultural Scientist</td>
<td>Architect</td>
</tr>
<tr>
<td>Full Stack Developer</td>
<td>Product Manager</td>
<td></td>
<td>Environmental Scientist</td>
<td>Animator</td>
</tr>
<tr>
<td>Data Analyst</td>
<td></td>
<td></td>
<td></td>
<td>Graphic Designer</td>
</tr>
<tr>
<td>Cyber Security Analyst</td>
<td></td>
<td></td>
<td></td>
<td>UI/UX Designer</td>
</tr>
<tr>
<td>Cloud Architect</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

Each career comes with:
- 📈 **Salary range** (Indian market, e.g. ₹5L–₹18L/yr)
- 🎓 **Required degree** (e.g. BTech CS / BCA)
- 🏢 **Top companies** (e.g. Infosys, Google, TCS)
- 📉 **Industry growth %** (e.g. +22% annually)
- 📜 **Recommended certifications** (e.g. AWS, Full Stack Cert)
- 🗺️ **8-step career roadmap**

---

## ⚙️ Setup & Installation

### Prerequisites
- Python **3.10+**
- MySQL **8.x** (running on localhost)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd "Personalized Career Recommendation System Using Machine Learning"
```

### 2. Set Up Database

```bash
mysql -u root -p < backend/career_system_db.sql
```

> Creates `career_system_db` with all 15 tables, seeds admin user, and inserts 30 career roadmaps.
> **Default admin:** `admin@gmail.com` / `Admin@123`

### 3. Configure Environment

Edit `backend/.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_system_db
JWT_SECRET=your_secret_key_here
```

### 4. Install Python Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Run the Application

**Windows (one-click):**
```
Double-click start.bat
```

**Manual:**
```bash
cd backend
python app.py
```

App runs at → **http://localhost:5000**

| Page | URL |
|---|---|
| 🏠 Landing | `http://localhost:5000/` |
| 📝 Register | `http://localhost:5000/register.html` |
| 🔑 Login | `http://localhost:5000/login.html` |
| 📋 Assessment | `http://localhost:5000/assessment.html` |
| 📊 Dashboard | `http://localhost:5000/dashboard.html` |
| 🕐 History | `http://localhost:5000/history.html` |
| 🛡️ Admin | `http://localhost:5000/admin.html` |

---

## 🎯 Tips for 90%+ Prediction Confidence

| Priority | Step | What to Do |
|---|---|---|
| ⭐⭐⭐ | **Step 5 — Interests** | Choose 80%+ of pairs toward **one domain** — this is the single biggest factor |
| ⭐⭐⭐ | **Step 3 — Aptitude** | Score 8/10 or higher |
| ⭐⭐ | **Step 6 — Skills** | Select 6–10 skills, pass each quiz at Intermediate or Advanced |
| ⭐⭐ | **Step 2 — Marks** | Enter subject marks ≥ 75 |
| ⭐ | **Step 4 — Psychometric** | Answer all 6 scenarios consistently toward one personality type |

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| ML Features | 72 |
| Career Classes | 30 |
| Skill Quizzes | 53 skills × 3 questions |
| Aptitude Questions | 200+ (multi-level bank) |
| Database Tables | 15 |
| Career Roadmaps | 30 (8-step each) |
| Assessment Steps | 9 (adaptive — 7 for school students) |
| Backend Lines of Code | ~1,984 lines |
| Assessment Engine (JS) | ~143 KB |

---

<div align="center">
  <p>⭐ If this project helped you, please consider giving it a star on GitHub!</p>
  <p><i>Built with ❤️ — AI-powered career guidance for every student, from Class 7 to PhD.</i></p>
</div>

# AI Career Recommendation System

> **AI-powered career guidance for students from Class 7 to Postgraduate.**
> Takes a 9-step adaptive assessment and returns your top-5 personalised career matches with full AI explainability — all running from one command.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-3.3.0-FF6600?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

</div>

---

## Table of Contents

- [What is this?](#what-is-this)
- [Quick Start](#quick-start-5-minutes)
- [Default Credentials](#default-login-credentials)
- [What it does](#what-it-does)
- [Pages](#pages)
- [How it works](#how-it-works)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [ML Model Details](#ml-model-details)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [License](#license)

---

## What is this?

Students often struggle to pick the right career. This system solves that by:

1. Asking the student a smart adaptive quiz (difficulty adjusts in real time)
2. Scoring **61 features** — academics, psychometric traits, skills, and interests
3. Running those features through a trained **XGBoost ML model**
4. Returning the **top-5 best-fit careers** with confidence percentages
5. Explaining *why* each career was recommended using **SHAP (Explainable AI)**

Everything — the web app, the REST API, and the ML engine — runs from a **single Python command**.

---

## Quick Start (5 minutes)

### What you need before starting

| Tool | Version | Download |
|---|---|---|
| Python | 3.10 or higher | [python.org](https://www.python.org/downloads/) |
| MySQL | 8.0 or higher | [mysql.com](https://dev.mysql.com/downloads/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

> **No Node.js needed.** The frontend is plain HTML/CSS/JavaScript served directly by Flask.

---

### Step 1 — Get the code

```bash
git clone https://github.com/AMB-007/Career_Recommendation_System.git
cd Career_Recommendation_System
```

---

### Step 2 — Set up the database

Open your MySQL client and run:

```sql
CREATE DATABASE career_system_db;
```

> The app automatically creates all 15 tables on first launch. No SQL import needed unless you want sample data.

---

### Step 3 — Create a Python virtual environment

```bash
# Go into the backend folder
cd backend

# Create the virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Return to the project root
cd ..
```

---

### Step 4 — Configure your database password

Create a file called `.env` inside the `backend/` folder:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=career_system_db
JWT_SECRET=career_super_secret_key_2026
```

> Replace `your_mysql_password_here` with your actual MySQL password.

---

### Step 5 — Launch the app

From the **project root** folder, run:

```bash
python app.py
```

You will see:

```
============================================================
  AI Career Recommendation System
  Starting server...
============================================================
[OK] Database initialised.

  Frontend + Backend running at: http://127.0.0.1:5000
  API health check:              http://127.0.0.1:5000/api/health
  Press CTRL+C to stop.
```

Open **http://127.0.0.1:5000** in your browser. Done!

---

### Step 6 — Verify everything works

Visit this URL in your browser or Postman:

```
GET http://localhost:5000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "ml_loaded": true,
  "message": "Career Recommendation System API is running"
}
```

---

## Default Login Credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@gmail.com` | `Admin@123` |

> Change the admin password after your first login.

---

## What it does

| Feature | Details |
|---|---|
| Adaptive Assessment | 200+ questions that adjust based on your education level, stream, and board |
| ML Career Prediction | XGBoost model trained on 35,000+ records across 272 career labels |
| SHAP Explainability | Shows exactly which factors (skills, marks, traits) influenced each recommendation |
| Top-5 Career Results | Ranked career matches with confidence percentages |
| Career Readiness Score | A single composite score showing how job-ready you are today |
| Learning Roadmap | Step-by-step path to reach your recommended career |
| Prediction History | View all past assessments and how your profile changed over time |
| Admin Dashboard | Manage users, edit the question bank, and view platform analytics |
| JWT Authentication | Secure login with role-based access (Student vs Admin) |
| Dark / Light Mode | Theme preference is saved across sessions |
| Single Command Launch | `python app.py` starts the entire system — no separate frontend server needed |

---

## Pages

| URL | Page | Needs Login |
|---|---|---|
| `/` | Home — landing page | No |
| `/register.html` | Create a student account | No |
| `/login.html` | Student login | No |
| `/admin-login.html` | Admin login | No |
| `/assessment.html` | 9-step career assessment wizard | Yes |
| `/test.html` | Adaptive aptitude quiz | Yes |
| `/dashboard.html` | Your ML results, SHAP chart, and roadmap | Yes |
| `/history.html` | Past prediction history | Yes |
| `/settings.html` | Profile and account settings | Yes |
| `/admin.html` | Admin portal | Admin only |

---

## How it works

```
Student fills the assessment form
              |
              v
   Flask API receives 61 input features
              |
              v
   OrdinalEncoder  +  StandardScaler
   (categorical)       (numerical)
              |
              v
       XGBoost Classifier
              |
         _____|_____
        |           |
     Top-5       SHAP Explainer
   Careers +    (why each career
   Confidence    was recommended)
        |           |
        |___________|
              |
              v
   Saved to MySQL  -->  Shown on Dashboard
```

> If the ML model fails to load (e.g. Python version mismatch), the system automatically falls back to a rule-based heuristic engine. The UI never breaks.

---

## Project Structure

```
Career_Recommendation_System/
|
|-- app.py                     <-- START HERE: run this to launch everything
|
|-- backend/
|   |-- app.py                 Flask application (all API routes, ML logic, DB)
|   |-- requirements.txt       Python dependencies
|   |-- .env                   Your database credentials (never commit this)
|   |-- career_system_db.sql   SQL schema backup (optional)
|   |
|   |-- core/
|   |   `-- db_config.py       Database connection helper
|   |
|   `-- models/                Trained ML files (auto-loaded at startup)
|       |-- career_model.pkl       The trained XGBoost model
|       |-- label_encoder.pkl      Career name encoder
|       |-- ordinal_encoder.pkl    Categorical feature encoder
|       |-- scaler.pkl             Numerical feature scaler
|       |-- feature_columns.pkl    All 61 feature names in order
|       |-- shap_explainer.pkl     Pre-computed SHAP explainer
|       `-- career_dataset.csv     Training dataset (35K+ rows, 272 careers)
|
|-- frontend/
|   `-- dist/                  Web pages (served by Flask automatically)
|       |-- index.html
|       |-- login.html
|       |-- register.html
|       |-- assessment.html
|       |-- dashboard.html
|       |-- history.html
|       |-- settings.html
|       |-- admin.html
|       |-- css/style.css      Global design system and theme
|       `-- js/
|           |-- app.js         Shared utilities (auth, theme, navbar)
|           |-- home.js
|           |-- assessment.js
|           |-- dashboard.js
|           |-- history.js
|           |-- settings.js
|           `-- admin.js
|
`-- README.md
```

---

## Database Schema

All 15 tables are created automatically on first run. No manual SQL import needed.

| Table | What it stores |
|---|---|
| `users` | Student and admin accounts |
| `student_profiles` | Bio, LinkedIn, GitHub, portfolio links |
| `education_profiles` | Degree, stream, board, CGPA, attendance |
| `subject_marks` | Marks per subject per semester |
| `question_bank` | The 200+ adaptive MCQ questions |
| `assessment_sessions` | Each time a student starts an assessment |
| `assessment_answers` | Each answer given during an assessment |
| `feature_scores` | The 61 computed ML input features per session |
| `skills` | Master skill catalog |
| `skill_verification` | Which skills a student has verified and at what level |
| `projects` | Student project portfolio |
| `certifications` | Student certifications |
| `career_predictions` | ML output — top-5 careers + SHAP values |
| `career_history` | Timeline of all past predictions |
| `roadmaps` | Learning roadmaps per career path |

---

## ML Model Details

### Input Features (61 total)

| Category | Examples | Count |
|---|---|---|
| Demographics | Age, Gender, Country, State | 4 |
| Academics | CGPA, Attendance %, Semester Marks | 3 |
| Education Context | Level, Board, Stream, Degree, Specialization | 5 |
| Aptitude Scores | Logical, Numerical, Verbal, Spatial | 4 |
| Psychometric Traits | Leadership, Teamwork, Curiosity, Creativity, Resilience, Problem Solving... | 8 |
| Interest Scores | AI, Technology, Healthcare, Business, Arts, Research, Law, Engineering... | 10 |
| Skill Scores | Programming, Science, Business, Creative, Medical | 7 |
| Certifications & Projects | Cert score, Project score, Internship score, Verified skill score | 4 |
| Computed | Academic composite score, Career readiness composite | 2+ |

### Output: 272 Career Labels

Covers every major field — Software Engineering, Medicine, Law, Design, Finance, Research, Education, and more.

---

## API Reference

**Base URL:** `http://localhost:5000`

Protected endpoints require this header:
```
Authorization: Bearer <your_jwt_token>
```

---

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/health` | None | Check if the server is running |
| POST | `/api/auth/register` | None | Create a new student account |
| POST | `/api/auth/login` | None | Login and get a JWT token |

#### Register — `POST /api/auth/register`

```json
{
  "full_name": "Arjun Sharma",
  "email": "arjun@example.com",
  "password": "MyPass@123",
  "phone": "9876543210",
  "age": 20,
  "gender": "Male",
  "country": "India",
  "state": "Karnataka",
  "institution": "RV College of Engineering"
}
```

#### Login — `POST /api/auth/login`

Request:
```json
{ "email": "arjun@example.com", "password": "MyPass@123" }
```

Response:
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "user": { "id": 1, "full_name": "Arjun Sharma", "role": "student" }
}
```

---

### Student Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/user/profile` | Student JWT | Get your full profile |
| PUT | `/api/user/profile` | Student JWT | Update your profile |
| GET | `/api/dashboard` | Student JWT | Get your latest career prediction results |
| GET | `/api/history` | Student JWT | Get all your past predictions |

---

### Assessment

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/questions` | None | Fetch questions (filter by level, board, stream) |
| POST | `/api/assessment/submit` | Optional | Submit answers and trigger ML prediction |

#### Submit Assessment — `POST /api/assessment/submit`

Request:
```json
{
  "education_level": "Undergraduate",
  "degree": "BTech",
  "specialization": "Computer Science",
  "cgpa": 8.5,
  "attendance": 85,
  "semester_marks": 78,
  "psychometric_traits": {
    "leadership": 4,
    "teamwork": 5,
    "curiosity": 5,
    "creativity": 3
  },
  "interest_scores": {
    "ai_interest": 5,
    "technology_interest": 5,
    "business_interest": 2
  },
  "skill_scores": { "Python": 4, "Machine Learning": 3 },
  "certifications": ["AWS Certified"],
  "projects": ["ML Sentiment Analyser"]
}
```

Response:
```json
{
  "status": "success",
  "top_career": "Data Scientist",
  "top5": [
    { "career": "Data Scientist",  "confidence": 0.87 },
    { "career": "ML Engineer",     "confidence": 0.76 },
    { "career": "AI Researcher",   "confidence": 0.61 },
    { "career": "Data Analyst",    "confidence": 0.54 },
    { "career": "Cloud Architect", "confidence": 0.48 }
  ],
  "readiness_score": 82.4,
  "shap_top_features": [
    { "feature": "AI Interest",       "value": 0.34 },
    { "feature": "Programming Score", "value": 0.28 }
  ]
}
```

---

### Admin Endpoints (Admin JWT required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/users` | List all registered users |
| PUT | `/api/admin/users/<id>/role` | Change a user's role (student or admin) |
| DELETE | `/api/admin/users/<id>` | Delete a user account |
| GET | `/api/admin/questions` | List all questions in the question bank |
| POST | `/api/admin/questions` | Add a new question |
| PUT | `/api/admin/questions/<id>` | Edit an existing question |
| DELETE | `/api/admin/questions/<id>` | Remove a question |
| GET | `/api/admin/analytics` | Platform stats — users, assessments, top careers |

---

## Environment Variables

Create `backend/.env` with these values:

| Variable | What it does | Default |
|---|---|---|
| `DB_HOST` | MySQL server address | `localhost` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | *(required)* |
| `DB_NAME` | MySQL database name | `career_system_db` |
| `JWT_SECRET` | Secret key used to sign login tokens | `career_super_secret_key_2026` |

> **Important:** Never push your `.env` file to GitHub. Add it to `.gitignore`.

---

## Development Notes

### Running the app

```bash
# From the project root (recommended)
python app.py

# Or run the backend directly (cd into backend/ first with venv active)
cd backend
python app.py
```

### Editing the frontend

No build tools needed. Edit any `.html`, `.css`, or `.js` file inside `frontend/dist/` and refresh your browser to see changes immediately.

### Adding Python packages

```bash
cd backend
pip install <package-name>
pip freeze > requirements.txt
```

---

## Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and commit: `git commit -m "feat: describe what you changed"`
4. Push and open a Pull Request

### Commit message guide

| Prefix | When to use |
|---|---|
| `feat:` | Adding a new feature |
| `fix:` | Fixing a bug |
| `docs:` | Documentation only changes |
| `refactor:` | Code cleanup with no behaviour change |
| `chore:` | Build scripts, dependency updates |

---

## License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">
Built with Python · Flask · XGBoost · SHAP · Vanilla HTML/CSS/JS · MySQL
</div>

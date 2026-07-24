# Personalized Career Recommendation System Using Machine Learning 🎓🤖

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-82.33%25%20Accuracy-orange.svg)](https://xgboost.readthedocs.io/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

An intelligent, web-based career guidance platform developed as an **MCA Major Project**. The system predicts the most suitable career path for students based on their academic scores, technical proficiencies, soft skills, personality traits, interests, and career preferences using an **XGBoost Machine Learning Classifier** achieving **82.33% accuracy** across 75 career domains.

---

## 📌 Project Overview & Objectives

Traditional career counseling often relies on subjective evaluations or generalized advice. This system provides a **data-driven, objective, and personalized career recommendation engine** leveraging machine learning models trained on **7,500 student profiles** across **157 input attributes**.

### Key Objectives:
- Predict Top-5 career recommendations with probability confidence scores.
- Evaluate academic performance, technical skills, soft skills, and interest profiles.
- Generate structured career growth roadmaps, recommended certifications, and industry salary insights.
- Provide a responsive executive dashboard for students and an analytics control panel for system administrators.

---

## ✨ System Features

### 👤 Student Features
- **Multi-Step Assessment Engine**: 8-section interactive assessment covering Personal Details, Academic Performance, Technical Skills, Soft Skills, Interests, Projects/Experience, Certifications, and Career Goals.
- **Top 5 Career Matches**: Real-time Machine Learning prediction with confidence percentages (e.g., 91.2% Match).
- **Career Roadmaps**: Phase-by-phase skill development roadmaps, required technologies, and hiring industry listings for 75 career fields.
- **Personal Profile & Skill Radar**: Interactive Chart.js radar charts visualizing 8 core soft skill dimensions against assessment history.
- **Bookmarks & PDF Reports**: Save favorite career paths and generate printable summary reports.
- **Feedback System**: Submit star-rating reviews and suggestions directly to system administrators.

### 🛡️ Admin Features
- **Executive Analytics Dashboard**: Real-time user statistics, total assessments generated, and system health metrics.
- **Career Demand Charts**: Bar chart visualizations of top-recommended careers across all student assessments.
- **User Demographics Breakdown**: Doughnut charts displaying education level distribution (B.Tech, MCA, Degree, Diploma, PhD).
- **User Management**: View user registration details, prediction history count, and delete accounts.
- **Data Export**: Export complete assessment and prediction history records as downloadable CSV reports.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, FontAwesome 6, Google Fonts (Inter) | Modern, responsive, flat executive UI |
| **Data Visualization** | Chart.js, SweetAlert2 | Interactive radar/bar/doughnut charts and smooth modal dialogs |
| **Backend Framework** | Python 3.14, Flask 2.x, Werkzeug | RESTful routing, session management, template rendering, and API handlers |
| **Machine Learning** | XGBoost 2.x, Scikit-Learn, Pandas, NumPy | Gradient Boosted Classifier trained on 157 features for multi-class prediction |
| **Database** | MySQL 8.0, mysql-connector-python | Relational database with connection pooling and normalized schema |
| **Security** | BCrypt (12 rounds) | Salted password hashing and session cookie security |

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Frontend                         │
│  Bootstrap 5 + FontAwesome + Chart.js + SweetAlert2     │
└────────────────────────────┬────────────────────────────┘
                             │ HTTP / JSON APIs
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    Flask Backend                        │
│  app.py ──► Session Management ──► BCrypt Hashing       │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌───────────────────────────┐
│     MySQL Database       │  │  XGBoost ML Engine        │
│  career_recommendation   │  │  predict.py (82.33% Acc)  │
│  (users, predictions...) │  │  xgboost_model.pkl        │
└──────────────────────────┘  └───────────────────────────┘
```

---

## 🤖 Machine Learning Model Details

- **Model Type**: XGBoost Classifier (`XGBClassifier`)
- **Dataset**: `career_recommendation_dataset_cleaned.csv` (7,500 student records)
- **Features Used**: 157 multi-dimensional profile attributes
- **Target Classes**: 75 unique career options (e.g. *AI Engineer, Data Scientist, Cybersecurity Analyst, Cloud Architect, IAS Officer, Chartered Accountant, UI/UX Designer*)
- **Accuracy**: **82.33%** on test evaluation set
- **Hyperparameters**:
  - `n_estimators`: 200
  - `max_depth`: 6
  - `learning_rate`: 0.1
  - `subsample`: 0.8
  - `colsample_bytree`: 0.8

---

## 🗄️ Database Schema (`career_recommendation`)

The normalized MySQL database consists of the following 7 core tables:

| # | Table | Description |
|---|---|---|
| 1 | `users` | Student accounts, hashed credentials, demographics, education level, CGPA |
| 2 | `prediction_history` | Recorded assessment predictions, top career name, confidence score, JSON Top-5 payload |
| 3 | `career_details` | Reference data for 75 careers including roadmaps, skills, certifications, salary range |
| 4 | `feedback` | User feedback, star rating scores (1–5), and support/contact messages |
| 5 | `bookmarked_careers` | Saved/bookmarked career paths per student |
| 6 | `login_history` | IP address, user agent, and timestamp audit logs for all login attempts |
| 7 | `admin_users` | Administrator credentials and access control |

---

## 🔍 Complete Database Queries Reference

All queries use **parameterized `%s` placeholders** to prevent SQL injection. They are executed via the centralized `execute_query()` helper in `app.py`.

### 🔐 User Authentication

```sql
-- Check if user exists and is active (Login)
SELECT * FROM users WHERE email = %s AND is_active = TRUE;

-- Check if email already registered (Registration)
SELECT user_id FROM users WHERE email = %s;

-- Create new student account (Registration)
INSERT INTO users
  (full_name, email, password_hash, age, gender, education_level,
   specialization, cgpa, profile_image, is_active, is_admin, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Fetch admin credentials (Admin Login)
SELECT * FROM admin_users WHERE email = %s;
```

---

### 📜 Login History Audit Log

```sql
-- Log successful login attempt
INSERT INTO login_history (user_id, ip_address, user_agent, success)
VALUES (%s, %s, %s, TRUE);

-- Log failed login attempt
INSERT INTO login_history (user_id, ip_address, user_agent, success)
VALUES (%s, %s, %s, FALSE);
```

---

### 🏠 Student Dashboard

```sql
-- Fetch logged-in user full profile
SELECT * FROM users WHERE user_id = %s;

-- Fetch last 5 career predictions
SELECT * FROM prediction_history
WHERE user_id = %s
ORDER BY created_at DESC
LIMIT 5;

-- Count total assessments completed
SELECT COUNT(*) as count FROM prediction_history WHERE user_id = %s;

-- Count total bookmarked careers
SELECT COUNT(*) as count FROM bookmarked_careers WHERE user_id = %s;
```

---

### 🤖 Career Prediction & Recommendations

```sql
-- Save a new prediction result
INSERT INTO prediction_history
  (user_id, career_name, confidence_score, recommendation_data, created_at)
VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);

-- Fetch a specific prediction by ID (owner-verified)
SELECT * FROM prediction_history
WHERE prediction_id = %s AND user_id = %s;

-- Fetch the latest prediction for a user
SELECT * FROM prediction_history
WHERE user_id = %s
ORDER BY created_at DESC
LIMIT 1;

-- Fetch career detail information by name
SELECT * FROM career_details WHERE career_name = %s;

-- Search careers by keyword
SELECT career_name, description FROM career_details
WHERE career_name LIKE %s
LIMIT 10;
```

---

### 👤 Student Profile Management

```sql
-- Get full user profile
SELECT * FROM users WHERE user_id = %s;

-- Get complete prediction history (profile page)
SELECT * FROM prediction_history
WHERE user_id = %s
ORDER BY created_at DESC;

-- Update student profile details
UPDATE users
SET full_name = %s,
    age = %s,
    education_level = %s,
    specialization = %s,
    cgpa = %s
WHERE user_id = %s;
```

---

### 💬 Feedback & Contact Form

```sql
-- Submit user feedback with star rating
INSERT INTO feedback (user_id, subject, message, rating)
VALUES (%s, %s, %s, %s);

-- Submit contact form (stored as feedback with rating 5)
INSERT INTO feedback (user_id, subject, message, rating)
VALUES (%s, %s, %s, 5);

-- Fetch user's past submitted feedback
SELECT * FROM feedback
WHERE user_id = %s
ORDER BY created_at DESC
LIMIT 5;
```

---

### 🔖 Career Bookmarks

```sql
-- Bookmark a career (upsert — prevents duplicate entries)
INSERT INTO bookmarked_careers (user_id, career_name)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE bookmarked_at = NOW();
```

---

### 🛡️ Admin Panel Queries

```sql
-- Total registered users count
SELECT COUNT(*) as count FROM users;

-- Total assessments/predictions count
SELECT COUNT(*) as count FROM prediction_history;

-- Total feedback submissions count
SELECT COUNT(*) as count FROM feedback;

-- 5 most recently registered users
SELECT * FROM users ORDER BY created_at DESC LIMIT 5;

-- All users with their prediction count (LEFT JOIN)
SELECT u.*, COUNT(p.prediction_id) as prediction_count
FROM users u
LEFT JOIN prediction_history p ON u.user_id = p.user_id
GROUP BY u.user_id
ORDER BY u.created_at DESC;

-- Latest 50 predictions with student name (JOIN)
SELECT p.*, u.full_name
FROM prediction_history p
JOIN users u ON p.user_id = u.user_id
ORDER BY p.created_at DESC
LIMIT 50;

-- All feedback with submitter name (LEFT JOIN)
SELECT f.*, u.full_name
FROM feedback f
LEFT JOIN users u ON f.user_id = u.user_id
ORDER BY f.created_at DESC
LIMIT 50;

-- Top 10 most recommended careers (aggregate)
SELECT career_name AS career, COUNT(*) AS count
FROM prediction_history
GROUP BY career_name
ORDER BY count DESC
LIMIT 10;

-- Education level distribution of all users (aggregate)
SELECT education_level AS level, COUNT(*) AS count
FROM users
WHERE education_level IS NOT NULL AND education_level != ''
GROUP BY education_level;

-- Export: Full prediction report with user info (CSV download)
SELECT p.prediction_id, u.full_name, u.email,
       p.career_name, p.confidence_score, p.created_at
FROM prediction_history p
JOIN users u ON p.user_id = u.user_id;

-- Delete a user account (Admin action)
DELETE FROM users WHERE user_id = %s;
```

---

## 📂 Project Directory Structure

```
Career_Recommendation_System/
│
├── backend/
│   ├── app.py                   # Main Flask Backend Server & API Routes
│   ├── config.py                # Database Credentials & App Settings
│   ├── predict.py               # ML Inference Engine & Input Preprocessor
│   ├── train_model.py           # XGBoost Training Script
│   ├── Dockerfile               # Container Deployment Spec
│   │
│   ├── model/                   # ML Model Artifacts
│   │   ├── career_recommendation_dataset_cleaned.csv
│   │   ├── xgboost_model.pkl
│   │   ├── label_encoder.pkl
│   │   └── feature_columns.pkl
│   │
│   ├── static/                  # Static Assets
│   │   ├── css/style.css        # Executive Flat Design System
│   │   ├── js/main.js           # Client-side Validation & Interactivity
│   │   └── images/
│   │       ├── default.png      # Default User Profile Avatar
│   │       └── favicon.ico      # Site Favicon
│   │
│   ├── templates/               # Jinja2 HTML Templates
│   │   ├── base.html            # Master Layout (Header & Footer)
│   │   ├── index.html           # Landing Page
│   │   ├── login.html           # Student Login
│   │   ├── register.html        # Student Registration
│   │   ├── dashboard.html       # Student Overview Dashboard
│   │   ├── assessment.html      # 8-Section Multi-Step Career Assessment
│   │   ├── recommendation.html  # Top 5 Career Predictions & Insights
│   │   ├── career_details.html  # Detailed Career Information Page
│   │   ├── profile.html         # Student Profile & Skill Radar Chart
│   │   ├── feedback.html        # System Feedback Form
│   │   ├── about.html           # Technical & Academic Details
│   │   ├── contact.html         # Support Page & FAQ Accordion
│   │   ├── admin_login.html     # Admin Portal Login
│   │   ├── admin_dashboard.html # Admin Control Panel & Analytics
│   │   ├── 404.html             # Page Not Found View
│   │   └── 500.html             # Server Error View
│   │
│   ├── logs/                    # Application Log Output (auto-created)
│   └── uploads/                 # Uploaded Files Directory (auto-created)
│
├── database/
│   └── career_system.sql        # MySQL DB Schema & Seed Data
│
├── .gitignore                   # Git Ignore Rules
├── requirements.txt             # Python Package Dependencies
└── README.md                    # Project Documentation
```

> **Structure Update (July 2026):** The project was reorganized. All source files previously nested inside a `Career_Recommendation_System/` subdirectory have been moved to the repository root. Root-level `LICENSE`, `career_recommendation_dataset_cleaned.csv`, `feature_columns.pkl`, `label_encoder.pkl`, and `xgboost_model.pkl` have been removed — ML artifacts are now exclusively stored inside `backend/model/`.

---

## ⚡ How to Run the Project (Step-by-Step)

### ✅ Prerequisites

Ensure the following tools are installed before proceeding:

| Tool | Version | Download |
|---|---|---|
| Python | 3.10 or above | https://www.python.org/downloads/ |
| MySQL Server | 8.0+ | https://dev.mysql.com/downloads/ |
| MySQL Workbench *(optional)* | Any | https://dev.mysql.com/downloads/workbench/ |
| Git | Any | https://git-scm.com/ |

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/AMB-007/Career_Recommendation_System.git
cd Career_Recommendation_System
```

---

### Step 2 — Create a Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Install all dependencies
pip install -r requirements.txt
```

---

### Step 3 — Set Up MySQL Database

**3a. Open MySQL and create the database:**

```sql
CREATE DATABASE career_recommendation
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

**3b. Import the full schema and seed data:**

```bash
mysql -u root -p career_recommendation < database/career_system.sql
```

> Enter your MySQL root password when prompted.

**3c. Verify all tables were created:**

```sql
USE career_recommendation;
SHOW TABLES;
```

Expected output:
```
+-----------------------------------+
| Tables_in_career_recommendation   |
+-----------------------------------+
| admin_users                       |
| bookmarked_careers                |
| career_details                    |
| feedback                          |
| login_history                     |
| prediction_history                |
| users                             |
+-----------------------------------+
```

---

### Step 4 — Configure Database Credentials

Open `backend/config.py` and update the `DB_CONFIG` block with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',   # ← Change this
    'database': 'career_recommendation',
    'pool_name': 'career_pool',
    'pool_size': 5,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

---

### Step 5 — Verify ML Model Files

Confirm all 3 model artifacts exist inside `backend/model/`:

```
backend/model/
├── xgboost_model.pkl      ← Trained XGBoost classifier
├── label_encoder.pkl      ← Career label encoder
└── feature_columns.pkl    ← 157 feature column names
```

If any file is missing, re-train the model from scratch:

```bash
cd backend
python train_model.py
```

---

### Step 6 — Start the Flask Server

```bash
cd backend
python app.py
```

Successful startup output:
```
INFO - Database connection pool created successfully
INFO - ML Model loaded successfully
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

To run in **debug mode** (detailed error messages):
```bash
python app.py debug
```

---

### Step 7 — Open in Browser

| Page | URL |
|---|---|
| 🏠 Home / Landing Page | http://127.0.0.1:5000 |
| 🔑 Student Login | http://127.0.0.1:5000/login |
| 📝 Student Register | http://127.0.0.1:5000/register |
| 📊 Student Dashboard | http://127.0.0.1:5000/dashboard |
| 🎯 Career Assessment | http://127.0.0.1:5000/assessment |
| 🛡️ Admin Login | http://127.0.0.1:5000/admin/login |
| 🛡️ Admin Dashboard | http://127.0.0.1:5000/admin/dashboard |
| ❤️ Health Check API | http://127.0.0.1:5000/health |

---

## 🔑 Default Credentials for Evaluation

| Role | Access URL | Email | Password |
|---|---|---|---|
| **Student** | `/login` | Registered student email | Set during registration |
| **Administrator** | `/admin/login` | `admin@gmail.com` | `Admin@123` |

> **Password Policy:** Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 special character.

---

## 🐳 Running with Docker (Optional)

```bash
cd backend
docker build -t career-recommendation .
docker run -p 5000:5000 \
  -e DB_PASSWORD=your_mysql_password \
  career-recommendation
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `Database connection pool not available` | Ensure MySQL is running and credentials in `backend/config.py` are correct |
| `ML Model not loaded` | Verify `backend/model/*.pkl` files exist; run `python train_model.py` if missing |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your activated virtual environment |
| Port 5000 already in use | Kill the existing process or change the port in the last line of `app.py` |
| `Table doesn't exist` error | Re-import schema: `mysql -u root -p career_recommendation < database/career_system.sql` |
| Templates not rendering | Ensure you are running `python app.py` from inside the `backend/` directory |

---

## 📝 License & Academic Disclaimer

Developed for academic purposes as an **MCA Major Project**. All rights reserved &copy; 2026.

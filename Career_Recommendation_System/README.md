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
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, FontAwesome 6, Google Fonts (Inter) | Modern, responsive, flat executive UI without gradient overlays. |
| **Data Visualization** | Chart.js, SweetAlert2 | Interactive radar/bar/doughnut charts and smooth modal dialogs. |
| **Backend Framework** | Python 3.14, Flask 2.x, Werkzeug | RESTful routing, session management, template rendering, and API handlers. |
| **Machine Learning** | XGBoost 3.x, Scikit-Learn, Pandas, NumPy | Gradient Boosted Classifier trained on 157 features for multi-class prediction. |
| **Database** | MySQL 8.0, mysql-connector-python | Relational database with connection pooling and normalized schema. |
| **Security** | BCrypt | Salted password hashing (12 work factor) and session cookie security. |

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

The normalized MySQL database consists of the following core tables:

1. `users` — Student accounts, hashed credentials, demographics, education level, CGPA.
2. `prediction_history` — Recorded assessment predictions, top career name, confidence score, and JSON payload of Top 5 matches.
3. `career_details` — Reference data for 75 careers including roadmaps, skills, certifications, and salary range.
4. `feedback` — User feedback, rating scores (1–5 stars), and support messages.
5. `bookmarked_careers` — Saved careers per student.
6. `login_history` — IP address, user agent, and timestamp audit logs for user logins.
7. `admin_users` — Administrator credentials.

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
│   ├── Dockerfile               # Deployment Spec
│   │
│   ├── model/                   # ML Artifacts
│   │   ├── career_recommendation_dataset_cleaned.csv
│   │   ├── xgboost_model.pkl
│   │   ├── label_encoder.pkl
│   │   └── feature_columns.pkl
│   │
│   ├── static/                  # Assets
│   │   ├── css/style.css        # Executive Flat Design System
│   │   ├── js/main.js           # Client Validation & Interactivity
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
│   │   ├── career_details.html  # Detailed Career Page
│   │   ├── profile.html         # Student Profile & Skill Radar Chart
│   │   ├── feedback.html        # System Feedback Form
│   │   ├── about.html           # Technical & Academic Details
│   │   ├── contact.html         # Support Page & FAQ Accordion
│   │   ├── admin_login.html     # Admin Portal Login
│   │   ├── admin_dashboard.html # Admin Control Panel & Analytics
│   │   ├── 404.html             # Page Not Found View
│   │   └── 500.html             # Server Error View
│   │
│   └── logs/                    # Application Log Output
│
├── database/
│   └── career_system.sql        # MySQL DB Schema & Initial Data
│
├── .gitignore                   # Git Ignore Rules
├── requirements.txt             # Python Package Dependencies
└── README.md                    # Project Documentation
```

---

## ⚡ Quick Start & Setup Guide

### Prerequisites
- **Python 3.10+** (Python 3.14 recommended)
- **MySQL Server 8.0+**
- **Git & Visual Studio Code**

### 1. Clone & Set Up Project
```bash
cd D:\Project\Career_Recommendation_System\backend
```

### 2. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 3. Initialize MySQL Database
Open **MySQL Workbench** or Command Prompt:
```sql
CREATE DATABASE career_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Import the schema:
```bash
mysql -u root -p career_recommendation < ../database/career_system.sql
```

### 4. Run Flask Server
```bash
python app.py
```
The server will start on: **`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials for Evaluation

| Role | Access URL | Email | Password |
|---|---|---|---|
| **Student** | `/login` | Registered Student Email | Created at Registration |
| **Administrator** | `/admin/login` | `admin@gmail.com` | `Admin@123` |

*Password Policy: Minimum 8 characters, containing at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character.*

---

## 📝 License & Academic Disclaimer

Developed for academic purposes as an **MCA Major Project**. All rights reserved &copy; 2026.

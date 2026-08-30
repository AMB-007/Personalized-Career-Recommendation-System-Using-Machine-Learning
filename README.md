<p align="center">
  <img src="frontend/static/logo.jpg" alt="PathFinder Logo" width="220" />
</p>

<h1 align="center">PathFinder</h1>
<h3 align="center">Personalized Career Recommendation System Using Machine Learning</h3>
<p align="center"><em>AI-Powered Career Guidance for Indian Secondary School Students — Classes 7 to 12</em></p>

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/XGBoost-95.97%25%20Accuracy-FF6600?style=flat-square&logo=python&logoColor=white" alt="XGBoost" />
  <img src="https://img.shields.io/badge/MySQL-8.x-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/Tests-83%2F83%20Passing-22C55E?style=flat-square&logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/Model-V9.5--Champion-8B5CF6?style=flat-square" alt="Model Version" />
  <img src="https://img.shields.io/badge/License-MIT-6366F1?style=flat-square" alt="License" />
</p>

---

## Table of Contents

1. [Overview](#overview)
2. [Key Statistics](#key-statistics)
3. [Features](#features)
4. [System Architecture](#system-architecture)
5. [Database Schema](#database-schema)
6. [Machine Learning Engine](#machine-learning-engine)
7. [Compliance-Based Ranking](#compliance-based-ranking)
8. [Assessment & Question Bank](#assessment--question-bank)
9. [Dataset Catalogue](#dataset-catalogue)
10. [Project Structure](#project-structure)
11. [Installation](#installation)
12. [Demo Credentials](#demo-credentials)
13. [API Reference](#api-reference)
14. [Testing](#testing)
15. [Changelog](#changelog)

---

## Overview

**PathFinder** is a full-stack, machine-learning-driven career guidance platform built for Indian secondary and senior secondary school students (Classes 7–12). It moves beyond simplistic personality quizzes by delivering a structured psychometric assessment, an XGBoost-powered compatibility engine, domain-specific prerequisite filtering, and a curated occupational taxonomy of 2,259 careers.

The system evaluates students across **19 psychometric and aptitude dimensions**, maps scores against real-world career knowledge profiles, applies domain-level prerequisite threshold compliance checks, and produces ranked recommendations with actionable skill development roadmaps — all in under 250 ms per request.

---

## Key Statistics

| Metric | Value |
| :--- | :--- |
| **ML Model** | XGBoost Classifier — V9.5-Champion |
| **Model Accuracy** | **95.97%** |
| **Hit@5 Rate** | **98.55%** |
| **NDCG@5** | **0.9475** |
| **ROC-AUC** | **0.9902** |
| **Careers in Catalogue** | **1,203** (full knowledge base) |
| **Career Domains** | **33 domains → 389 subdomains → 466 clusters** |
| **Assessment Questions** | **413** (class-adaptive, 19 sections) |
| **Answer Options** | **1,805** scored options |
| **Database Tables** | **18 normalized tables** |
| **Test Suite** | **83 / 83 tests passing** |

---

## Features

### For Students
- **Grade-Adaptive Assessment** — Question sets calibrated per class level and subject stream (PCM, PCB, Commerce, Humanities, General)
- **Timed & Standard Modes** — 45-minute competitive mode or untimed standard mode
- **Real-Time Auto-Save** — Assessment progress persists across browser sessions
- **Interactive Results Dashboard** — Radar charts, bar visualizers, and percentile breakdowns of cognitive aptitude and interest dimensions
- **Career Roadmaps** — 5-stage milestone progressions, prerequisite subjects, and curated online course links per career
- **Compliance-Verified Recommendations** — Careers that don't meet domain-level prerequisite thresholds are ranked lower, preventing unrealistic suggestions

### For Administrators
- **Student & Session Management** — Audit logs, attempt history, and per-question answer inspection
- **Question Bank Editor** — Browse, filter, and manage all 413 questions by section and class range
- **Career Catalogue Manager** — Full CRUD over the 1,203-career knowledge base, domains, and clusters
- **System Analytics Dashboard** — Completion rates, active users, and domain-level recommendation distribution

### Platform
- **Accessible Dark / Light Theme** — WCAG 2.1 AA high-contrast design system
- **Responsive Layout** — Bootstrap 5.3 with mobile-first breakpoints
- **Role-Based Navigation** — Separate, purpose-built navbars for guests, students, and administrators
- **One-File Database Setup** — Single consolidated `setup.sql` for any MySQL 8.x / MariaDB environment

---

## System Architecture

The diagram below illustrates the complete request lifecycle from client interaction through the ML inference pipeline to database persistence:

```mermaid
flowchart TB
    classDef client  fill:#E0E7FF,stroke:#3730A3,stroke-width:1.5px,color:#111827
    classDef flask   fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px,color:#111827
    classDef ml      fill:#DCFCE7,stroke:#15803D,stroke-width:1.5px,color:#111827
    classDef db      fill:#F1F5F9,stroke:#334155,stroke-width:1.5px,color:#111827

    subgraph Client [" Client Layer — Bootstrap 5.3 + Vanilla JS "]
        A["Student / Admin Browser"]:::client
        A1["Class-Adaptive Assessment<br/>(Auto-Save, MCQ / Ratings)"]:::client
        A2["Results Dashboard<br/>(Chart.js Radar & Bar)"]:::client
        A3["Career Explorer<br/>(1,203 Careers, Filters, Roadmaps)"]:::client
    end

    subgraph App [" Application Layer — Flask 3.0+ "]
        B["Flask Application Factory"]:::flask
        B1["Auth Controller<br/>(Register, Login, Logout)"]:::flask
        B2["Assessment Controller<br/>(Session, Normalization, Scoring)"]:::flask
        B3["Career Controller<br/>(Taxonomy, Search, Filters)"]:::flask
        B4["Admin Controller<br/>(Users, Questions, Careers)"]:::flask
    end

    subgraph ML [" ML Pipeline — backend/ml/ "]
        C1["Feature Vector Builder<br/>(19-D Psychometric + Academic)"]:::ml
        C2["Preprocessor Pipeline<br/>(StandardScaler + OrdinalEncoder)"]:::ml
        C3["XGBoost Classifier V9.5<br/>(500 Trees, 95.97% Accuracy)"]:::ml
        C4["Compliance Threshold Check<br/>(config.yaml domain rules)"]:::ml
        C5["Top-K Ranker<br/>(Threshold Pass → Probability → Ability)"]:::ml
    end

    subgraph DB [" Persistence Layer — MySQL 8.x "]
        D1[("Users & Student Profiles")]:::db
        D2[("413 Questions & 1,805 Options")]:::db
        D3[("1,203 Careers, Skills & Pathways")]:::db
        D4[("Assessment Scores & Recommendations")]:::db
    end

    A --> B1
    B1 <--> D1
    A --> A1
    A1 --> B2
    B2 <--> D2
    B2 --> C1
    D3 --> C1
    C1 --> C2 --> C3 --> C4 --> C5
    C5 --> D4
    D4 --> A2
    A --> A3
    A3 <--> D3
```

---

## Database Schema

The database (`career_recommendation_db`) is built on **MySQL 8.x** with **18 relational tables**, enforcing strict foreign keys, cascade deletes, and check constraints. The entire schema plus seed data is consolidated into a single file:

```bash
# Initialize from the unified setup script
mysql -u root -p < setup.sql
```

```mermaid
erDiagram
    USERS ||--o| STUDENTS : "has profile"
    USERS {
        bigint id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        enum role "student, admin"
        datetime created_at
    }

    STUDENTS ||--o| ACADEMIC_SCORES : "maintains"
    STUDENTS ||--o{ ASSESSMENT_SESSIONS : "attempts"
    STUDENTS {
        bigint id PK
        bigint user_id FK
        varchar student_code UK
        varchar first_name
        varchar last_name
        int class_level "7–12"
        varchar stream
        varchar board
    }

    ACADEMIC_SCORES {
        bigint id PK
        bigint student_id FK
        float mathematics_score
        float science_score
        float computer_science_score
        float english_score
        float overall_percentage
    }

    QUESTION_SECTIONS ||--o{ QUESTIONS : "categorizes"
    QUESTIONS ||--o{ QUESTION_OPTIONS : "provides"
    QUESTIONS ||--o{ STUDENT_ANSWERS : "answered in"
    QUESTIONS {
        bigint id PK
        varchar question_code UK
        int section_id FK
        text question_text
        enum question_type "MCQ, RATING, SCENARIO"
        int class_min
        int class_max
        varchar stream_specific
    }

    ASSESSMENT_SESSIONS ||--o{ STUDENT_ANSWERS : "contains"
    ASSESSMENT_SESSIONS ||--o| ASSESSMENT_SCORES : "computes"
    ASSESSMENT_SESSIONS ||--o{ CAREER_RECOMMENDATIONS : "generates"
    ASSESSMENT_SESSIONS {
        bigint id PK
        bigint student_id FK
        int attempt_number
        enum status "in_progress, completed, abandoned"
        datetime started_at
        datetime completed_at
    }

    ASSESSMENT_SCORES {
        bigint id PK
        bigint assessment_id FK
        float mathematical_ability
        float logical_reasoning
        float scientific_reasoning
        float problem_solving
        float analytical_ability
        float creativity
        float digital_ability
        float technology_interest
        float engineering_interest
        float healthcare_interest
        float business_interest
        float research_interest
    }

    CAREER_DOMAINS ||--o{ CAREER_SUBDOMAINS : "groups"
    CAREER_DOMAINS ||--o{ CAREERS : "classifies"
    CAREER_SUBDOMAINS ||--o{ CAREER_CLUSTERS : "branches"
    CAREERS ||--o{ CAREER_SKILLS : "demands"
    CAREERS ||--o{ CAREER_PATHWAYS : "charts"
    CAREERS ||--o{ CAREER_RECOMMENDATIONS : "ranked as"
    CAREERS {
        bigint id PK
        varchar career_code UK
        varchar career_name
        int domain_id FK
        int subdomain_id FK
        int cluster_id FK
        text description
        varchar minimum_education
        varchar typical_education
    }
```

---

## Machine Learning Engine

The ML pipeline evaluates student–career compatibility using a multi-phase feature engineering process and an **XGBoost Classifier (V9.5-Champion)** trained on labelled multi-dimensional aptitude and occupational knowledge profiles.

### Feature Engineering (11-Dimensional Feature Contract)

Student assessment scores are transformed into an **11-dimensional feature vector**:

| # | Feature | Description |
| :---: | :--- | :--- |
| 1 | `ability_match_component` | Mean of 8 ability dimension proximity scores (`100 - |student - required|`) |
| 2 | `interest_match_component` | Weighted mean of 10 interest dimension proximity scores (top-3 interests boosted 1.5×) |
| 3 | `academic_match_component` | Student academic percentage (0–100) |
| 4 | `learning_match_component` | Student learning ability score |
| 5 | `composite_alignment_index` | `0.45×ability + 0.35×interest + 0.10×academic + 0.10×learning` |
| 6 | `ability_interest_synergy` | `(ability × interest) / 100` |
| 7 | `ability_interest_gap` | `|ability - interest|` |
| 8 | `min_core_match` | `min(ability, interest)` |
| 9 | `max_core_match` | `max(ability, interest)` |
| 10 | `harmonic_core_match` | Harmonic mean of ability and interest |
| 11 | `geometric_core_synergy` | `√(ability × interest)` |
| 12 | `holistic_synergy` | Geometric mean of all four components |

Plus **categorical metadata**: `career_name`, `career_domain`, `career_subdomain`, `career_cluster`, `stream`, `age`, `class`.

The feature vector is scaled with `StandardScaler` and encoded with `OrdinalEncoder` before XGBoost inference.

### Model Performance

| Metric | Score |
| :--- | :---: |
| **Accuracy** | **95.97%** |
| **Precision (weighted)** | **95.95%** |
| **Recall (weighted)** | **95.97%** |
| **F1-Score (weighted)** | **95.96%** |
| **ROC-AUC** | **0.9902** |
| **Hit@5 Rate** | **98.55%** |
| **Hit@10 Rate** | **99.4%** |
| **NDCG@5** | **0.9475** |

### Interest Weighting (`config.yaml`)

The top-N student interests receive a configurable boost factor during interest-match computation:

```yaml
interest_boost_factor: 1.5   # Multiplier applied to top expressed interests
top_n_interests: 3           # Number of interests to boost
```

This ensures a student with 80% Engineering Interest and 65% Technology Interest will have those dimensions weighted more heavily when evaluating engineering-aligned careers.

---

## Compliance-Based Ranking

A key feature introduced in **V9.5-Champion** is domain-specific prerequisite threshold enforcement. This prevents synthetic or low-requirement career variants from appearing at the top of recommendations for students with strong, domain-specific profiles.

### How It Works

After XGBoost probabilities are computed for all 1,203 careers, each career is evaluated against its domain's minimum requirements defined in `backend/ml/config.yaml`:

```yaml
domain_requirements:
  healthcare:
    scientific_reasoning: 60     # Career must require ≥ 60% scientific reasoning
    mathematical_ability: 60     # Career must require ≥ 60% mathematical ability
  engineering:
    engineering_interest: 55     # Career must require ≥ 55% engineering interest
  arts:
    arts_interest: 50

default_requirements:
  required_scientific_thinking: 50   # Applied to all domains not explicitly listed
  required_mathematical_ability: 50
```

A `threshold_pass` flag (1 = compliant, 0 = non-compliant) is computed per career and becomes the **primary sort key**. Compliant careers always rank above non-compliant ones, regardless of raw XGBoost probability. The final sort order is:

```
threshold_pass DESC → probability DESC → ability_match DESC → interest_match DESC
```

### Example Output (Class 11, Science Stream, Low Ability / High Engineering Interest)

```
Rank  1: Electrical Engineer Specialist  | Healthcare    | 99.48% | A: 88.62% | I: 73.3%
Rank  2: Biotechnologist Specialist      | Healthcare    | 99.24% | A: 93.38% | I: 74.5%
Rank  3: UI UX Designer Specialist       | Engineering   | 98.96% | A: 89.25% | I: 73.6%
Rank  4: Financial Analyst Specialist    | Engineering   | 98.83% | A: 87.62% | I: 78.7%
Rank  5: Cybersecurity Analyst           | Engineering   | 97.90% | A: 92.50% | I: 82.2%
```

---

## Assessment & Question Bank

The psychometric assessment adapts dynamically to the student's class level and subject stream.

### Question Sections (19 Dimensions)

| # | Dimension | Questions |
| :---: | :--- | :---: |
| 1 | Academic Focus | 30 |
| 2 | Mathematical Ability | 75 |
| 3 | Logical Reasoning | 42 |
| 4 | Scientific Thinking | 37 |
| 5 | Problem Solving | 20 |
| 6 | Analytical Thinking | 18 |
| 7 | Communication | 12 |
| 8 | Creativity | 12 |
| 9 | Digital Ability | 21 |
| 10 | Learning Ability | 12 |
| 11 | Spatial Ability | 12 |
| 12 | Practical Ability | 10 |
| 13 | Core Interests | 46 |
| 14 | Activities & Hobbies | 20 |
| 15 | Teamwork | 8 |
| 16 | Leadership | 8 |
| 17 | Work Preferences | 10 |
| 18 | Career Awareness | 10 |
| 19 | Career Preferences | 10 |
| | **Total** | **413** |

### Available Questions by Class

| Class | Eligible Questions | Focus |
| :---: | :---: | :--- |
| 7 | 140 | Early interest discovery and foundational logic |
| 8 | 140 | Cognitive aptitude and problem solving |
| 9 | 152 | Abstract reasoning and stream preparation |
| 10 | 148 | Senior stream selection and analytical skills |
| 11 | 163 | Stream-tailored questions (PCM, PCB, Commerce, Arts) |
| 12 | 161 | Higher education readiness and specialized career matching |

---

## Dataset Catalogue

All research and training datasets are stored in the `Datasets/` directory.

| File | Rows | Size | Description |
| :--- | :---: | :---: | :--- |
| `Career_Knowledge_CLEANED.csv` | 1,203 | 230 KB | Curated occupational knowledge base — 27 columns of ability/interest requirements per career |
| `Career_Knowledge_RAW_1206_with_issues.csv` | 1,206 | 229 KB | Raw dataset used for EDA — demonstrates cleaning and outlier treatment |
| `Student_Assessment_CLEANED.csv` | 10,000 | 6.07 MB | Normalized psychometric scores for 10,000 students (Grades 7–12) |
| `Student_Assessment_RAW_10k_with_issues.csv` | 10,000 | 6.06 MB | Raw uncalibrated assessment data for pipeline benchmarking |
| `Student_Career_Compatibility_CLEANED.csv` | 50,000 | 6.32 MB | Ground-truth compatibility pairs used for XGBoost training |
| `Student_Career_Compatibility_RAW_50k_with_issues.csv` | 50,000 | 6.30 MB | Raw unprocessed compatibility pairs |

> EDA visualizations and performance benchmark reports are in `Datasets/figures/` and `Datasets/reports/`.

---

## Project Structure

```
Personalized-Career-Recommendation-System-Using-Machine-Learning/
│
├── backend/
│   ├── app.py                        # Flask application factory
│   ├── config.py                     # Environment configuration
│   ├── extensions.py                 # SQLAlchemy, login manager
│   ├── ml/
│   │   ├── config.yaml               # Domain thresholds & interest weighting
│   │   ├── feature_builder.py        # 11-D feature vector construction
│   │   ├── model_loader.py           # Thread-safe singleton artifact loader
│   │   ├── prediction_service.py     # XGBoost batch inference
│   │   ├── recommendation_service.py # Compliance ranking & Top-K extraction
│   │   ├── data/
│   │   │   └── career_knowledge_requirements.csv
│   │   └── models/
│   │       ├── model.joblib          # XGBoost V9.5-Champion
│   │       ├── preprocessor.joblib   # StandardScaler + OrdinalEncoder
│   │       ├── feature_columns.json  # 19-column contract
│   │       ├── classes.json          # Label encoding map
│   │       ├── model_config.json     # Hyperparameter record
│   │       └── version.json          # Model version metadata
│   ├── models/                       # SQLAlchemy ORM models
│   ├── routes/                       # Flask blueprints (auth, assessment, career, admin)
│   ├── services/                     # Business logic (scoring, profile, recommendation)
│   └── utils/                        # Validators, decorators, helpers
│
├── database/
│   ├── setup.sql                     # Complete DB schema + seed data (mirror)
│   ├── questions_seed.sql            # 413 questions + 1,805 options seed
│   └── *.py                          # Database utility & import scripts
│
├── Datasets/
│   ├── Career_Knowledge_CLEANED.csv
│   ├── Student_Assessment_CLEANED.csv
│   ├── Student_Career_Compatibility_CLEANED.csv
│   ├── Career_Recommendation_ML_Training_EDA_SHAP.ipynb
│   ├── figures/                      # EDA & SHAP plots
│   └── reports/                      # Benchmark CSVs & classification reports
│
├── model_training/                   # Training pipeline and notebooks
├── scripts/
│   ├── build_unified_setup_sql.py    # Generates consolidated setup.sql
│   ├── clean_knowledge_base.py       # Applies threshold filters to career CSV
│   ├── inspect_scores.py             # Sample prediction output inspector
│   ├── organize_unwanted_files.py    # Archives legacy files
│   └── ...
│
├── tests/                            # 83-test automated suite
├── frontend/
│   ├── static/                       # CSS, JS, logo, images
│   └── templates/                    # Jinja2 HTML templates
│
├── setup.sql                         # ★ Single-file database initialization
├── requirements.txt
├── run.py
├── .env.example
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.10, 3.11, 3.12, or 3.13
- MySQL Server 8.0+ (or MariaDB)
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning
```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment

Copy the example file and set your database credentials:

```bash
cp .env.example .env
```

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=career_recommendation_db
SECRET_KEY=your_secret_key
```

### Step 5 — Initialize the Database

Run the single, consolidated SQL script in MySQL Workbench or the MySQL CLI:

```bash
mysql -u root -p < setup.sql
```

Or from within MySQL Workbench:

```sql
SOURCE /path/to/setup.sql;
```

This single file creates all **18 tables**, inserts **413 questions**, **1,805 answer options**, **2,259 careers** (across 33 domains), demo credentials, indexes, and analytical views.

### Step 6 — Run the Application

```bash
python run.py
```

Open **`http://127.0.0.1:5000`** in your browser.

---

## Demo Credentials

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@123` | Full access to admin dashboard, users, questions, and career catalogue |
| **Student (Class 12)** | `rahul_sharma_12` | `Student@123` | Pre-completed Science-PCB profile with assessment history and recommendations |

New student accounts can be registered at `/register` for any class from 7 to 12.

---

## API Reference

### Authentication — `/auth`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/login` | Student or admin authentication |
| `POST` | `/auth/register` | New student registration |
| `GET` | `/auth/logout` | Session invalidation |

### Assessment — `/assessment` & `/api/assessment`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/assessment/instructions` | Pre-test guidelines and mode selector |
| `POST` | `/assessment/start` | Initialize a new class-adaptive question session |
| `POST` | `/api/assessment/answer` | Auto-save a single answer with latency tracking |
| `POST` | `/api/assessment/submit` | Trigger scoring, ML inference, compliance ranking, and recommendation storage |
| `GET` | `/assessment/results/<id>` | Full results page with charts and printable report |
| `GET` | `/api/assessment/<id>/profile` | JSON student profile with strengths and growth areas |

### Career Explorer — `/career`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/career/explorer` | Paginated search with domain, cluster, and education filters |
| `GET` | `/career/<id>` | Detailed career profile with roadmap, skills, and courses |

### Administration — `/admin`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/admin/dashboard` | System analytics and completion metrics |
| `GET` | `/admin/users` | Student cohort management and session audit logs |
| `GET` | `/admin/questions` | 413-question bank browser with grade and section filters |
| `GET` | `/admin/careers` | Career catalogue manager |

---

## Testing

The repository includes an automated unit and integration test suite covering authentication, session state machines, scoring algorithms, ML model loading, concurrency, and recommendation APIs.

```bash
python -m unittest discover -s tests -v
```

```
----------------------------------------------------------------------
Ran 83 tests in ~30s

OK
```

### Test Modules

| Module | Tests | Coverage |
| :--- | :---: | :--- |
| `test_ml_model_loading` | 3 | Artifact integrity, singleton loader, missing artifact errors |
| `test_ml_prediction` | 4 | Feature vector → probability output, reference sample sanity |
| `test_ml_feature_builder` | 2 | Ability match & interest match computation |
| `test_ml_recommendation` | 3 | Full catalogue loading, Top-K ranking, result structure |
| `test_ml_concurrency_and_performance` | 2 | 5 & 10 concurrent recommendation requests |
| `test_ml_integrity_and_security` | 3 | SHA-256 artifact hashes, `.gitignore` security, path traversal |
| `test_ml_api_endpoints` | 5 | REST API contract and JSON schema |
| `test_assessment_workflow` | 12 | Session lifecycle: start → answer → submit → results (all class cohorts) |
| `test_assessment_selection` | 4 | Class-adaptive question pool filtering and difficulty balancing |
| `test_scoring` | 2 | Score calculation normalization and guidance categories |
| `test_scoring_deterministic` | 5 | 0%, 50%, 80%, 100% correctness, ability/interest independence |
| `test_student_profile_and_baseline` | 3 | Profile creation, API endpoint, baseline recommendation matching |
| `test_questionnaire_validation_comprehensive` | 5 | Class bounds, academic bounds, sensitive fields, empty submission |
| `test_auth` | 3 | Registration, login, logout |
| `test_e2e_real_student_flow` | 4 | Full journey: register → assess → submit → recommendations |
| `test_admin_and_user_history` | 5 | Admin session audit, user history retrieval |
| `test_admin` | 3 | Admin dashboard access and user management |
| `test_assessment` | 3 | Assessment session initialization and question delivery |
| `test_career` | 2 | Career explorer and detail views |
| `test_career_import` | 9 | Career data import pipeline integrity |

---

## Changelog

### V9.5-Champion (Current)

- **[NEW] Compliance-Based Ranking**: Introduced domain-specific prerequisite threshold enforcement via `backend/ml/config.yaml`. Careers that fail minimum requirement checks are deprioritized in the final sort order using a `threshold_pass` flag.
- **[NEW] Dynamic Interest Weighting**: Top-3 student interests receive a configurable 1.5× boost factor during interest-match score computation.
- **[NEW] Unified Database Setup**: All schema DDL and seed data consolidated into a single `setup.sql` file for one-command database initialization.
- **[FIX] Full Catalogue Evaluation**: Restored `DEFAULT_CAREER_DATA_PATH` to the complete `career_knowledge_requirements.csv` (1,203 careers) ensuring the test suite and production pipeline both evaluate the full career space.
- **[FIX] Recommendation Result Keys**: Corrected output keys from `ability_match_component`/`interest_match_component` to `ability_match_score`/`interest_match_score` for API consistency.
- **[CLEANUP] Dataset Organization**: Archived legacy migration scripts and training logs to `unwanted files and folders/`. Verified and documented all datasets in `Datasets/README.md`.
- **[TEST] 83/83 Tests Passing**: All unit, integration, concurrency, and security tests green.

---

<p align="center">
  Built with Python · Flask · XGBoost · MySQL · Bootstrap 5
  <br/>
  <em>PathFinder — Helping every student find their best path forward.</em>
</p>

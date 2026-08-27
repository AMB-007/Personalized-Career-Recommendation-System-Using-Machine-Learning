# 🚀 Personalized Career Recommendation System
### *AI-Powered Career Guidance & Compatibility Engine for Classes 7–12*

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-Flask%203.0+-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/ML%20Engine-XGBoost%20V7.2-orange?style=for-the-badge&logo=xgboost&logoColor=white" alt="XGBoost" />
  <img src="https://img.shields.io/badge/Database-MySQL%208.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/Frontend-Bootstrap%205.3%20%7C%20Chart.js-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/Tests-73%2F73%20PASSING-success?style=for-the-badge&logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/Theme-Light%20%26%20Dark%20Mode-black?style=for-the-badge" alt="Theme" />
  <img src="https://img.shields.io/badge/Design-Zero%20Gradients%20Flat%20UI-0F172A?style=for-the-badge" alt="Flat Design" />
</p>

---

## 📖 Table of Contents
1. [🌟 Executive Overview](#-executive-overview)
2. [🏗️ End-to-End System Architecture](#️-end-to-end-system-architecture)
3. [🗄️ Database Entity-Relationship (ER) Model](#️-database-entity-relationship-er-model)
4. [🧠 Machine Learning Compatibility & Ranking Engine (V7.2)](#-machine-learning-compatibility--ranking-engine-v72)
5. [⚡ First-Time Database Setup & Query Execution](#-first-time-database-setup--query-execution)
6. [🚀 Quick Start & Installation](#-quick-start--installation)
7. [🔑 Demo Credentials](#-demo-credentials)
8. [🌐 REST API Reference](#-rest-api-reference)
9. [🎨 UI/UX Design System & Theme Engine](#-uiux-design-system--theme-engine)
10. [🧪 Automated Verification Suite](#-automated-verification-suite)

---

## 🌟 Executive Overview

The **Personalized Career Recommendation System** is an enterprise-grade career guidance platform tailored specifically for junior and senior secondary school students (**Classes 7–12**), educational counsellors, and parents. 

Unlike generic keyword-matching tools, this platform evaluates students across **19 psychometric dimensions** (8 cognitive abilities, 10 disciplinary affinities, and school curriculum marks) against a database of **1,206 career knowledge profiles**. Compatibility is predicted by a high-performance **XGBoost Classifier (V7.2)** that dynamically ranks all careers and generates personalized educational roadmaps, prerequisite subjects, and skill gap analyses.

---

## 🏗️ End-to-End System Architecture

The following diagram illustrates the complete request lifecycle, machine learning inference pipeline, and relational database synchronization:

```mermaid
flowchart TB
    %% Styling Definitions
    classDef client fill:#E0E7FF,stroke:#1B2CC1,stroke-width:2px,color:#111827;
    classDef app fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#111827;
    classDef ml fill:#DCFCE7,stroke:#15803D,stroke-width:2px,color:#111827;
    classDef db fill:#F1F5F9,stroke:#475569,stroke-width:2px,color:#111827;
    classDef output fill:#FCE7F3,stroke:#BE185D,stroke-width:2px,color:#111827;

    subgraph ClientLayer [" 📱 Client Presentation Layer (Bootstrap 5.3 + Vanilla JS) "]
        A["👤 Student / Admin Browser"]:::client
        A1["📋 Grade-Adaptive Assessment<br/>(1-5 Rating Grids, Autosave)"]:::client
        A2["📊 Dynamic Visualizations<br/>(Theme-Aware Radar & Bar Charts)"]:::client
        A3["🔍 Career Explorer & Details<br/>(Search, Filters, 5-Stage Roadmaps)"]:::client
    end

    subgraph AppLayer [" ⚡ Application & Orchestration Layer (Flask 3.0+) "]
        B["🌐 Flask Application Factory & Blueprints"]:::app
        B1["🔐 Auth & Security Service<br/>(Multi-Format Password Hashing)"]:::app
        B2["📝 Assessment Orchestrator<br/>(19-D Normalization Engine)"]:::app
        B3["💼 Career & Taxonomy Service<br/>(Domains, Subdomains, Clusters)"]:::app
    end

    subgraph MLLayer [" 🧠 Production ML Pipeline (XGBoost V7.2 Engine) "]
        C1["🧩 Feature Builder Module<br/>(8-D Ability & 10-D Interest Matchers)"]:::ml
        C2["📐 11-Feature Contract DataFrame<br/>[Age, Class, 4 Match Scores, Taxonomy, Stream]"]:::ml
        C3["⚙️ Preprocessor Pipeline<br/>(StandardScaler + OrdinalEncoder)"]:::ml
        C4["🌲 XGBoost Classifier (500 Trees)<br/>(Probability Inference: Threshold 0.495)"]:::ml
        C5["🏆 Ranking & Top-K Extraction Engine<br/>(Ranks all 1,206 Careers Descending)"]:::ml
    end

    subgraph DBLayer [" 🗄️ Persistence Layer (MySQL Server 8.x) "]
        D1[("👥 Users & Student Profiles")]:::db
        D2[("❓ Question Bank & Answers")]:::db
        D3[("📚 1,206 Career Knowledge Base")]:::db
        D4[("🏅 Saved Career Recommendations")]:::db
    end

    %% Workflow Flowlines
    A -->|"1. Registration / Login"| B1
    B1 <-->|"Authenticate User"| D1
    A -->|"2. Submit Assessment Answers"| A1
    A1 -->|"3. POST /api/assessment/submit"| B2
    B2 <-->|"Fetch Raw Answers & Scores"| D2
    B2 -->|"4. Normalized Profile Data"| C1
    D3 -->|"5. 1,206 Career Benchmark Vectors"| C1
    C1 -->|"6. Generate 11-Feature Matrix"| C2
    C2 -->|"7. Transform Matrix"| C3
    C3 -->|"8. Scaled & Encoded Arrays"| C4
    C4 -->|"9. Compatibility Probabilities"| C5
    C5 -->|"10. Persist Top 5 Recommendations"| D4
    D4 -->|"11. Render Results & Explanations"| A2
    A -->|"12. Explore Career Catalogue"| A3
    A3 <-->|"Fetch Career Pathways & Skills"| D3
```

---

## 🗄️ Database Entity-Relationship (ER) Model

The application utilizes a relational MySQL schema structured into four functional modules: **Authentication**, **Assessment & Scoring**, **Career Knowledge Taxonomy**, and **Recommendations**.

```mermaid
erDiagram
    %% Entities & Attributes

    USERS ||--o| STUDENTS : "profiles"
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
        int class_level "7-12"
        varchar stream "Science-PCM, Science-PCB, Commerce, Humanities, General"
        varchar board "CBSE, ICSE, State Board, IB"
    }

    ACADEMIC_SCORES {
        bigint id PK
        bigint student_id FK
        float mathematics_score
        float science_score
        float computer_science_score
        float english_score
    }

    QUESTION_SECTIONS ||--o{ QUESTIONS : "categorizes"
    QUESTION_SECTIONS {
        bigint id PK
        varchar name
        int display_order
        text description
    }

    QUESTIONS ||--o{ QUESTION_OPTIONS : "provides"
    QUESTIONS ||--o{ STUDENT_ANSWERS : "evaluated in"
    QUESTIONS {
        bigint id PK
        bigint section_id FK
        varchar question_code UK
        text question_text
        enum question_type "RATING, SINGLE_CHOICE"
        int class_min "7"
        int class_max "12"
    }

    QUESTION_OPTIONS {
        bigint id PK
        bigint question_id FK
        varchar option_text
        int option_value
        int sequence_order
    }

    ASSESSMENT_SESSIONS ||--o{ STUDENT_ANSWERS : "contains"
    ASSESSMENT_SESSIONS ||--o| ASSESSMENT_SCORES : "computes"
    ASSESSMENT_SESSIONS ||--o{ CAREER_RECOMMENDATIONS : "generates"
    ASSESSMENT_SESSIONS {
        bigint id PK
        bigint student_id FK
        enum status "in_progress, completed, abandoned"
        datetime started_at
        datetime completed_at
    }

    STUDENT_ANSWERS {
        bigint id PK
        bigint assessment_id FK
        bigint question_id FK
        int response_value "1-5"
        datetime answered_at
    }

    ASSESSMENT_SCORES {
        bigint id PK
        bigint assessment_id FK
        float mathematical_ability
        float scientific_reasoning
        float computational_thinking
        float spatial_verbal_reasoning
        float technology_interest
        float healthcare_science_interest
        float business_finance_interest
        float creative_arts_interest
        float academic_score
    }

    CAREER_DOMAINS ||--o{ CAREER_SUBDOMAINS : "groups"
    CAREER_DOMAINS ||--o{ CAREERS : "classifies"
    CAREER_DOMAINS {
        bigint id PK
        varchar domain_name UK
        text description
        varchar icon
        int display_order
    }

    CAREER_SUBDOMAINS ||--o{ CAREER_CLUSTERS : "branches"
    CAREER_SUBDOMAINS ||--o{ CAREERS : "specifies"
    CAREER_SUBDOMAINS {
        bigint id PK
        bigint domain_id FK
        varchar name
        text description
    }

    CAREER_CLUSTERS ||--o{ CAREERS : "clusters"
    CAREER_CLUSTERS {
        bigint id PK
        bigint subdomain_id FK
        varchar name
        text description
    }

    CAREERS ||--o{ CAREER_SKILLS : "demands"
    CAREERS ||--o{ CAREER_SUBJECTS : "requires"
    CAREERS ||--o{ CAREER_EDUCATION : "specifies"
    CAREERS ||--o{ CAREER_PATHWAYS : "charts"
    CAREERS ||--o{ CAREER_RECOMMENDATIONS : "recommended as"
    CAREERS {
        bigint id PK
        varchar career_code UK
        varchar career_name
        bigint domain_id FK
        bigint subdomain_id FK
        bigint cluster_id FK
        text description
        varchar minimum_education
        varchar typical_education
        varchar work_environment
        varchar work_style
        varchar entry_level_role
        varchar advanced_role
    }

    CAREER_SKILLS {
        bigint id PK
        bigint career_id FK
        varchar skill_name
        int importance_level "1-5"
        varchar importance_label "Critical, Essential, Important"
    }

    CAREER_SUBJECTS {
        bigint id PK
        bigint career_id FK
        varchar subject_name
        int importance_level "1-5"
        varchar importance_label
    }

    CAREER_EDUCATION {
        bigint id PK
        bigint career_id FK
        varchar education_level
        varchar degree_name
        int sequence_order
    }

    CAREER_PATHWAYS {
        bigint id PK
        bigint career_id FK
        int stage_number "1-5"
        varchar stage_name
        text description
    }

    CAREER_RECOMMENDATIONS {
        bigint id PK
        bigint assessment_id FK
        bigint career_id FK
        int rank_position "1-10"
        float score "Compatibility %"
        text recommendation_reason
        text strengths
        text skill_gaps
        datetime created_at
    }
```

---

## 🧠 Machine Learning Compatibility & Ranking Engine (V7.2)

### 1. Authoritative 11-Feature Contract Schema
The XGBoost inference engine enforces an exact 11-feature contract. All inputs are strictly validated before scoring:

| # | Feature Name | Data Type | Permitted Range | Description |
| :-: | :--- | :---: | :---: | :--- |
| **1** | `age` | `float` | $10.0 - 25.0$ | Student chronological age |
| **2** | `class` | `int` | $7 - 12$ | Current academic grade level |
| **3** | `ability_match_component` | `float` | $0.0 - 100.0$ | Mean alignment across 8 cognitive ability dimensions |
| **4** | `interest_match_component` | `float` | $0.0 - 100.0$ | Mean alignment across 10 disciplinary interest tracks |
| **5** | `academic_match_component`| `float` | $0.0 - 100.0$ | Composite score of self-reported academic subjects |
| **6** | `learning_match_component`| `float` | $0.0 - 100.0$ | Problem solving and learning adaptability score |
| **7** | `career_name` | `string` | Categorical | Target candidate career name |
| **8** | `career_domain` | `string` | Categorical | Primary professional industry sector |
| **9** | `career_subdomain` | `string` | Categorical | Specialized track within domain |
| **10**| `career_cluster` | `string` | Categorical | Functional occupational cluster |
| **11**| `stream` | `string` | Categorical | Selected stream (`Science-PCM`, `Science-PCB`, `Commerce`, `Humanities`, `General`) |

> [!CAUTION]
> **Data Privacy Guarantee:** `student_id`, names, and contact details are strictly excluded from the ML feature matrix to prevent data leakage and bias.

---

### 2. Verified Performance Metrics (V7.2 Model)

> [!NOTE]
> Classification performance and ranking performance are strictly distinguished in our verified evaluation benchmarks:

#### A. Multi-Candidate Recommendation Ranking (Catalogue of 1,206 Careers)
| Metric | Benchmark Result | Evaluation Description |
| :--- | :---: | :--- |
| **Hit@1 (Top 1 Accuracy)** | **96.18%** | Primary recommended career perfectly matches student profile |
| **Hit@3** | **99.68%** | True optimal career exists within the Top 3 recommendations |
| **Hit@5** | **99.88%** | True optimal career exists within the Top 5 recommendations |
| **Hit@10** | **99.94%** | True optimal career exists within the Top 10 recommendations |
| **Mean Reciprocal Rank (MRR)** | **97.98%** | Average reciprocal rank of the ground-truth optimal career |
| **NDCG@5** | **92.12%** | Normalized Discounted Cumulative Gain across Top 5 ranks |

#### B. Binary Student-Career Compatibility Classification (Test Set)
| Metric | Score | Metric | Score |
| :--- | :---: | :--- | :---: |
| **Overall Accuracy** | **80.99%** | **Balanced Accuracy** | **71.71%** |
| **Precision** | **83.21%** | **Recall** | **92.40%** |
| **F1-Score** | **87.56%** | **ROC-AUC** | **85.25%** |
| **PR-AUC** | **93.48%** | **Optimal Threshold** | **0.495** |

---

## ⚡ First-Time Database Setup & Query Execution

To initialize the MySQL database for the first time, use either **Method A (Automated Python Script)** or **Method B (MySQL Workbench / Command Line)**.

### Method A: Automated One-Command Python Setup (Recommended)
```powershell
python database/seed.py
```
*This automatically creates `career_recommendation_db`, runs all table DDLs, seeds users, imports all 1,206 careers, and generates analytical views.*

---

### Method B: MySQL Workbench All-In-One Script (Single File)

1. Open **MySQL Workbench** and connect to your MySQL Server.
2. Open the all-in-one setup file: **[`database/setup.sql`](file:///c:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/database/setup.sql)** (`File -> Open SQL Script`).
3. Click the ⚡ **Execute** button (or press `Ctrl + Shift + Enter`).

*This single file creates `career_recommendation_db`, sets up all 18 tables, seeds demo users, imports all 1,206 career knowledge profiles, populates the adaptive questions, creates analytical views, and runs the verification check automatically.*

```sql
-- Or run from terminal:
mysql -u root -p < database/setup.sql
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- **Python:** 3.10, 3.11, 3.12, or 3.14
- **Database:** MySQL Server 8.0+ (or MySQL Workbench)
- **Git**

### 2. Clone and Install Dependencies
```powershell
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and configure your database credentials:
```powershell
copy .env.example .env
```
Sample `.env` configuration:
```ini
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_recommendation_db

# ML Model Paths
MODEL_DIR=backend/ml/models
CAREER_DATA_PATH=backend/ml/data/career_knowledge_requirements.csv
```

### 4. Launch Application
```powershell
python run.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🔑 Demo Credentials

| Role | Username / Identifier | Password | Access Level | Description |
| :--- | :--- | :--- | :---: | :--- |
| **Administrator** | `admin` | `Admin@123` | **Full Admin** | Question management, career CRUD, student analytics |
| **Student (Junior)** | `rahul_class8` | `Student@123` | **Student** | Class 8 student profile (General curriculum) |
| **Student (Middle)** | `ananya_class10`| `Student@123` | **Student** | Class 10 student profile (Board exam candidate) |
| **Student (Senior)** | `aravind_class12`| `Student@123` | **Student** | Class 12 student profile (Science-PCM stream) |

---

## 🌐 REST API Reference

The platform provides a comprehensive REST API returning JSON responses in standard formats:

| Method | Endpoint | Auth | Purpose & Description |
| :---: | :--- | :---: | :--- |
| `GET` | `/api/health` | Public | System status, database connectivity, and ML engine health check |
| `GET` | `/api/model/info` | Public | Inspect active XGBoost model version (V7.2), feature contract, and metrics |
| `POST` | `/api/predictions` | Student | Directly run XGBoost inference on candidate feature vectors |
| `POST` | `/api/recommendations` | Student | Generate and rank career recommendations across all 1,206 careers |
| `GET` | `/api/recommendations/<int:session_id>` | Student | Fetch stored Top-K recommendations and explanations for a completed session |
| `GET` | `/api/recommendations/student/<student_code>` | Student | Fetch historical recommendations for a student code |
| `GET` | `/api/careers` | Public | Search and filter 1,206 careers by domain, subdomain, cluster, or keyword |
| `GET` | `/api/careers/<int:id>` | Public | Get full career knowledge profile, required skills, and 5-stage roadmap |
| `GET` | `/api/careers/domains` | Public | List all 28 career domains and icons |
| `POST` | `/api/assessment/start` | Student | Initialize a new adaptive assessment session for logged-in student |
| `POST` | `/api/assessment/answer` | Student | Record an individual question response with autosave |
| `POST` | `/api/assessment/submit` | Student | Finalize assessment, trigger ML pipeline, and compute recommendations |

*See [`docs/API_EXAMPLES.md`](file:///c:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/docs/API_EXAMPLES.md) for full request/response payloads.*

---

## 🎨 UI/UX Design System & Theme Engine

### 1. Flat Solid Design Philosophy (Zero Gradients)
The user interface follows a strict **zero-gradient, solid-color design system** engineered for maximum readability, focus, and visual clarity across mobile, tablet, and desktop screens.

### 2. Curated Color Palette

| Token Role | Light Mode Hex | Dark Mode Hex | Purpose |
| :--- | :---: | :---: | :--- |
| **Primary Brand** | `#1B2CC1` | `#7692FF` | Main CTAs, Active States, Key Metrics |
| **Secondary Accent** | `#7692FF` | `#98ACFF` | Supporting Highlights, Badges |
| **Page Canvas** | `#F8FAFC` | `#0F172A` | Base Viewport Background |
| **Surface Card** | `#FFFFFF` | `#1E293B` | Content Cards, Tables, Modals |
| **Subtle Card** | `#F1F5F9` | `#334155` | Table Headers, Inner Callouts, Filter Bars |
| **Text Main** | `#111827` | `#F8FAFC` | Headings, Primary Typography |
| **Text Secondary** | `#4B5563` | `#CBD5E1` | Body Text, Field Labels, Descriptions |
| **Border Outline** | `#E5E7EB` | `#334155` | Dividers, Card Outlines, Input Borders |
| **Success Feedback** | `#15803D` | `#22C55E` | Strong Match Badges, Completed Tests |
| **Warning Feedback** | `#B45309` | `#F59E0B` | In-Progress Status, Skipped Notices |

### 3. Dynamic Light / Dark Theme Switcher
- Instant `<head>` initialization queries `localStorage` and `prefers-color-scheme` to prevent any flash of unstyled content.
- Broadcasts a `themechange` JavaScript event so Chart.js Radar and Bar visualizers re-render dynamically with optimized dark/light gridline contrast.

---

## 🧪 Automated Verification Suite

The repository includes a comprehensive, multi-layer automated test suite spanning model integrity, concurrency, API endpoints, scoring logic, and real student lifecycle flows.

```powershell
python -m unittest discover tests
```

### Verified Test Breakdown:
- `tests/test_ml_model_loading.py` — Verifies singleton thread-safety, schema validation, and threshold loading.
- `tests/test_ml_feature_builder.py` — Validates 8-D ability match and 10-D interest match calculations.
- `tests/test_ml_prediction.py` — Validates preprocessor pipeline transformation and probability calculations.
- `tests/test_ml_recommendation.py` — Validates 1,206 career catalogue scoring and monotonic rank sorting.
- `tests/test_ml_integrity_and_security.py` — Validates SHA-256 model checksums and path traversal protections.
- `tests/test_ml_concurrency_and_performance.py` — Tests multi-threaded concurrent recommendation requests.
- `tests/test_e2e_real_student_flow.py` — Tests complete student journey (*Register $\rightarrow$ Login $\rightarrow$ Assessment $\rightarrow$ ML Evaluation $\rightarrow$ Results UI*).
- Full regression tests covering auth, assessment scoring, career search, and admin management.

```
Ran 73 tests in 17.421s

OK (73 passed, 0 failed, 0 errors)
```

---

## 📄 License & Attribution
Developed as part of the **Personalized Career Recommendation System Research Initiative**. Distributed under the MIT License.

<div align="center">

<img src="frontend/static/banner.jpg" alt="PathFinder — AI Career Guidance" width="100%" />

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12%20|%203.13-FFD43B?style=for-the-badge&logo=python&logoColor=306998)
![Flask](https://img.shields.io/badge/Flask-3.0+-black?style=for-the-badge&logo=flask&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-Classifier-00ADD8?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-00758F?style=for-the-badge&logo=mysql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)

![Tests](https://img.shields.io/badge/Tests-83%2F83%20Passing-00C851?style=for-the-badge&logo=pytest&logoColor=white)
![Classes](https://img.shields.io/badge/Classes-7%20to%2012-8B5CF6?style=for-the-badge)
![Careers](https://img.shields.io/badge/Careers-1%2C203%20in%20Catalogue-FF69B4?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-6366F1?style=for-the-badge)

<h3>🧭 Personalized Career Recommendation System Using Machine Learning</h3>
<p><em>AI-powered psychometric assessment and career guidance for Indian secondary school students — Classes 7 to 12</em></p>

</div>

---

## 🌟 What This Project Does

PathFinder is a full-stack web application that takes an Indian school student (Class 7–12) through a structured **psychometric and aptitude assessment**, then uses a trained **CatBoost machine learning model** (V9.5-Champion) to rank all 1,203 careers in its knowledge base by compatibility with that student's unique cognitive profile.

The system does **not** recommend careers based on a simple personality quiz. It:

1. 📝 Administers a **class-adaptive assessment** (50–55 questions selected from a bank of 413, tailored to the student's class and stream)
2. 🧮 Computes **22 normalized dimension scores** (abilities, interests, work preferences) from the student's answers
3. 🔢 Constructs an **19-feature engineering vector** per career candidate using those scores
4. 🤖 Runs the feature matrix through a **trained CatBoost Classifier** to get a compatibility probability for every career in the catalogue
5. 🛡️ Applies **domain-level prerequisite compliance checks** from `config.yaml` to ensure realistic recommendations
6. 🏆 Produces a **ranked Top-K recommendation list** with compatibility scores, ability match, interest match, and skill gap explanations

---

## 📊 System at a Glance

<div align="center">

| 🏷️ Metric | 📈 Value |
| :--- | :--- |
| 🤖 **Champion ML Model** | **CatBoost Classifier** (V9.5-Champion) with ColumnTransformer Preprocessor |
| 🎯 **Hit@1** | **96.03%** |
| 🔥 **Hit@3** | **99.64%** |
| 💯 **Hit@5** | **99.89%** |
| 📊 **MRR** | **0.9781** |
| 📐 **NDCG@5** | **0.9211** |
| 🎓 **Classification Accuracy** | **86.22%** |
| 🏆 **F1-Score** | **0.9154 (91.54%)** |
| 📈 **ROC-AUC** | **86.04% / 92.14%** |
| 💼 **Career Catalogue** | **1,203 careers** across 33 domains |
| ❓ **Question Bank** | **413 questions**, 1,805 scored answer options |
| 🏫 **Supported Classes** | Class 7 to Class 12 (Middle, Secondary, Higher Secondary) |
| 🧠 **Scored Dimensions** | **22 cognitive, interest, and behavioral dimensions** |
| 🔢 **ML Feature Vector** | **19 features** (11 numerical + 4 categorical + age, class, stream) |
| 🗄️ **Database** | MySQL 8.x — 18 relational tables |
| 🧪 **Test Suite** | **83 / 83 tests passing** |

</div>

---

## 🎓 Student Journey — How It Works

```mermaid
flowchart LR
    classDef step fill:#1E1B4B,stroke:#818CF8,stroke-width:2px,color:#E0E7FF
    classDef ml fill:#14532D,stroke:#4ADE80,stroke-width:2px,color:#DCFCE7
    classDef out fill:#7C2D12,stroke:#FB923C,stroke-width:2px,color:#FEF3C7

    A["🔐 Register / Login"]:::step
    B["👤 Complete Profile\n(Class, Stream, Marks)"]:::step
    C["📝 Read Instructions\n(Timed or Standard mode)"]:::step
    D["📋 Adaptive Assessment\n(50–55 questions, auto-saved)"]:::step
    E["✅ Review & Submit"]:::step
    F["🧮 ScoringService\n22-dimension normalization"]:::ml
    G["🔢 FeatureBuilder\n19-feature vector × 1,203 careers"]:::ml
    H["🤖 CatBoost Inference\nCompatibility probabilities"]:::ml
    I["🛡️ Compliance Check\nDomain threshold config.yaml"]:::ml
    J["🏆 Top-K Ranking\nSorted by compliance → score → ability → interest"]:::ml
    K["📊 Results Dashboard\nRadar charts + career explanations"]:::out

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K
```

---

## 📝 Adaptive Assessment Engine

The assessment is **not a fixed quiz**. The `AssessmentSelectionService` selects a personalized, randomized question set for every student on every attempt.

### 🏫 Cohort Question Targets

<div align="center">

| 🏫 Cohort | 🏛️ Classes | ❓ Questions Delivered | 📚 Difficulty Mix |
| :---: | :---: | :---: | :--- |
| **Middle School** | 7 & 8 | **50** | Easy + Medium |
| **Secondary** | 9 & 10 | **52** | Easy + Medium + Hard |
| **Higher Secondary** | 11 & 12 | **55** | Medium + Hard + Easy |

</div>

### 📚 Question Bank — 19 Sections, 413 Questions

<div align="center">

| # | 📖 Section | ❓ Questions | 🎯 What It Measures |
| :---: | :--- | :---: | :--- |
| 1 | 🎓 Academic Profile | 30 | Learning preferences, study habits, subject focus |
| 2 | ➗ Mathematical Ability | 75 | Numerical computation, algebra, quantitative reasoning |
| 3 | 🧠 Logical Reasoning | 42 | Pattern detection, deductive argument, syllogism |
| 4 | 🔬 Scientific Thinking | 37 | Hypothesis, variable isolation, empirical deduction |
| 5 | 🧩 Problem Solving | 20 | Multi-step constraint solving, root-cause analysis |
| 6 | 📊 Analytical Thinking | 18 | Graph interpretation, data synthesis, inference |
| 7 | 💬 Communication | 12 | Verbal clarity, written articulation, presentation |
| 8 | 🎨 Creativity | 12 | Lateral thinking, design intuition, original ideation |
| 9 | 💻 Digital Ability | 21 | Computational thinking, digital fluency, cyber awareness |
| 10 | 📖 Learning Ability | 12 | Cognitive agility, self-directed learning |
| 11 | 🗺️ Spatial Ability | 12 | 3D rotation, geometric visualization, structural layout |
| 12 | 🔧 Practical Ability | 10 | Hands-on aptitude, mechanical intuition |
| 13 | ❤️ Core Interests | 46 | Technology, Engineering, Healthcare, Business, Research, Arts |
| 14 | 🎯 Activities & Hobbies | 20 | Extracurricular engagement and recreational preferences |
| 15 | 🤝 Teamwork | 8 | Collaborative execution, consensus-building |
| 16 | 👑 Leadership | 8 | Initiative, responsibility-taking, vision |
| 17 | 🏢 Work Preferences | 10 | Indoor/outdoor, structure, autonomy preferences |
| 18 | 🔭 Career Awareness | 10 | Exposure to occupational landscape |
| 19 | 🗺️ Career Preferences | 10 | Expressed career direction and aspiration |
| | **Total** | **413** | |

</div>

**Key features of the selection engine:**
- ✅ **Section quotas** — every cohort is guaranteed a minimum number of questions per section
- 🔄 **Attempt differentiation** — students who retake the assessment receive a fresh set with different questions
- 🎲 **Randomization** — within each section, questions are shuffled every session
- 📱 **Auto-save** — every answer is saved immediately via `/api/assessment/answer` (no data loss)
- 🔍 **Stream filtering** — Class 11/12 questions are filtered by stream (PCM, PCB, Commerce, Humanities)

---

## 🧮 Scoring — 22 Dimensions

After submission, `ScoringService` processes every recorded answer and computes **22 normalized scores (0–100)**:

### 🧠 8 Cognitive & Aptitude Abilities

| Dimension | How Scored |
| :--- | :--- |
| `mathematical_ability` | MCQ/Scenario points ÷ max possible × 100 |
| `logical_reasoning` | MCQ/Scenario points ÷ max possible × 100 |
| `scientific_reasoning` | MCQ/Scenario points ÷ max possible × 100 |
| `problem_solving` | MCQ/Scenario points ÷ max possible × 100 |
| `analytical_ability` | MCQ/Scenario points ÷ max possible × 100 |
| `communication` | MCQ/Scenario points ÷ max possible × 100 |
| `creativity` | MCQ/Scenario points ÷ max possible × 100 |
| `digital_ability` | MCQ/Scenario points ÷ max possible × 100 |

### 🌟 Additional Scored Dimensions

`learning_ability` · `memory` · `observation` · `spatial_ability` · `practical_ability` · `teamwork` · `leadership`

### ❤️ 7 Interest Dimensions

`technology_interest` · `science_interest` · `healthcare_interest` · `business_interest` · `creative_interest` · `research_interest` · `social_interest`

> [!NOTE]
> Interest scores that have no direct questions are **inferred** from correlated ability scores. For example, `research_interest = 0.6 × scientific_reasoning + 0.4 × analytical_ability`. This prevents zero-score gaps in the student profile.

**Score Bands** used across the Results Dashboard:

| 🏷️ Band | 📊 Range | 📝 Meaning |
| :---: | :---: | :--- |
| 🟢 **Excellent** | 80.5 – 100 | Strong conceptual mastery and high affinity |
| 🔵 **Good** | 60.5 – 80.4 | Solid capability with positive aptitude indicators |
| 🟡 **Average** | 40.5 – 60.4 | Moderate proficiency with room to grow |
| 🟠 **Low** | 20.5 – 40.4 | Foundational stage; supplementary practice recommended |
| 🔴 **Very Low** | 0 – 20.4 | Minimal exposure or current interest |

---

## 🤖 Machine Learning Pipeline

### 🔢 Feature Engineering — 19 Features Per Career Candidate

The `FeatureBuilder` constructs one feature row per career (producing a matrix of 1,203 rows) using these formulas:

<div align="center">

| # | 🏷️ Feature | 📐 Formula |
| :---: | :--- | :--- |
| 1 | `ability_match_component` | `mean(100 − |student_ability − required_ability|)` across **8 cognitive dimensions** |
| 2 | `interest_match_component` | Weighted `mean(100 − |student_interest − required_interest|)` across **10 interest dimensions** |
| 3 | `academic_match_component` | Student's overall academic percentage (0–100) |
| 4 | `learning_match_component` | Student's `learning_ability` score (0–100) |
| 5 | `composite_alignment_index` | `0.45 × ability + 0.35 × interest + 0.10 × academic + 0.10 × learning` |
| 6 | `ability_interest_synergy` | `(ability × interest) / 100` |
| 7 | `ability_interest_gap` | `|ability − interest|` |
| 8 | `min_core_match` | `min(ability, interest)` |
| 9 | `max_core_match` | `max(ability, interest)` |
| 10 | `harmonic_core_match` | `2ab / (a + b)` |
| 11 | `geometric_core_synergy` | `√(ability × interest)` |
| 12 | `holistic_synergy` | `(ability × interest × academic × learning)^0.25` |
| 13 | `age` | Student age (clamped 10–30) |
| 14 | `class` | Class level (clamped 7–12) |
| 15 | `career_name` | Career name (categorical, OrdinalEncoded) |
| 16 | `career_domain` | Domain name (categorical, OrdinalEncoded) |
| 17 | `career_subdomain` | Subdomain (categorical, OrdinalEncoded) |
| 18 | `career_cluster` | Cluster (categorical, OrdinalEncoded) |
| 19 | `stream` | Student stream — General / PCM / PCB / Commerce / Humanities |

</div>

### ⚡ Dynamic Interest Weighting

The top **3 student interests** (by score) receive a **1.5× boost** during interest match computation. This ensures a student who is highly interested in Engineering will have that dimension weighted more when evaluating engineering careers.

```yaml
# backend/ml/config.yaml
interest_boost_factor: 1.5   # Boost multiplier applied to top interests
top_n_interests: 3           # Number of interests to boost
```

### 🛡️ Domain Prerequisite Compliance Check

After CatBoost predicts probabilities for all 1,203 careers, each career is checked against minimum prerequisite requirements for its domain:

```yaml
domain_requirements:
  healthcare:
    scientific_reasoning: 60    # Career must REQUIRE ≥ 60% scientific reasoning
    mathematical_ability: 60    # Career must REQUIRE ≥ 60% mathematical ability
  engineering:
    engineering_interest: 55    # Career must REQUIRE ≥ 55% engineering interest
  arts:
    arts_interest: 50

default_requirements:           # Applied to all other domains
  required_scientific_thinking: 50
  required_mathematical_ability: 50
```

A `threshold_pass` flag (1 = compliant, 0 = non-compliant) is computed. **Compliant careers always rank above non-compliant ones.** The final sort order is:

```
threshold_pass DESC  →  probability DESC  →  ability_match DESC  →  interest_match DESC
```

### 🏆 Model Performance

<div align="center">

| 📊 Metric | 🎯 Score |
| :---: | :---: |
| **Champion Model** | **CatBoost Classifier** (`V9.5-Champion`) |
| **Classification Accuracy** | **86.22%** |
| **F1-Score** | **0.9154 (91.54%)** |
| **ROC-AUC** | **86.04% / 92.14%** |
| **Hit@1 (Top 1 Accuracy)** | **96.03%** |
| **Hit@3 (Top 3 Recall)** | **99.64%** |
| **Hit@5 (Top 5 Recall)** | **99.89%** |
| **Hit@10 (Top 10 Recall)** | **99.95%** |
| **Mean Reciprocal Rank (MRR)** | **0.9781** |
| **NDCG@5 (Normalized DCG)** | **0.9211** |

</div>

---

## 💼 Career Catalogue & Explorer

The system maintains **1,203 active careers** organized in a 3-level taxonomy:

```
33 Domains  →  Subdomains  →  Clusters  →  1,203 Careers
```

For each career, the database stores:
- 📋 Description, minimum and typical education
- 🏢 Work environment (Indoor / Outdoor / Hybrid / Remote)
- 🧠 Required ability levels for all 8 cognitive dimensions
- ❤️ Required interest levels for all 10 interest dimensions
- 📚 Prerequisite subjects and recommended academic pathway
- 🗺️ 5-stage career education roadmap (with course links)
- 🛠️ Required skills and competencies

The **Career Explorer** page at `/careers` supports:
- 🔍 Full-text search by career name
- 🌐 Filter by Domain, Subdomain, Cluster
- 🎓 Filter by education level
- 🏢 Filter by work environment
- 📄 Paginated results (24 per page)

---

## 🖥️ Application Pages

<div align="center">

| 🔗 Route | 👤 Access | 📝 Page |
| :--- | :---: | :--- |
| `/` | All | 🏠 Home — domain highlights, sample careers, AI disclosure |
| `/register` | Guest | 📝 Student registration (Class 7–12) |
| `/login` | Guest | 🔐 Login (email or username + password) |
| `/dashboard` | Student | 📊 Overview — latest scores, top 3 recommendations, attempt history |
| `/profile` | Student | 👤 Profile editor — personal info, academic marks (17 subjects), stream |
| `/assessment/instructions` | Student | 📖 Pre-test guidelines and mode selection |
| `/assessment` | Student | 📋 Adaptive assessment — sectioned MCQ/Rating/Scenario questions |
| `/assessment/review` | Student | 🔍 Review answers before final submission |
| `/assessment/results/<id>` | Student/Admin | 📊 Full results — radar charts, score breakdown, career recommendations |
| `/careers` | All | 🔍 Career Explorer — search, filter, browse 1,203 careers |
| `/careers/<id>` | All | 💼 Career detail — description, skills, education path |
| `/careers/<id>/roadmap` | All | 🗺️ 5-stage career education roadmap |
| `/admin/` | Admin | 🛠️ Admin dashboard — system stats and recent sessions |
| `/admin/users` | Admin | 👥 Student management — search, filter, view history |
| `/admin/questions` | Admin | ❓ Question bank browser — filter by class, section |
| `/admin/careers` | Admin | 💼 Career catalogue manager |

</div>

---

## 🔌 REST API Reference

<details open>
<summary><b>📋 Assessment API</b></summary>

| Method | Endpoint | Auth | Description |
| :---: | :--- | :---: | :--- |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/questions/<class_level>` | ❌ | Fetch adaptive questions for a class level and stream |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | `/api/assessment/start` | ✅ | Start a new assessment session |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | `/api/assessment/answer` | ✅ | Auto-save one answer (session_id, question_id, selected_option) |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | `/api/assessment/submit` | ✅ | Submit session → triggers scoring + ML inference + recommendations |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/assessment/<id>/scores` | ✅ | Retrieve normalized 22-dimension score record |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/assessment/<id>/profile` | ✅ | Full synthesized student profile (abilities, interests, strengths, gaps) |

</details>

<details>
<summary><b>💼 Career & Recommendations API</b></summary>

| Method | Endpoint | Auth | Description |
| :---: | :--- | :---: | :--- |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/careers` | ❌ | Search careers (q, domain_id, subdomain_id, cluster_id, education, environment) |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/careers/<id>` | ❌ | Career detail with skills, subjects, roadmap |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/careers/domains` | ❌ | All 33 career domains |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/careers/subdomains/<domain_id>` | ❌ | Subdomains under a domain |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/careers/clusters/<subdomain_id>` | ❌ | Clusters under a subdomain |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | `/api/recommendations` | ❌ | Generate recommendations from session_id or raw student profile payload |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/recommendations/<assessment_id>` | ✅ | Retrieve saved recommendations for a session |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/recommendations/student/<student_id>` | ✅ | Recommendations for latest completed session of a student |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | `/api/predictions` | ❌ | Raw ML prediction from feature vector (direct CatBoost call) |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/health` | ❌ | System health — model, preprocessor, catalogue, DB status |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/model/info` | ❌ | Model version, features, classification metrics, ranking metrics |

</details>

<details>
<summary><b>👤 Student Profile API</b></summary>

| Method | Endpoint | Auth | Description |
| :---: | :--- | :---: | :--- |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat-square) | `/api/student/profile` | ✅ | Get current student's profile and academic scores |
| ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | `/api/student/profile` | ✅ | Update profile fields and all 17 academic subject scores |

</details>

---

## ⚙️ Installation

> [!IMPORTANT]
> Requires **Python 3.10+**, **MySQL Server 8.0+**, and the trained model artifacts in `backend/ml/models/`.

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### 2️⃣ Configure Environment

```bash
cp .env.example .env
```

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_recommendation_db
SECRET_KEY=your_secret_key
```

### 3️⃣ Initialize Database

Run the single consolidated SQL file which creates all **18 tables** and seeds all data:

```bash
mysql -u root -p < setup.sql
```

> Seeds: 413 questions · 1,805 answer options · 1,203 careers · 33 domains · demo accounts

### 4️⃣ Run

```bash
python run.py
# Open http://127.0.0.1:5000
```

---

## 🔑 Demo Credentials

> [!WARNING]
> Change these passwords before any public deployment.

<div align="center">

| 👤 Role | 🔐 Username | 🗝️ Password | 📝 Access Level |
| :---: | :---: | :---: | :--- |
| 🛠️ **Admin** | `admin` | `Admin@123` | Full admin panel — users, questions, careers, sessions |
| 🎓 **Student** | `rahul_sharma_12` | `Student@123` | Class 12 Science-PCB student with completed assessment history |

</div>

New accounts can be self-registered at `/register` for any class 7–12.

---

## 🧪 Testing

```bash
python -m unittest discover -s tests -v
```

```
----------------------------------------------------------------------
Ran 83 tests in ~18s

OK  (83 passed, 0 failures)
```

<details>
<summary><b>📋 Full Test Module List</b></summary>

<br/>

| 🧪 Module | 🔢 Tests | 📝 What Is Tested |
| :--- | :---: | :--- |
| `test_ml_model_loading` | 3 | Artifact existence, singleton loader, `ModelArtifactError` on missing files |
| `test_ml_prediction` | 4 | Feature vector → probability output, batch prediction, threshold application |
| `test_ml_feature_builder` | 2 | `calculate_ability_match`, `calculate_interest_match`, alias resolution |
| `test_ml_recommendation` | 3 | Full 1,203-career catalogue load, Top-K extraction, result key structure |
| `test_ml_concurrency_and_performance` | 2 | 5 and 10 simultaneous recommendation requests |
| `test_ml_integrity_and_security` | 3 | SHA-256 artifact hashes, `.gitignore` model exclusion, path traversal |
| `test_ml_api_endpoints` | 5 | `/api/health`, `/api/model/info`, `/api/predictions`, `/api/recommendations` |
| `test_assessment_workflow` | 12 | Session lifecycle across all class cohorts: start → answer → submit → results |
| `test_assessment_selection` | 4 | Section quotas, cohort target counts, stream filtering, attempt differentiation |
| `test_scoring` | 2 | Score normalization, `get_score_category` bands |
| `test_scoring_deterministic` | 5 | 0%, 50%, 80%, 100% correctness; ability/interest dimension independence |
| `test_student_profile_and_baseline` | 3 | Profile creation, `/api/assessment/<id>/profile` response, baseline matching |
| `test_questionnaire_validation_comprehensive` | 5 | Class bounds (7–12), academic score bounds (0–100), sensitive field handling |
| `test_auth` | 3 | Registration, login with email/username, logout |
| `test_e2e_real_student_flow` | 4 | End-to-end: register → profile → assess → submit → recommendations |
| `test_admin_and_user_history` | 5 | Admin session audit, per-student attempt history, answer inspection |
| `test_admin` | 3 | Admin-only route guards, dashboard stats |
| `test_assessment` | 3 | Session init, question delivery, completion percentage tracking |
| `test_career` | 2 | Explorer page rendering, career detail, roadmap page |
| `test_career_import` | 9 | Career CSV import pipeline — domain mapping, duplicate handling, validation |
| | **83** | ✅ **100% Passing** |

</details>

---

## 📦 Tech Stack

<div align="center">

| Layer | Technology |
| :---: | :--- |
| 🐍 **Backend** | Python 3.10+, Flask 3.0+, Flask-Login, Flask-Bcrypt, Flask-SQLAlchemy |
| 🗄️ **Database** | MySQL 8.x via `mysql-connector-python` / `PyMySQL` |
| 🤖 **ML Champion** | **CatBoost 1.2+**, scikit-learn 1.4+, pandas 2.1+, numpy 1.24+, joblib |
| 📊 **Analysis & Ensembles** | XGBoost 2.0+, LightGBM 4.3+, SHAP 0.45+, matplotlib 3.8+, seaborn 0.13+ |
| 🎨 **Frontend** | Jinja2 templates, Bootstrap 5.3, Chart.js (Radar + Bar charts) |
| 🔐 **Security** | bcrypt password hashing, Flask-Login session management, CSRF |
| 🧪 **Testing** | Python `unittest`, isolated SQLite in-memory test database |

</div>

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-00ADD8?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap%205-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

<br/>

### 🧭 *PathFinder — Helping every student find their best path forward.*

⭐ **Star this repository if it helped you!** ⭐

</div>

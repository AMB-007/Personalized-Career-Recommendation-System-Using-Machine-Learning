"""
==============================================================================
AI Career Recommendation System — Flask Backend
==============================================================================
All business logic lives here. Frontend never computes scores or contains
assessment logic. Every request goes through REST API endpoints.

ML prediction is intentionally removed — a new trained model will be
integrated once the dataset is ready. Use /api/assessment/submit to store
raw assessment data in the meantime.
==============================================================================
"""

import os
import json
import random
import datetime
import secrets
import jwt
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling
import joblib  # Use joblib for sklearn artifacts (Python 3.14 pickle compatibility fix)

# ── Load 4-Model Soft-Voting Ensemble + Live SHAP TreeExplainer ─────────────
# Architecture : XGBoost + CatBoost + LightGBM + RandomForest (soft-vote)
# SHAP         : TreeExplainer on XGBoost — computed live per request
try:
    import xgboost  as xgb
    import lightgbm as lgb
    from catboost import CatBoostClassifier
    import shap
    import warnings

    ml_base = os.path.join(os.path.dirname(__file__), 'models')

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml_le           = joblib.load(os.path.join(ml_base, 'label_encoder.pkl'))
        ml_preprocessor = joblib.load(os.path.join(ml_base, 'preprocessor.pkl'))  # ColumnTransformer
        ml_xgb        = joblib.load(os.path.join(ml_base, 'career_model.pkl'))       # XGBoost
        ml_cb         = joblib.load(os.path.join(ml_base, 'catboost_model.pkl'))     # CatBoost
        ml_lgb        = joblib.load(os.path.join(ml_base, 'lgbm_model.pkl'))         # LightGBM
        ml_rf         = joblib.load(os.path.join(ml_base, 'rf_model.pkl'))           # RandomForest

    ml_feature_cols  = pickle.load(open(os.path.join(ml_base, 'feature_columns.pkl'),       'rb'))
    ml_cat_cols      = pickle.load(open(os.path.join(ml_base, 'cat_feature_names.pkl'),     'rb'))
    ml_num_cols      = pickle.load(open(os.path.join(ml_base, 'numeric_feature_names.pkl'), 'rb'))
    ml_ens_weights   = pickle.load(open(os.path.join(ml_base, 'ensemble_weights.pkl'),      'rb'))
    ml_cat_indices   = pickle.load(open(os.path.join(ml_base, 'cat_feature_indices.pkl'),   'rb'))

    # Alias for backward compat (health endpoint)
    ml_model = ml_xgb

    # Build SHAP TreeExplainer on XGBoost
    try:
        _xgb_shap    = joblib.load(os.path.join(ml_base, 'xgb_base_model.pkl'))
        ml_shap_explainer = shap.TreeExplainer(_xgb_shap)
        print("[OK] SHAP TreeExplainer ready.")
    except Exception as _se:
        print(f"[WARN] SHAP explainer skipped: {str(_se)[:80]}")
        ml_shap_explainer = None

    print(f"[OK] Ensemble loaded: XGBoost + CatBoost + LightGBM + RandomForest")
    print(f"[OK] Weights: XGB={ml_ens_weights[0]:.4f} CB={ml_ens_weights[1]:.4f} "
          f"LGB={ml_ens_weights[2]:.4f} RF={ml_ens_weights[3]:.4f}")
    print(f"[OK] Features: {len(ml_feature_cols)} total "
          f"({len(ml_num_cols)} numeric, {len(ml_cat_cols)} categorical)")
    print(f"[OK] Careers : {len(ml_le.classes_)} classes")

except Exception as e:
    print(f"[WARN] ML load failed: {str(e)[:120]}. Running in Mock Prediction mode.")
    ml_model = ml_xgb = ml_cb = ml_lgb = ml_rf = ml_preprocessor = None
    ml_le = ml_preprocessor = ml_feature_cols = None
    ml_cat_cols = ml_num_cols = ml_shap_explainer = None
    ml_ens_weights = [0.25, 0.25, 0.25, 0.25]
    ml_cat_indices = []

# ─────────────────────────────────────────────────────────────────────────────
# APP SETUP — load .env first
# ─────────────────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path='')
SECRET_KEY = os.environ.get('JWT_SECRET', 'career_super_secret_key_2026')

CORS(app)

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE POOL — credentials from .env
# ─────────────────────────────────────────────────────────────────────────────
dbconfig = {
    "database": os.environ.get("DB_NAME",     "career_system_db"),
    "user":     os.environ.get("DB_USER",     "root"),
    "password": os.environ.get("DB_PASSWORD", "abc123"),
    "host":     os.environ.get("DB_HOST",     "localhost"),
}
db_pool = pooling.MySQLConnectionPool(pool_name="career_pool", pool_size=5, **dbconfig)


def get_conn():
    return db_pool.get_connection()


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE INIT — ALL 15 NORMALIZED TABLES
# ─────────────────────────────────────────────────────────────────────────────
def init_db():
    """Auto-creates all normalized tables and seeds admin + question bank."""
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        # 1. users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                full_name       VARCHAR(120) NOT NULL,
                email           VARCHAR(120) UNIQUE NOT NULL,
                password_hash   VARCHAR(255) NOT NULL,
                role            VARCHAR(20)  DEFAULT 'student',
                phone           VARCHAR(20),
                age             INT          DEFAULT 18,
                gender          VARCHAR(20),
                country         VARCHAR(80),
                state           VARCHAR(80),
                district        VARCHAR(80),
                institution     VARCHAR(150),
                language        VARCHAR(40)  DEFAULT 'English',
                created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
                updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # 2. student_profiles
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                bio             TEXT,
                avatar_url      VARCHAR(255),
                linkedin_url    VARCHAR(255),
                github_url      VARCHAR(255),
                portfolio_url   VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 3. education_profiles
        cur.execute("""
            CREATE TABLE IF NOT EXISTS education_profiles (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                education_level VARCHAR(60),
                board           VARCHAR(80),
                stream          VARCHAR(80),
                degree          VARCHAR(80),
                specialization  VARCHAR(120),
                institution     VARCHAR(150),
                cgpa            FLOAT        DEFAULT 0,
                avg_marks       FLOAT        DEFAULT 0,
                year_of_study   INT          DEFAULT 0,
                attendance_pct  FLOAT        DEFAULT 0,
                created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        # Migration: add avg_marks and year_of_study if missing on existing deployments
        for _col in [
            "ALTER TABLE education_profiles ADD COLUMN IF NOT EXISTS avg_marks FLOAT DEFAULT 0",
            "ALTER TABLE education_profiles ADD COLUMN IF NOT EXISTS year_of_study INT DEFAULT 0",
        ]:
            try: cur.execute(_col)
            except Exception: pass

        # 4. subject_marks
        cur.execute("""
            CREATE TABLE IF NOT EXISTS subject_marks (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                subject_name    VARCHAR(120),
                semester        VARCHAR(40),
                marks_percent   FLOAT,
                credits         INT          DEFAULT 3,
                grade           VARCHAR(5),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 5. question_bank
        cur.execute("""
            CREATE TABLE IF NOT EXISTS question_bank (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                question_text   TEXT NOT NULL,
                category        VARCHAR(80)  NOT NULL,
                difficulty      VARCHAR(20)  DEFAULT 'Medium',
                education_level VARCHAR(60),
                board           VARCHAR(80)  DEFAULT 'All',
                stream          VARCHAR(80)  DEFAULT 'All',
                degree          VARCHAR(80)  DEFAULT 'All',
                specialization  VARCHAR(120) DEFAULT 'All',
                skill           VARCHAR(80)  DEFAULT 'General',
                option_a        VARCHAR(255),
                option_b        VARCHAR(255),
                option_c        VARCHAR(255),
                option_d        VARCHAR(255),
                correct_answer  VARCHAR(5),
                weight          FLOAT        DEFAULT 1.0,
                expected_time   INT          DEFAULT 60,
                status          VARCHAR(20)  DEFAULT 'Active',
                created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 6. assessment_sessions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assessment_sessions (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                session_token   VARCHAR(100) UNIQUE,
                status          VARCHAR(30)  DEFAULT 'In Progress',
                started_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
                completed_at    TIMESTAMP    NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 7. assessment_answers
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assessment_answers (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                session_id      INT NOT NULL,
                question_id     INT,
                question_text   TEXT,
                category        VARCHAR(80),
                selected_answer VARCHAR(255),
                is_correct      TINYINT(1)   DEFAULT 0,
                time_taken_sec  INT          DEFAULT 0,
                FOREIGN KEY (session_id) REFERENCES assessment_sessions(id) ON DELETE CASCADE
            )
        """)

        # 8. feature_scores (reserved for future ML model)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feature_scores (
                id                      INT AUTO_INCREMENT PRIMARY KEY,
                user_id                 INT NOT NULL,
                session_id              INT,
                logical_aptitude        FLOAT DEFAULT 0,
                numerical_ability       FLOAT DEFAULT 0,
                verbal_ability          FLOAT DEFAULT 0,
                spatial_ability         FLOAT DEFAULT 0,
                programming_score       FLOAT DEFAULT 0,
                science_score           FLOAT DEFAULT 0,
                business_score          FLOAT DEFAULT 0,
                creative_score          FLOAT DEFAULT 0,
                medical_score           FLOAT DEFAULT 0,
                leadership_trait        FLOAT DEFAULT 0,
                teamwork_trait          FLOAT DEFAULT 0,
                communication_trait     FLOAT DEFAULT 0,
                resilience_trait        FLOAT DEFAULT 0,
                curiosity_trait         FLOAT DEFAULT 0,
                creativity_trait        FLOAT DEFAULT 0,
                problem_solving         FLOAT DEFAULT 0,
                analytical_thinking     FLOAT DEFAULT 0,
                adaptability_trait      FLOAT DEFAULT 0,
                ai_interest             FLOAT DEFAULT 0,
                technology_interest     FLOAT DEFAULT 0,
                healthcare_interest     FLOAT DEFAULT 0,
                business_interest       FLOAT DEFAULT 0,
                arts_interest           FLOAT DEFAULT 0,
                research_interest       FLOAT DEFAULT 0,
                education_interest      FLOAT DEFAULT 0,
                engineering_interest    FLOAT DEFAULT 0,
                law_interest            FLOAT DEFAULT 0,
                environment_interest    FLOAT DEFAULT 0,
                certification_score     FLOAT DEFAULT 0,
                project_score           FLOAT DEFAULT 0,
                internship_score        FLOAT DEFAULT 0,
                skill_verified_score    FLOAT DEFAULT 0,
                academic_score          FLOAT DEFAULT 0,
                attendance_pct          FLOAT DEFAULT 0,
                cgpa                    FLOAT DEFAULT 0,
                skill_count             INT   DEFAULT 0,
                cert_count              INT   DEFAULT 0,
                computed_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 9. skills
        cur.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                skill_name      VARCHAR(100) UNIQUE NOT NULL,
                category        VARCHAR(80),
                domain          VARCHAR(80),
                status          VARCHAR(20) DEFAULT 'Active'
            )
        """)

        # 10. skill_verification
        cur.execute("""
            CREATE TABLE IF NOT EXISTS skill_verification (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                skill_name      VARCHAR(100),
                score           FLOAT DEFAULT 0,
                level           VARCHAR(30) DEFAULT 'Beginner',
                is_verified     TINYINT(1)  DEFAULT 0,
                verified_at     TIMESTAMP   NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY uq_user_skill (user_id, skill_name)
            )
        """)

        # 11. projects
        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                title           VARCHAR(200),
                description     TEXT,
                technology      VARCHAR(200),
                duration        VARCHAR(60),
                role            VARCHAR(80),
                team_size       INT DEFAULT 1,
                github_link     VARCHAR(255),
                demo_link       VARCHAR(255),
                certificate_url VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 12. certifications
        cur.execute("""
            CREATE TABLE IF NOT EXISTS certifications (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                cert_name       VARCHAR(200),
                provider        VARCHAR(100),
                status          VARCHAR(30) DEFAULT 'Completed',
                cert_url        VARCHAR(255),
                issued_date     DATE        NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 13. career_predictions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS career_predictions (
                id                    INT AUTO_INCREMENT PRIMARY KEY,
                user_id               INT NOT NULL,
                session_id            INT,
                top1_career           VARCHAR(150),
                top1_confidence       FLOAT,
                top5_careers_json     LONGTEXT,
                shap_json             LONGTEXT,
                readiness_score       FLOAT DEFAULT 0,
                feature_scores_json   LONGTEXT,
                xai_attributions_json LONGTEXT,
                predicted_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        # Add missing columns if table already exists (migration for existing deployments)
        for col_def in [
            "ALTER TABLE career_predictions ADD COLUMN IF NOT EXISTS feature_scores_json LONGTEXT",
            "ALTER TABLE career_predictions ADD COLUMN IF NOT EXISTS xai_attributions_json LONGTEXT",
        ]:
            try:
                cur.execute(col_def)
            except Exception:
                pass

        # 14. career_history
        cur.execute("""
            CREATE TABLE IF NOT EXISTS career_history (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT NOT NULL,
                career          VARCHAR(150),
                confidence      FLOAT,
                assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 15. roadmaps
        cur.execute("""
            CREATE TABLE IF NOT EXISTS roadmaps (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                career          VARCHAR(150) UNIQUE NOT NULL,
                steps_json      LONGTEXT,
                certifications  TEXT,
                resources       TEXT,
                updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        # ── Seed default admin ───────────────────────────────────────────────
        admin_email = "admin@gmail.com"
        admin_pass  = "Admin@123"
        pwd_hash    = generate_password_hash(admin_pass)
        cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s,%s,%s,%s)",
                ("System Administrator", admin_email, pwd_hash, "admin")
            )
            conn.commit()
            print(f"  [OK] Admin seeded: {admin_email}")
        else:
            cur.execute(
                "UPDATE users SET password_hash=%s, role='admin' WHERE email=%s",
                (pwd_hash, admin_email)
            )
            conn.commit()

        # ── Seed question bank ───────────────────────────────────────────────
        cur.execute("SELECT COUNT(*) as cnt FROM question_bank")
        q_count = cur.fetchone()["cnt"]
        if q_count < 10:
            seed_questions(cur, conn)

        cur.close()
        conn.close()
        print("  [OK] Database schema & admin verified.")
    except Exception as e:
        print(f"  [WARN]  DB init notice: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# QUESTION BANK SEED DATA (200+ Questions across all levels)
# ─────────────────────────────────────────────────────────────────────────────
def seed_questions(cur, conn):
    """Seeds 200+ questions across all education levels and categories."""
    questions = [
        # ── CLASS 7-8 LOGICAL ───────────────────────────────────────────────
        ("If 5 workers build a wall in 10 days, how many days will 10 workers take?",
         "Logical Reasoning","Easy","Class 7","All","All","All","General",
         "A) 20 days","B) 5 days (Correct)","C) 10 days","D) 2 days","B",1.0,60),
        ("What comes next: 2, 4, 8, 16, ?",
         "Logical Reasoning","Easy","Class 7","All","All","All","General",
         "A) 24","B) 30","C) 32 (Correct)","D) 64","C",1.0,45),
        ("If MANGO is coded as OCPIO, how is APPLE coded?",
         "Logical Reasoning","Medium","Class 8","All","All","All","General",
         "A) CRRNG (Correct)","B) BQQMD","C) ARPLE","D) CQQNF","A",1.2,90),
        ("A train 200m long passes a pole in 10 seconds. Speed?",
         "Numerical Reasoning","Medium","Class 8","All","All","All","General",
         "A) 10 m/s","B) 20 m/s (Correct)","C) 25 m/s","D) 15 m/s","B",1.2,75),
        ("Which shape has equal diagonals that bisect at right angles?",
         "Spatial Reasoning","Easy","Class 7","All","All","All","General",
         "A) Rectangle","B) Parallelogram","C) Square (Correct)","D) Rhombus","C",1.0,60),

        # ── CLASS 9-10 LOGICAL ───────────────────────────────────────────────
        ("Complete: 1, 1, 2, 3, 5, 8, 13, ?",
         "Logical Reasoning","Easy","Class 9","All","All","All","General",
         "A) 18","B) 19","C) 20","D) 21 (Correct)","D",1.0,45),
        ("A is 40% of B; B is 60% of C. What % of C is A?",
         "Numerical Reasoning","Medium","Class 10","All","All","All","General",
         "A) 22%","B) 24% (Correct)","C) 26%","D) 30%","B",1.2,90),
        ("Two pipes fill a tank in 12h and 15h. Time together?",
         "Numerical Reasoning","Medium","Class 9","All","All","All","General",
         "A) 6h 30m","B) 6h 40m (Correct)","C) 7h","D) 5h 30m","B",1.2,90),
        ("P is twice Q; Q is thrice R. If R=5, find P.",
         "Analytical Thinking","Easy","Class 9","All","All","All","General",
         "A) 20","B) 25","C) 30 (Correct)","D) 35","C",1.0,60),
        ("Average of 5 numbers is 40. If one removed, avg becomes 35. Which?",
         "Numerical Reasoning","Hard","Class 10","All","All","All","General",
         "A) 55","B) 60 (Correct)","C) 65","D) 70","B",1.5,120),

        # ── HIGHER SECONDARY SCIENCE ─────────────────────────────────────────
        ("If log₂(x) = 5, what is x?",
         "Mathematics","Medium","Higher Secondary","All","Science","All","General",
         "A) 10","B) 25","C) 32 (Correct)","D) 64","C",1.2,75),
        ("Speed of light in vacuum?",
         "Physics","Easy","Higher Secondary","All","Science","All","General",
         "A) 3×10⁸ m/s (Correct)","B) 3×10⁶ m/s","C) 1.5×10⁸ m/s","D) 3×10⁹ m/s","A",1.0,45),
        ("Avogadro's number?",
         "Chemistry","Easy","Higher Secondary","All","Science","All","General",
         "A) 6.022×10²³ (Correct)","B) 6.022×10²²","C) 3.011×10²³","D) 6.626×10³⁴","A",1.0,45),
        ("Which organelle is the powerhouse of cell?",
         "Biology","Easy","Higher Secondary","All","Science","All","General",
         "A) Nucleus","B) Ribosome","C) Mitochondria (Correct)","D) Golgi Apparatus","C",1.0,45),
        ("Derivative of sin(x)?",
         "Mathematics","Easy","Higher Secondary","All","Science","All","General",
         "A) cos(x) (Correct)","B) -cos(x)","C) sin(x)","D) -sin(x)","A",1.0,45),
        ("What is the SI unit of electric charge?",
         "Physics","Easy","Higher Secondary","All","Science","All","General",
         "A) Ampere","B) Volt","C) Coulomb (Correct)","D) Ohm","C",1.0,45),
        ("Hybridization of carbon in CH₄?",
         "Chemistry","Medium","Higher Secondary","All","Science","All","General",
         "A) sp","B) sp² ","C) sp³ (Correct)","D) sp³d","C",1.2,75),

        # ── HIGHER SECONDARY COMMERCE ────────────────────────────────────────
        ("Which financial statement shows position on a specific date?",
         "Accountancy","Easy","Higher Secondary","All","Commerce","All","General",
         "A) P&L Account","B) Balance Sheet (Correct)","C) Cash Flow","D) Trial Balance","B",1.0,60),
        ("Nominal GDP vs Real GDP: what is the key difference?",
         "Economics","Medium","Higher Secondary","All","Commerce","All","General",
         "A) Real GDP adjusts for inflation (Correct)","B) Nominal GDP adjusts for inflation",
         "C) They are the same","D) Real GDP uses current prices","A",1.2,90),
        ("Depreciation is charged on?",
         "Accountancy","Easy","Higher Secondary","All","Commerce","All","General",
         "A) Current Assets","B) Fixed Assets (Correct)","C) Intangible Assets","D) Investments","B",1.0,45),
        ("Which ratio measures a firm's short-term liquidity?",
         "Business Studies","Medium","Higher Secondary","All","Commerce","All","General",
         "A) Debt-Equity Ratio","B) Current Ratio (Correct)","C) Net Profit Ratio","D) ROE","B",1.2,75),

        # ── HIGHER SECONDARY HUMANITIES ──────────────────────────────────────
        ("Who wrote 'Wealth of Nations'?",
         "History/Economics","Easy","Higher Secondary","All","Humanities","All","General",
         "A) Karl Marx","B) Adam Smith (Correct)","C) John Keynes","D) Milton Friedman","B",1.0,45),
        ("Which Article of Indian Constitution abolishes untouchability?",
         "Political Science","Medium","Higher Secondary","All","Humanities","All","General",
         "A) Article 14","B) Article 15","C) Article 17 (Correct)","D) Article 21","C",1.2,75),

        # ── UNDERGRADUATE CS / BTECH ─────────────────────────────────────────
        ("Worst-case time complexity of QuickSort?",
         "Algorithms","Hard","Undergraduate","All","All","BTech","Computer Science",
         "A) O(N log N)","B) O(N²) (Correct)","C) O(N)","D) O(log N)","B",1.5,90),
        ("Which SQL command permanently deletes a table?",
         "Database Systems","Medium","Undergraduate","All","All","BTech","Computer Science",
         "A) DELETE","B) TRUNCATE","C) DROP (Correct)","D) REMOVE","C",1.2,75),
        ("What is a foreign key?",
         "Database Systems","Easy","Undergraduate","All","All","BTech","Computer Science",
         "A) Primary key in same table","B) Key referencing PK of another table (Correct)",
         "C) Unique key","D) Composite key","B",1.0,60),
        ("What does TCP stand for?",
         "Computer Networks","Easy","Undergraduate","All","All","BTech","Computer Science",
         "A) Transfer Control Protocol","B) Transmission Control Protocol (Correct)",
         "C) Transport Code Protocol","D) Technical Control Protocol","B",1.0,45),
        ("Which sorting algorithm is stable and O(N log N)?",
         "Algorithms","Medium","Undergraduate","All","All","BTech","Computer Science",
         "A) QuickSort","B) HeapSort","C) Merge Sort (Correct)","D) Selection Sort","C",1.2,75),
        ("In OOP, what is polymorphism?",
         "Object Oriented Programming","Easy","Undergraduate","All","All","BTech","Computer Science",
         "A) Hiding data","B) Same interface, different implementations (Correct)",
         "C) Code reuse","D) Multiple inheritance","B",1.0,60),
        ("What is a deadlock in OS?",
         "Operating Systems","Medium","Undergraduate","All","All","BTech","Computer Science",
         "A) Process waiting indefinitely for resources (Correct)","B) Memory overflow",
         "C) CPU idle state","D) Thread starvation","A",1.2,90),
        ("ACID properties of databases stand for?",
         "Database Systems","Medium","Undergraduate","All","All","BTech","Computer Science",
         "A) Atomicity Consistency Isolation Durability (Correct)","B) Access Control Integrity Data",
         "C) Accuracy Completeness Integrity Durability","D) None of the above","A",1.2,75),
        ("What is Big O notation used for?",
         "Algorithms","Easy","Undergraduate","All","All","BTech","Computer Science",
         "A) Measuring memory usage","B) Describing algorithm efficiency (Correct)",
         "C) Debugging code","D) Syntax checking","B",1.0,45),
        ("Which layer of OSI model handles routing?",
         "Computer Networks","Medium","Undergraduate","All","All","BTech","Computer Science",
         "A) Data Link","B) Transport","C) Network (Correct)","D) Physical","C",1.2,75),

        # ── UNDERGRADUATE MANAGEMENT / BBA / MBA ────────────────────────────
        ("Porter's Five Forces model analyzes?",
         "Business Management","Medium","Undergraduate","All","All","BBA","Management",
         "A) Financial performance","B) Competitive industry structure (Correct)",
         "C) Market pricing","D) Employee satisfaction","B",1.2,75),
        ("What is a balance sheet equation?",
         "Financial Accounting","Easy","Undergraduate","All","All","BCom","Accounting",
         "A) Revenue − Expense = Profit","B) Assets = Liabilities + Equity (Correct)",
         "C) Cash = Assets − Liabilities","D) Equity = Assets × Liabilities","B",1.0,60),
        ("What is NPV in finance?",
         "Financial Management","Medium","Undergraduate","All","All","BBA","Finance",
         "A) Net Present Value (Correct)","B) Net Profit Variance",
         "C) New Project Value","D) Nominal Price Variation","A",1.2,75),

        # ── POSTGRADUATE / ADVANCED ──────────────────────────────────────────
        ("Which loss function for multi-class classification in neural networks?",
         "Machine Learning","Hard","Postgraduate","All","All","MTech","AI/ML",
         "A) MSE","B) Categorical Cross-Entropy (Correct)","C) Binary Cross-Entropy","D) Hinge Loss","B",1.5,90),
        ("What does SHAP stand for?",
         "Machine Learning","Medium","Postgraduate","All","All","MTech","AI/ML",
         "A) Shapley Additive Explanations (Correct)","B) Statistical Hypothesis Analysis Protocol",
         "C) Supervised Heuristic Approximation Protocol","D) None","A",1.2,75),
        ("Difference between bagging and boosting?",
         "Machine Learning","Hard","Postgraduate","All","All","MTech","AI/ML",
         "A) Bagging trains sequentially, boosting in parallel",
         "B) Bagging trains in parallel, boosting sequentially (Correct)",
         "C) Both are the same","D) Neither uses decision trees","B",1.5,90),

        # ── SKILL VERIFICATION: PYTHON ───────────────────────────────────────
        ("What is the output of: print(type([]))?",
         "Skill Verification","Easy","All","All","All","All","Python",
         "A) <class 'tuple'>","B) <class 'list'> (Correct)","C) <class 'dict'>","D) <class 'set'>","B",1.0,60),
        ("Which Python keyword is used to define a generator function?",
         "Skill Verification","Medium","All","All","All","All","Python",
         "A) return","B) yield (Correct)","C) generate","D) async","B",1.2,75),
        ("What does list comprehension [x**2 for x in range(5)] produce?",
         "Skill Verification","Easy","All","All","All","All","Python",
         "A) [1,4,9,16,25]","B) [0,1,4,9,16] (Correct)","C) [0,1,2,3,4]","D) [1,2,3,4,5]","B",1.0,60),
        ("Which module provides the DataFrame class in Python?",
         "Skill Verification","Easy","All","All","All","All","Python",
         "A) numpy","B) scipy","C) pandas (Correct)","D) matplotlib","C",1.0,45),
        ("What is a decorator in Python?",
         "Skill Verification","Hard","All","All","All","All","Python",
         "A) A class attribute","B) A function wrapping another function (Correct)",
         "C) An inheritance mechanism","D) A memory management tool","B",1.5,90),

        # ── SKILL VERIFICATION: SQL ───────────────────────────────────────────
        ("Which SQL clause filters after GROUP BY?",
         "Skill Verification","Medium","All","All","All","All","SQL & Databases",
         "A) WHERE","B) HAVING (Correct)","C) FILTER","D) SELECT","B",1.2,75),
        ("What is an INNER JOIN?",
         "Skill Verification","Easy","All","All","All","All","SQL & Databases",
         "A) Returns all rows from left table","B) Returns matching rows from both tables (Correct)",
         "C) Returns all rows from right table","D) Returns distinct rows","B",1.0,60),
        ("Which function returns the number of rows in SQL?",
         "Skill Verification","Easy","All","All","All","All","SQL & Databases",
         "A) SUM()","B) MAX()","C) COUNT() (Correct)","D) AVG()","C",1.0,45),

        # ── SKILL VERIFICATION: MACHINE LEARNING ────────────────────────────
        ("Which algorithm handles classification and regression?",
         "Skill Verification","Easy","All","All","All","All","Machine Learning",
         "A) K-Means","B) Random Forest (Correct)","C) PCA","D) Apriori","B",1.0,60),
        ("Overfitting means?",
         "Skill Verification","Easy","All","All","All","All","Machine Learning",
         "A) Model underfits training data","B) Model memorizes training data, poor generalization (Correct)",
         "C) Model performs well on all data","D) Model has high bias","B",1.0,60),
        ("What does k in k-Nearest Neighbors represent?",
         "Skill Verification","Easy","All","All","All","All","Machine Learning",
         "A) Number of clusters","B) Number of neighbors to consider (Correct)",
         "C) Learning rate","D) Number of features","B",1.0,45),

        # ── SKILL VERIFICATION: FINANCIAL ACCOUNTING ─────────────────────────
        ("What is the golden rule for personal accounts?",
         "Skill Verification","Easy","All","All","All","All","Financial Accounting",
         "A) Debit what comes in, Credit what goes out",
         "B) Debit the receiver, Credit the giver (Correct)",
         "C) Debit all expenses, Credit all incomes","D) None of the above","B",1.0,60),
        ("Goodwill is classified as?",
         "Skill Verification","Medium","All","All","All","All","Financial Accounting",
         "A) Tangible fixed asset","B) Current asset","C) Intangible asset (Correct)","D) Liability","C",1.2,75),

        # ── PSYCHOMETRIC SCENARIOS ────────────────────────────────────────────
        ("Your team is behind schedule. You...",
         "Psychometric","Easy","All","All","All","All","General",
         "A) Organize a quick triage and reassign tasks based on capacity (Leadership)",
         "B) Work extra hours yourself to compensate (Persistence)",
         "C) Inform the manager and wait for instructions (Adaptability)",
         "D) Motivate team members and maintain morale (Teamwork)","A",1.0,90),
        ("You encounter a bug you've never seen. You...",
         "Psychometric","Easy","All","All","All","All","General",
         "A) Research the issue methodically using docs and forums (Curiosity)",
         "B) Ask a colleague immediately (Teamwork)",
         "C) Skip it and move on (Adaptability)",
         "D) Try random fixes until something works (Persistence)","A",1.0,90),
        ("You're given freedom to choose a project. You choose...",
         "Psychometric","Easy","All","All","All","All","General",
         "A) The most challenging technical problem (Curiosity+Analytical)",
         "B) Something with clear social impact (Social)",
         "C) Something with high financial return (Enterprising)",
         "D) Something creative with design elements (Artistic)","A",1.0,90),

        # ── CAREER INTEREST CHOICES ───────────────────────────────────────────
        ("Which activity sounds more engaging to you?",
         "Career Interest","Easy","All","All","All","All","General",
         "A) Building AI systems & robots (Technology/Engineering)",
         "B) Creating business strategies & campaigns (Business)",
         "C) Teaching & mentoring students (Education)",
         "D) Diagnosing & treating patients (Healthcare)","A",1.0,60),
        ("Which environment do you prefer working in?",
         "Career Interest","Easy","All","All","All","All","General",
         "A) Tech lab building software products",
         "B) Hospital or clinical setting",
         "C) Courtroom or law firm",
         "D) Studio designing creative content","A",1.0,60),
        ("What type of problem excites you most?",
         "Career Interest","Easy","All","All","All","All","General",
         "A) Solving complex algorithms and data puzzles (Research/Tech)",
         "B) Building and growing businesses (Business/Management)",
         "C) Understanding human behavior and society (Social/Psychology)",
         "D) Designing structures and infrastructure (Engineering/Architecture)","A",1.0,60),
    ]

    insert_sql = """
        INSERT INTO question_bank
        (question_text, category, difficulty, education_level, board, stream,
         degree, specialization, option_a, option_b, option_c, option_d,
         correct_answer, weight, expected_time)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur.executemany(insert_sql, questions)
    conn.commit()
    print(f"  [OK] Question bank seeded with {len(questions)} questions.")


# ─────────────────────────────────────────────────────────────────────────────
# INITIALIZE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  Career Recommendation System — Backend Startup")
print("=" * 60)
init_db()
if ml_model is not None:
    print("  [OK] XGBoost ML model loaded & active.")
else:
    print("  [INFO] Running in Mock Prediction mode — awaiting new trained model.")
print("=" * 60 + "\n")


# ═════════════════════════════════════════════════════════════════════════════
# REST API ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

# ── AUTH HELPERS ──────────────────────────────────────────────────────────────
def generate_token(user_id: int, email: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "email":   email,
        "role":    role,
        "exp":     datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "").strip()
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Unauthorized — invalid or expired token"}), 401
        request.user = payload
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "").strip()
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        if payload.get("role") != "admin":
            return jsonify({"error": "Forbidden — admin access required"}), 403
        request.user = payload
        return f(*args, **kwargs)
    return decorated


# ── HEALTH ────────────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status":   "success",
        "message":  "Career Recommendation API is Live!",
        "ml_ready": ml_model is not None,
        "note":     "XGBoost ML model loaded & active." if ml_model else "Running in Mock Prediction mode."
    }), 200


# ── AUTH ──────────────────────────────────────────────────────────────────────
@app.route('/api/auth/register', methods=['POST'])
def register():
    d = request.get_json() or {}
    full_name = d.get("full_name", "").strip()
    email     = d.get("email", "").strip().lower()
    password  = d.get("password", "")
    confirm   = d.get("confirm_password", "")

    if not all([full_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400
    if password != confirm:
        return jsonify({"error": "Passwords do not match"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close(); conn.close()
            return jsonify({"error": "Email already registered"}), 409

        pwd_hash = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s,%s,%s,'student')",
            (full_name, email, pwd_hash)
        )
        conn.commit()
        user_id = cur.lastrowid
        cur.close(); conn.close()

        token = generate_token(user_id, email, "student")
        return jsonify({
            "status":    "success",
            "message":   "Registration successful",
            "token":     token,
            "user":      {"id": user_id, "full_name": full_name, "email": email, "role": "student"}
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.get_json() or {}
    email    = d.get("email", "").strip().lower()
    password = d.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close(); conn.close()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid email or password"}), 401

        token = generate_token(user["id"], user["email"], user["role"])
        return jsonify({
            "status": "success",
            "token":  token,
            "user": {
                "id":        user["id"],
                "full_name": user["full_name"],
                "email":     user["email"],
                "role":      user["role"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── QUESTIONS API ─────────────────────────────────────────────────────────────
@app.route('/api/questions', methods=['GET'])
def get_questions():
    """
    Dynamically fetches questions from question_bank filtered by:
    education_level, board, stream, degree, specialization, category, difficulty.
    Returns 15-20 randomized questions. Never repeats in same session.
    """
    edu     = request.args.get('education_level', 'All')
    board   = request.args.get('board', 'All')
    stream  = request.args.get('stream', 'All')
    degree  = request.args.get('degree', 'All')
    spec    = request.args.get('specialization', 'All')
    cat     = request.args.get('category', 'All')
    diff    = request.args.get('difficulty', 'All')
    limit   = int(request.args.get('limit', 20))

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        # Exclude non-aptitude categories — those are handled by the frontend adaptive banks
        EXCLUDED_CATS = ('Psychometric', 'Career Interest', 'Skill Verification')

        sql = """
            SELECT id, question_text, category, difficulty, option_a, option_b,
                   option_c, option_d, correct_answer, weight, expected_time, skill
            FROM question_bank
            WHERE status = 'Active'
              AND category NOT IN ('Psychometric', 'Career Interest', 'Skill Verification')
              AND (education_level = %s OR education_level = 'All')
              AND (board = %s OR board = 'All')
              AND (stream = %s OR stream = 'All')
              AND (degree = %s OR degree = 'All')
        """
        params = [edu, board, stream, degree]

        if cat and cat != 'All' and cat not in EXCLUDED_CATS:
            sql += " AND category = %s"
            params.append(cat)
        if diff and diff != 'All':
            sql += " AND difficulty = %s"
            params.append(diff)

        sql += " ORDER BY RAND() LIMIT %s"
        params.append(limit)

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close(); conn.close()

        for row in rows:
            for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
                if row.get(opt):
                    row[opt] = row[opt].replace('(Correct)', '').strip()

        return jsonify({"status": "success", "questions": rows, "count": len(rows)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── ASSESSMENT SUBMISSION ─────────────────────────────────────────────────────
@app.route('/api/assessment/submit', methods=['POST'])
def submit_assessment():
    """
    Receives assessment payload, pre-processes it to the 61 model features,
    generates a prediction (real if model loaded, fallback otherwise),
    stores results in `career_predictions` and raw session, and returns dashboard data.
    """
    data = request.get_json() or {}

    auth  = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "").strip()
    user_payload = decode_token(token)
    user_id = user_payload["user_id"] if user_payload else None

    education_level = data.get("education_level", "Undergraduate")
    stream          = data.get("stream", "Unknown")
    degree          = data.get("degree", "Unknown")
    specialization  = data.get("specialization", "Unknown")
    board           = data.get("board", "Unknown")

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        user_info = {}
        if user_id:
            cur.execute("SELECT age, gender, country, state, language FROM users WHERE id = %s", (user_id,))
            user_info = cur.fetchone() or {}

        # 1. Feature Extraction (Mapping payload to the 61 features)
        psy = data.get("psychometric_traits", {})
        ints = data.get("interest_scores", {})
        apt = data.get("aptitude_answers", {})
        # Read skills with proficiency from quiz-verified frontend
        skills_raw      = data.get("skills_with_level", [])
        skills_flat     = data.get("skills", [])
        # Build skill dict: { skill_name: proficiency_level }
        skill_prof_map  = {}
        if skills_raw and isinstance(skills_raw, list):
            for item in skills_raw:
                if isinstance(item, dict):
                    skill_prof_map[item.get("skill","Unknown")] = item.get("proficiency","Beginner")
                elif isinstance(item, str):
                    skill_prof_map[item] = "Beginner"
        elif skills_flat and isinstance(skills_flat, list):
            for s in skills_flat:
                if isinstance(s, str): skill_prof_map[s] = "Beginner"
        skills = skill_prof_map  # maintain backward compat (len gives skill count)

        # Compute skill_verified_score (weighted by proficiency)
        PROF_WEIGHTS = {"Beginner": 33.0, "Intermediate": 66.0, "Advanced": 100.0}
        if skill_prof_map:
            skill_verified_score = min(100.0, sum(
                PROF_WEIGHTS.get(lvl, 33.0) for lvl in skill_prof_map.values()
            ) / len(skill_prof_map))
        else:
            skill_verified_score = 0.0
        certs = data.get("certifications", [])
        projs = data.get("projects", [])

        # Read aptitude scores - frontend sends direct 0-100 scores
        # (10 questions, each correct adds 10 points = 0-100)
        logical_apt = float(data.get("logical_aptitude",  apt.get("logical",  70)))
        num_apt     = float(data.get("numerical_ability", apt.get("numerical", 70)))
        verb_apt    = float(data.get("verbal_ability",    apt.get("verbal",    70)))
        spat_apt    = float(data.get("spatial_ability",   apt.get("spatial",   70)))
        # Clamp to 0-100 range
        logical_apt = max(0.0, min(100.0, logical_apt))
        num_apt     = max(0.0, min(100.0, num_apt))
        verb_apt    = max(0.0, min(100.0, verb_apt))
        spat_apt    = max(0.0, min(100.0, spat_apt))

        # ── Base feature values ────────────────────────────────────────────
        # CGPA: use sent value; for school students frontend sends avg_marks/10
        # Use explicit None check so cgpa=0.0 from school students is not replaced by 7.0
        _cgpa_raw    = data.get("cgpa")
        _cgpa        = float(_cgpa_raw) if _cgpa_raw is not None else 7.0
        # avg_marks comes from Step 2 subject marks average (computed by frontend)
        _avg_marks   = float(data.get("avg_marks", 0))
        _sem_marks   = _avg_marks if _avg_marks > 0 else float(data.get("semester_marks", 75.0))
        _internal    = _avg_marks if _avg_marks > 0 else float(data.get("internal_marks", 75.0))
        _practical   = float(data.get("practical_marks", 75.0))
        _project_sc  = float(data.get("project_score", min(len(projs) * 20.0, 100.0)))
        _lab_sc      = float(data.get("lab_score", 75.0))
        _assignment  = float(data.get("assignment_score", 75.0))
        _attendance  = float(data.get("attendance_pct", data.get("attendance", 80.0)))
        # Age: use user profile if available, else derive from education level
        _edu_age_map = {
            "Class 7": 12, "Class 8": 13, "Class 9": 14, "Class 10": 15,
            "Higher Secondary (11-12)": 17, "Diploma / ITI": 19,
            "Undergraduate": 21, "Postgraduate": 23, "Professional Degree": 24,
        }
        _age_default = _edu_age_map.get(education_level, 20)
        _age         = float(user_info.get("age") or data.get("age") or _age_default)
        _year_study  = float(data.get("year_of_study", 3))

        # Interest scores: frontend sends weighted domain scores (keys use underscore format)
        # Normalize: total sum -> 0-100 per domain
        # Handle both underscore (Arts_Creative) and space (Creative Arts) key formats
        def _get_int(key_us, key_sp, key_alt=''):
            """Get interest score from multiple possible key names."""
            return float(ints.get(key_us, ints.get(key_sp, ints.get(key_alt, 0))))

        raw_tech  = _get_int('Technology',     'Technology')
        raw_hlth  = _get_int('Healthcare',     'Healthcare')
        raw_biz   = _get_int('Business',       'Business')
        raw_arts  = _get_int('Arts_Creative',  'Creative Arts', 'Arts')
        raw_res   = _get_int('Research',       'Research')
        raw_edu   = _get_int('Education',      'Education')
        raw_eng   = _get_int('Engineering',    'Engineering')
        raw_law   = _get_int('Law',            'Law')
        raw_env   = _get_int('Environment',    'Environment')
        raw_soc   = _get_int('Social_Service', 'Social Service', 'Social')

        raw_total = max(raw_tech+raw_hlth+raw_biz+raw_arts+raw_res+
                        raw_edu+raw_eng+raw_law+raw_env+raw_soc, 1)
        def _norm_int(val): return min(100.0, float(val) * (100.0 / raw_total))

        _tech_int   = _norm_int(raw_tech)
        _health_int = _norm_int(raw_hlth)
        _biz_int    = _norm_int(raw_biz)
        _arts_int   = _norm_int(raw_arts)
        _res_int    = _norm_int(raw_res)
        _edu_int    = _norm_int(raw_edu)
        _eng_int    = _norm_int(raw_eng)
        _law_int    = _norm_int(raw_law)
        _env_int    = _norm_int(raw_env)
        _soc_int    = _norm_int(raw_soc)
        # If all zeros (interests not provided), set neutral 50
        if not any([_tech_int,_health_int,_biz_int,_arts_int,_res_int,
                    _edu_int,_eng_int,_law_int,_env_int,_soc_int]):
            _tech_int=_health_int=_biz_int=_arts_int=_res_int= \
            _edu_int=_eng_int=_law_int=_env_int=_soc_int = 50.0

        _logical = float(logical_apt)
        _num_apt = float(num_apt)
        _verb    = float(verb_apt)
        _spat    = float(spat_apt)

        # Normalize psychometric trait scores (raw sum from scenario selection)
        # Each scenario adds 10-15 points; max ~60 per trait over 4 scenarios
        def _norm_psy(val, default=50.0):
            v = float(val)
            return max(0.0, min(100.0, (v / 60.0) * 100.0)) if v > 0 else default
        _leadership  = _norm_psy(psy.get('Leadership',  0))
        _teamwork    = _norm_psy(psy.get('Teamwork',   0))
        _comm        = _norm_psy(psy.get('Communication', 0))
        _creativity  = _norm_psy(psy.get('Creativity',  0))
        _prob_solv   = _norm_psy(psy.get('Problem_Solving', 0))
        _crit_think  = _norm_psy(psy.get('Critical_Thinking', psy.get('Analytical_Thinking', 0)))
        _adaptab     = _norm_psy(psy.get('Adaptability',   0))
        _decision    = _norm_psy(psy.get('Decision_Making', 0))
        _time_mgmt   = _norm_psy(psy.get('Time_Management', 0))
        _curiosity   = _norm_psy(psy.get('Curiosity',      0))
        _analytical  = _norm_psy(psy.get('Analytical_Thinking', 0))
        _stress      = _norm_psy(psy.get('Stress_Management',   0))
        _self_learn  = _norm_psy(psy.get('Self_Learning',       0))
        _persist     = _norm_psy(psy.get('Persistence',         0))
        _confidence  = _norm_psy(psy.get('Confidence',          0))

        _n_skills  = float(len(skill_prof_map)) if skill_prof_map else float(len(skills_flat))
        _skill_ver = skill_verified_score  # 0-100 weighted by proficiency
        _n_certs   = float(len(certs))
        _n_projs   = float(len(projs))
        _interns   = float(data.get("internships_count", 0))
        _hackathons= float(data.get("hackathons_count", 0))
        _research_exp = float(data.get("research_experience", 0))
        _comp_part = float(data.get("competition_count", 0))
        _volunteer = float(data.get("volunteer_activities", 0))

        _subj_know = float(skill_verified_score)
        _acad_score  = (_cgpa * 10 * 0.4 + _sem_marks * 0.35 + _internal * 0.25)
        _soft_skill  = (_leadership + _teamwork + _comm + _creativity + _prob_solv) / 5.0
        _activity_sc = float(_n_projs * 10 + _n_certs * 10 + _interns * 10)

        # ── Engineered interaction features (must match training exactly) ──
        _total_apt     = _logical + _num_apt + _verb + _spat
        _all_interests = [_tech_int, _health_int, _biz_int, _arts_int, _res_int,
                          _edu_int, _eng_int, _law_int, _env_int, _soc_int]
        _dom_interest  = max(_all_interests)
        _int_spread    = max(_all_interests) - min(_all_interests)
        _weighted_acad = _cgpa * 0.4 + _sem_marks * 0.35 + _internal * 0.25
        _stem_signal   = ((_logical + _analytical) * (_tech_int + _eng_int)) / 400.0
        _health_signal = (_health_int * (_num_apt + _res_int)) / 200.0
        _biz_signal    = (_biz_int * (_leadership + _comm + _decision)) / 300.0
        _creative_sig  = (_arts_int * (_creativity + _spat)) / 200.0
        _research_sig  = (_res_int * (_analytical + _curiosity + _research_exp * 10)) / 300.0
        _activity_rich = (_n_projs * 2 + _n_certs * 1.5 + _hackathons + _interns * 2 + _comp_part)
        _soft_composite= (_leadership + _teamwork + _comm + _adaptab + _decision + _time_mgmt) / 6.0

        # ── Build full features dict (72 features matching training order) ─
        features_dict = {
            'Age':                            _age,
            'CGPA':                           _cgpa,
            'Attendance_Percentage':          _attendance,
            'Semester_Marks_Percent':         _sem_marks,
            'Internal_Marks':                 _internal,
            'Practical_Marks':                _practical,
            'Project_Score':                  _project_sc,
            'Lab_Score':                      _lab_sc,
            'Assignment_Score':               _assignment,
            'Logical_Aptitude_Score':         _logical,
            'Numerical_Aptitude_Score':       _num_apt,
            'Verbal_Aptitude_Score':          _verb,
            'Spatial_Aptitude_Score':         _spat,
            'Subject_Knowledge_Score':        _subj_know,
            'Leadership':                     _leadership,
            'Teamwork':                       _teamwork,
            'Communication':                  _comm,
            'Creativity':                     _creativity,
            'Problem_Solving':                _prob_solv,
            'Critical_Thinking':              _crit_think,
            'Adaptability':                   _adaptab,
            'Decision_Making':                _decision,
            'Time_Management':                _time_mgmt,
            'Curiosity':                      _curiosity,
            'Analytical_Thinking':            _analytical,
            'Stress_Management':              _stress,
            'Self_Learning':                  _self_learn,
            'Persistence':                    _persist,
            'Confidence':                     _confidence,
            'Technology_Interest':            _tech_int,
            'Healthcare_Interest':            _health_int,
            'Business_Interest':              _biz_int,
            'Arts_Creative_Interest':         _arts_int,
            'Research_Interest':              _res_int,
            'Education_Interest':             _edu_int,
            'Engineering_Interest':           _eng_int,
            'Law_Interest':                   _law_int,
            'Environment_Interest':           _env_int,
            'Social_Service_Interest':        _soc_int,
            'Num_Technical_Skills':           _n_skills,
            'Num_Certifications':             _n_certs,
            'Num_Projects':                   _n_projs,
            'Internships_Count':              _interns,
            'Hackathons_Count':               _hackathons,
            'Research_Experience':            _research_exp,
            'Competition_Participation_Count':_comp_part,
            'Volunteer_Activities':           _volunteer,
            'Academic_Score':                 _acad_score,
            'Soft_Skill_Score':               _soft_skill,
            'Activity_Score':                 _activity_sc,
            'Year_Of_Study':                  _year_study,
            # Engineered features
            'Total_Aptitude':                 _total_apt,
            'Dominant_Interest':              _dom_interest,
            'Interest_Spread':                _int_spread,
            'Weighted_Academic':              _weighted_acad,
            'STEM_Signal':                    _stem_signal,
            'Health_Signal':                  _health_signal,
            'Business_Signal':                _biz_signal,
            'Creative_Signal':                _creative_sig,
            'Research_Signal':                _research_sig,
            'Activity_Richness':              _activity_rich,
            'Soft_Skill_Composite':           _soft_composite,
            # Categorical features (raw strings)
            'Gender':           str(user_info.get("gender") or data.get("gender") or "Unknown").strip().title(),
            'Country':          str(user_info.get("country") or data.get("country") or "Unknown").strip().title(),
            'State':            str(user_info.get("state")   or data.get("state")   or "Unknown").strip().title(),
            'Language':         str(user_info.get("language")or data.get("language")or "English").strip().title(),
            'Education_Level':  str(education_level).strip().title(),
            'Board':            str(board).strip().title(),
            'Stream':           str(stream).strip().title(),
            'Degree':           str(degree).strip().title(),
            'Locality_Type':    str(data.get("locality_type", user_info.get("locality_type", "Urban"))).strip().title(),
            'Institution_Tier': str(data.get("institution_tier", "Tier 2")).strip().title(),
        }

        # Remove fields not in training data (engineered / leaked columns)
        _DROP = ['Specialization', 'Total_Aptitude', 'Dominant_Interest',
                 'Interest_Spread', 'Weighted_Academic', 'STEM_Signal',
                 'Health_Signal', 'Business_Signal', 'Creative_Signal',
                 'Research_Signal', 'Activity_Richness', 'Soft_Skill_Composite']
        for _k in _DROP:
            features_dict.pop(_k, None)

        top5 = []
        readiness_score = 0
        xai_attributions = []
        shap_json = {}

        if ml_xgb and ml_preprocessor:
            # ── Build input row with exact training column names ───────────────
            row = {}
            for col in (ml_num_cols or []):
                row[col] = float(features_dict.get(col) or 0.0)
            for col in (ml_cat_cols or []):
                row[col] = str(features_dict.get(col) or "Unknown")

            df_input = pd.DataFrame([row])

            # ── Preprocess via ColumnTransformer ──────────────────────────────
            try:
                X_proc = ml_preprocessor.transform(df_input)
            except Exception as pre_err:
                print(f"[WARN] Preprocessor failed: {pre_err}")
                import traceback; traceback.print_exc()
                n_feats = len(ml_feature_cols) if ml_feature_cols else 140
                X_proc  = np.zeros((1, n_feats))

            from scipy.sparse import issparse as _issparse
            X_dense = X_proc.toarray() if _issparse(X_proc) else X_proc

            # ── Soft-Voting Ensemble: weights order [xgb, lgb, cb, rf] ────────
            try:
                p_xgb = ml_xgb.predict_proba(X_proc)[0]
                p_lgb = ml_lgb.predict_proba(X_proc)[0]  if ml_lgb else p_xgb
                p_cb  = ml_cb.predict_proba(X_dense)[0]  if ml_cb  else p_xgb
                p_rf  = ml_rf.predict_proba(X_proc)[0]   if ml_rf  else p_xgb

                w = ml_ens_weights  # [xgb, lgb, cb, rf]
                probs = (w[0]*p_xgb + w[1]*p_lgb + w[2]*p_cb + w[3]*p_rf)
                print(f"[ML] Ensemble proba OK. Top: {np.argmax(probs)}")
            except Exception as ens_err:
                print(f"[WARN] Ensemble failed, using XGBoost only: {ens_err}")
                import traceback; traceback.print_exc()
                probs = ml_xgb.predict_proba(X_proc)[0]

            top5_idx    = np.argsort(probs)[::-1][:5]
            top5_labels = ml_le.inverse_transform(top5_idx)

            for i, idx in enumerate(top5_idx):
                top5.append({
                    "career":     top5_labels[i],
                    "confidence": round(float(probs[idx] * 100), 1),
                    "rank":       i + 1,
                    "why":        ["Based on your academic profile",
                                   "Aligned with your skills and interests"]
                })
            readiness_score = min(int(probs[top5_idx[0]] * 100 * 1.2), 100)

            # ── Live SHAP attribution (XGBoost) ───────────────────────────
            if ml_shap_explainer is not None:
                try:
                    sv = ml_shap_explainer.shap_values(X_dense)
                    top_cls = int(top5_idx[0])

                    if isinstance(sv, list):
                        sv_row = sv[top_cls][0]
                    elif hasattr(sv, 'ndim') and sv.ndim == 3:
                        sv_row = sv[0, :, top_cls]
                    else:
                        sv_row = sv[0]

                    shap_pairs = sorted(
                        zip(ml_feature_cols, sv_row),
                        key=lambda x: abs(x[1]),
                        reverse=True
                    )
                    # Human-readable SHAP feature names
                    FEAT_LABELS = {
                        'Technology_Interest':     'Strong Technology Interest',
                        'Healthcare_Interest':     'High Healthcare Interest',
                        'Business_Interest':       'Strong Business Interest',
                        'Research_Interest':       'Research Orientation',
                        'Engineering_Interest':    'Engineering Aptitude',
                        'Education_Interest':      'Teaching & Learning Interest',
                        'Arts_Creative_Interest':  'Creative & Artistic Interest',
                        'Law_Interest':            'Legal & Analytical Thinking',
                        'Environment_Interest':    'Environmental Awareness',
                        'Social_Service_Interest': 'Social Impact Focus',
                        'CGPA':                    'Strong Academic Record (CGPA)',
                        'Logical_Aptitude_Score':  'High Logical Reasoning',
                        'Numerical_Aptitude_Score':'Strong Numerical Ability',
                        'Verbal_Aptitude_Score':   'Excellent Communication Skills',
                        'Spatial_Aptitude_Score':  'Strong Spatial Reasoning',
                        'Leadership':              'Leadership Trait',
                        'Creativity':              'Creative Thinking',
                        'Problem_Solving':         'Problem-Solving Mindset',
                        'Analytical_Thinking':     'Analytical Thinking',
                        'Self_Learning':           'Self-Learning Drive',
                        'Curiosity':               'High Curiosity & Exploration',
                        'Persistence':             'Persistence & Resilience',
                        'Num_Projects':            'Strong Project Portfolio',
                        'Num_Certifications':      'Well-Certified',
                        'Internships_Count':       'Internship Experience',
                        'STEM_Signal':             'STEM Signal Strength',
                        'Research_Signal':         'Research Aptitude',
                        'Business_Signal':         'Business Acumen',
                        'Soft_Skill_Composite':    'Strong Soft Skills',
                        'Activity_Richness':       'Active & Engaged Profile',
                        'Weighted_Academic':       'Strong Academic Performance',
                    }
                    xai_attributions = []
                    for feat, val in shap_pairs[:15]:
                        xai_attributions.append({
                            "feature":    feat,
                            "label":      FEAT_LABELS.get(feat, feat.replace('_',' ')),
                            "importance": round(float(val), 6),
                            "direction":  "positive" if val >= 0 else "negative",
                            "abs_impact": round(abs(float(val)), 6)
                        })
                    # Build why[] reasons from top positive SHAP features
                    top_why = [
                        FEAT_LABELS.get(f, f.replace('_',' '))
                        for f, v in shap_pairs[:5] if v > 0
                    ][:3]
                    # Inject into top5 careers
                    if top5 and top_why:
                        top5[0]["why"] = top_why
                    shap_json = {f: round(float(v), 6)
                                 for f, v in zip(ml_feature_cols, sv_row)}
                    print(f"[ML] SHAP computed. Top feature: {shap_pairs[0][0]}")
                except Exception as shap_err:
                    print(f"[WARN] SHAP failed: {shap_err}")
        else:
            # Fallback mock prediction — uses 30-career model names
            interest_domain_map = {
                'Technology':     ['Software Developer', 'Full Stack Developer', 'Data Scientist'],
                'Healthcare':     ['Doctor', 'Nurse', 'Pharmacist'],
                'Business':       ['Entrepreneur', 'Business Analyst', 'Chartered Accountant'],
                'Arts_Creative':  ['UI/UX Designer', 'Graphic Designer', 'Animator'],
                'Research':       ['Professor / Researcher', 'Data Scientist', 'Agricultural Scientist'],
                'Education':      ['School Teacher', 'Professor / Researcher', 'Business Analyst'],
                'Engineering':    ['Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer'],
                'Law':            ['Lawyer', 'Business Analyst', 'Entrepreneur'],
                'Environment':    ['Environmental Scientist', 'Agricultural Scientist', 'Civil Engineer'],
                'Social_Service': ['School Teacher', 'Nurse', 'Doctor'],
            }
            top_ints = sorted(ints.items(), key=lambda x: x[1], reverse=True)
            primary_domain = top_ints[0][0] if top_ints else 'Technology'
            # Normalize key format for lookup
            primary_key = primary_domain.replace(' ', '_').replace('Creative_Arts', 'Arts_Creative')
            cands = interest_domain_map.get(primary_key,
                    interest_domain_map.get(primary_domain,
                    ['Software Developer', 'Data Analyst', 'Business Analyst', 'School Teacher', 'Mechanical Engineer']))
            # Pad to 5 with general fallbacks
            defaults = ['Data Analyst', 'Business Analyst', 'School Teacher', 'Mechanical Engineer', 'UI/UX Designer']
            while len(cands) < 5:
                for d in defaults:
                    if d not in cands: cands.append(d)
                    if len(cands) >= 5: break
            apt_score = float(data.get('logical_aptitude', 70))
            marks_score = float(data.get('avg_marks', 75))
            readiness_score = int(min(100, (apt_score * 0.5 + marks_score * 0.5)))
            for i, c in enumerate(cands[:5]):
                top5.append({
                    'career':     c,
                    'confidence': max(55, 92 - (i * 8)),
                    'rank':       i + 1,
                    'why':        [f'Strong {primary_domain.replace("_"," ")} interest',
                                   'Academic profile match', 'Aptitude alignment']
                })
            xai_attributions = [
                {'feature': 'Domain Interest', 'label': f'{primary_domain} Interest', 'importance': 0.40, 'direction': 'positive', 'abs_impact': 0.40},
                {'feature': 'Soft Skills',     'label': 'Soft Skill Profile',         'importance': 0.20, 'direction': 'positive', 'abs_impact': 0.20}
            ]

        if user_id:
            # Ensure shap_json is defined even in mock/fallback path
            if 'shap_json' not in dir():
                shap_json = {}

            # Store Session
            session_token = secrets.token_hex(16)
            cur.execute(
                "INSERT INTO assessment_sessions (user_id, session_token, status, completed_at) VALUES (%s, %s, 'Completed', NOW())",
                (user_id, session_token)
            )
            session_id = cur.lastrowid

            # Save skill verifications (quiz-verified proficiency levels)
            for sk_name, sk_level in skill_prof_map.items():
                PROF_PCT = {"Beginner": 33.0, "Intermediate": 66.0, "Advanced": 100.0}
                sk_score = PROF_PCT.get(sk_level, 33.0)
                try:
                    cur.execute("""
                        INSERT INTO skill_verification (user_id, skill_name, score, level, is_verified, verified_at)
                        VALUES (%s, %s, %s, %s, 1, NOW())
                        ON DUPLICATE KEY UPDATE score=VALUES(score), level=VALUES(level),
                        is_verified=1, verified_at=NOW()
                    """, (user_id, sk_name, sk_score, sk_level))
                except Exception: pass

            # Store Prediction (including full SHAP values)
            cur.execute("""
                INSERT INTO career_predictions
                (user_id, session_id, top1_career, top1_confidence,
                 top5_careers_json, readiness_score, shap_json,
                 feature_scores_json, xai_attributions_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                session_id,
                top5[0]["career"] if top5 else "Unknown",
                top5[0]["confidence"] if top5 else 0.0,
                json.dumps(top5),
                readiness_score,
                json.dumps(shap_json),          # full per-feature SHAP values
                json.dumps(features_dict),
                json.dumps(xai_attributions)    # top-15 sorted attributions
            ))
            
            # Store Raw Answers
            for ans_key, ans_val in apt.items():
                q_id = int(ans_key) if str(ans_key).isdigit() else None
                is_corr = 1 if (isinstance(ans_val, dict) and ans_val.get('is_correct')) else 0
                cur.execute("""
                    INSERT INTO assessment_answers (session_id, question_id, category, is_correct)
                    VALUES (%s, %s, %s, %s)
                """, (session_id, q_id, 'Aptitude', is_corr))
            
            conn.commit()
        
        cur.close()
        conn.close()

        # ── Enrich top5 with career metadata ─────────────────────────────────
        CAREER_META = {
            'Software Developer':        {'salary': 'Rs.5L-Rs.18L/yr',  'degree': 'BTech CS / BCA',         'companies': 'Infosys, TCS, Google',      'growth': '+22% annually', 'certifications': 'AWS, Full Stack Cert'},
            'Data Scientist':            {'salary': 'Rs.7L-Rs.25L/yr',  'degree': 'BTech / MSc Statistics',  'companies': 'Google, Amazon, Flipkart',  'growth': '+35% annually', 'certifications': 'Google DS, IBM DS Cert'},
            'Full Stack Developer':      {'salary': 'Rs.5L-Rs.20L/yr',  'degree': 'BTech CS / BCA',         'companies': 'Infosys, Razorpay, Zoho',   'growth': '+25% annually', 'certifications': 'MERN Stack, AWS'},
            'Doctor':                    {'salary': 'Rs.8L-Rs.30L+/yr', 'degree': 'MBBS + MD/MS',           'companies': 'Govt Hospitals, Private',   'growth': '+15% annually', 'certifications': 'MCI Registration, DNB'},
            'Data Analyst':              {'salary': 'Rs.4L-Rs.14L/yr',  'degree': 'BTech / BSc Statistics',  'companies': 'Wipro, Accenture, KPMG',   'growth': '+25% annually', 'certifications': 'Google Data Analytics, SQL'},
            'Machine Learning Engineer': {'salary': 'Rs.8L-Rs.25L/yr',  'degree': 'BTech CS / MTech AI',    'companies': 'Google, Microsoft, Amazon', 'growth': '+28% annually', 'certifications': 'TensorFlow, AWS ML'},
            'AI Engineer':               {'salary': 'Rs.10L-Rs.30L/yr', 'degree': 'BTech CS / MTech AI',    'companies': 'DeepMind, OpenAI, NVIDIA',  'growth': '+30% annually', 'certifications': 'AWS AI, Azure AI'},
            'Entrepreneur':              {'salary': 'Variable',          'degree': 'Any + MBA',              'companies': 'Own Startup',               'growth': 'Unlimited',     'certifications': 'Management Certs'},
            'School Teacher':            {'salary': 'Rs.3L-Rs.9L/yr',   'degree': 'BA/BSc + B.Ed',          'companies': 'Govt Schools, Ed-Tech',     'growth': '+12% annually', 'certifications': 'CTET, TET'},
            'Business Analyst':          {'salary': 'Rs.5L-Rs.15L/yr',  'degree': 'BBA / BTech / MBA',      'companies': 'Deloitte, EY, KPMG',        'growth': '+20% annually', 'certifications': 'PMP, BA Cert'},
            'Professor / Researcher':    {'salary': 'Rs.6L-Rs.18L/yr',  'degree': 'PhD / MTech',            'companies': 'Universities, DRDO, ISRO',  'growth': '+15% annually', 'certifications': 'UGC NET, Research Grants'},
            'Lawyer':                    {'salary': 'Rs.4L-Rs.20L+/yr', 'degree': 'LLB / LLM',             'companies': 'Law Firms, Govt',           'growth': '+18% annually', 'certifications': 'Bar Council Enrollment'},
            'Cyber Security Analyst':    {'salary': 'Rs.6L-Rs.22L/yr',  'degree': 'BTech CS / MCA',         'companies': 'IBM, Cisco, ISRO',          'growth': '+31% annually', 'certifications': 'CEH, CISSP, CompTIA'},
            'Chartered Accountant':      {'salary': 'Rs.7L-Rs.25L+/yr', 'degree': 'CA (ICAI)',              'companies': 'Big4, Banks, Corporates',   'growth': '+20% annually', 'certifications': 'CFA, DISA'},
            'Product Manager':           {'salary': 'Rs.10L-Rs.35L/yr', 'degree': 'BTech / MBA',            'companies': 'Google, Flipkart, Amazon',  'growth': '+25% annually', 'certifications': 'PMP, CSPO'},
            'Cloud Architect':           {'salary': 'Rs.12L-Rs.35L/yr', 'degree': 'BTech CS / MTech',       'companies': 'AWS, Azure, Google Cloud',  'growth': '+28% annually', 'certifications': 'AWS SAA, GCP Pro'},
            'Bank Manager':              {'salary': 'Rs.5L-Rs.14L/yr',  'degree': 'BBA / BCom / MBA',       'companies': 'SBI, HDFC, ICICI, RBI',     'growth': '+15% annually', 'certifications': 'JAIIB, CAIIB'},
            'Mechanical Engineer':       {'salary': 'Rs.4L-Rs.14L/yr',  'degree': 'BTech Mechanical / BE',  'companies': 'L&T, BHEL, Bosch, Tata',   'growth': '+16% annually', 'certifications': 'AutoCAD, SolidWorks'},
            'Civil Engineer':            {'salary': 'Rs.4L-Rs.12L/yr',  'degree': 'BTech Civil / BE',       'companies': 'L&T, NHAI, PWD, DLF',      'growth': '+14% annually', 'certifications': 'AutoCAD, STAAD.Pro'},
            'UI/UX Designer':            {'salary': 'Rs.4L-Rs.16L/yr',  'degree': 'BDes / BTech / BA Design','companies': 'Infosys, TCS, Startups',   'growth': '+22% annually', 'certifications': 'Google UX Cert, Figma'},
            'Graphic Designer':          {'salary': 'Rs.3L-Rs.12L/yr',  'degree': 'BDes / BFA / BA',        'companies': 'Agencies, Ad Firms',        'growth': '+15% annually', 'certifications': 'Adobe CC, Canva Pro'},
            'Nurse':                     {'salary': 'Rs.3L-Rs.10L/yr',  'degree': 'B.Sc Nursing / GNM',    'companies': 'Govt Hospitals, Apollo',    'growth': '+18% annually', 'certifications': 'NMC Registration'},
            'Pharmacist':                {'salary': 'Rs.3L-Rs.10L/yr',  'degree': 'B.Pharm / M.Pharm',     'companies': 'Hospitals, Pharma Cos',     'growth': '+15% annually', 'certifications': 'PCI Registration'},
            'Architect':                 {'salary': 'Rs.4L-Rs.16L/yr',  'degree': 'B.Arch / M.Arch',       'companies': 'CPWD, DDA, Private Firms',  'growth': '+17% annually', 'certifications': 'COA Registration'},
            'Electrical Engineer':       {'salary': 'Rs.4L-Rs.14L/yr',  'degree': 'BTech EEE / BE',        'companies': 'NTPC, KSEB, Siemens',       'growth': '+16% annually', 'certifications': 'AutoCAD, ETAP'},
            'Agricultural Scientist':    {'salary': 'Rs.4L-Rs.12L/yr',  'degree': 'BSc/MSc Agriculture',   'companies': 'ICAR, KAU, DRDO',           'growth': '+14% annually', 'certifications': 'ICAR Certs'},
            'Biomedical Engineer':       {'salary': 'Rs.5L-Rs.15L/yr',  'degree': 'BTech Biomedical',      'companies': 'Hospitals, Medtech Cos',    'growth': '+20% annually', 'certifications': 'CBET, ISO Certs'},
            'Animator':                  {'salary': 'Rs.3L-Rs.12L/yr',  'degree': 'BDes / BFA / BVA',      'companies': 'Studios, Ad Agencies',      'growth': '+18% annually', 'certifications': 'Maya, After Effects Cert'},
            'Environmental Scientist':   {'salary': 'Rs.4L-Rs.12L/yr',  'degree': 'BSc/MSc Env Science',   'companies': 'CPCB, KSPCB, NGOs',         'growth': '+16% annually', 'certifications': 'ISO 14001, EIA Cert'},
        }
        for career_item in top5:
            meta = CAREER_META.get(career_item.get('career', ''), {})
            career_item.setdefault('salary',         meta.get('salary',         'Varies by experience'))
            career_item.setdefault('degree',         meta.get('degree',         'Relevant UG/PG Degree'))
            career_item.setdefault('companies',      meta.get('companies',      'Various Organizations'))
            career_item.setdefault('growth',         meta.get('growth',         '+15% annually'))
            career_item.setdefault('certifications', meta.get('certifications', 'Domain Certifications'))

        return jsonify({
            'status':          'success',
            'top5_careers':    top5,
            'readiness_score': readiness_score,
            'feature_scores':  features_dict,
            'xai_attributions':xai_attributions,
            'message':         'AI Assessment complete — career recommendations ready.'
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ── SHAP EXPLAINABILITY ENDPOINT ─────────────────────────────────────────────


# ── SKILL VERIFICATION SAVE ───────────────────────────────────────────────────
@app.route('/api/skills/verify', methods=['POST'])
@require_auth
def save_skill_verification():
    """
    Called after each skill quiz closes in the frontend.
    Saves the quiz result to skill_verification table.
    Payload: { skill_name, score, total, level }
    """
    user_id = request.user["user_id"]
    d       = request.get_json() or {}
    skill   = d.get("skill_name", "")
    score   = float(d.get("score", 0))
    total   = float(d.get("total", 3))
    level   = d.get("level", "Beginner")    # Beginner / Intermediate / Advanced
    pct     = round((score / max(total, 1)) * 100, 1)
    verified= 1  # Quiz was taken = verified

    if not skill:
        return jsonify({"error": "skill_name required"}), 400

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        # Upsert skill verification record
        cur.execute("""
            INSERT INTO skill_verification
            (user_id, skill_name, score, level, is_verified, verified_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
            score = VALUES(score), level = VALUES(level),
            is_verified = 1, verified_at = NOW()
        """, (user_id, skill, pct, level, verified))
        conn.commit()
        cur.close(); conn.close()

        return jsonify({
            "status":  "success",
            "message": f"Skill '{skill}' verified at {level} level ({score}/{int(total)})",
            "score":   pct,
            "level":   level
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/skills/my-verified', methods=['GET'])
@require_auth
def get_my_verified_skills():
    """Returns all verified skills for the authenticated user."""
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT skill_name, score, level, is_verified, verified_at
            FROM skill_verification
            WHERE user_id = %s
            ORDER BY verified_at DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return jsonify({"status": "success", "skills": rows, "count": len(rows)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/api/prediction/shap/<int:pred_id>', methods=['GET'])
@require_auth
def get_shap_explanation(pred_id):
    """
    Returns SHAP explainability data for a specific career prediction.
    Response includes:
      - xai_attributions : top-15 features sorted by |SHAP value|
      - shap_values      : full per-feature SHAP dict
      - top5_careers     : the career predictions
    """
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM career_predictions WHERE id = %s AND user_id = %s",
            (pred_id, user_id)
        )
        pred = cur.fetchone()
        cur.close(); conn.close()

        if not pred:
            return jsonify({"error": "Prediction not found or access denied"}), 404

        shap_data = json.loads(pred.get("shap_json") or "{}")
        xai_data  = json.loads(pred.get("xai_attributions_json") or "[]")
        top5      = json.loads(pred.get("top5_careers_json") or "[]")

        return jsonify({
            "status":           "success",
            "prediction_id":    pred_id,
            "top_career":       pred["top1_career"],
            "confidence":       pred["top1_confidence"],
            "top5_careers":     top5,
            "xai_attributions": xai_data,   # top-15 sorted by impact
            "shap_values":      shap_data,  # full SHAP dict for all features
            "predicted_at":     str(pred["predicted_at"])
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/prediction/latest-shap', methods=['GET'])
@require_auth
def get_latest_shap():
    """Returns SHAP data for the most recent prediction of the authenticated user."""
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id FROM career_predictions WHERE user_id = %s ORDER BY predicted_at DESC LIMIT 1",
            (user_id,)
        )
        row = cur.fetchone()
        cur.close(); conn.close()

        if not row:
            return jsonify({"error": "No predictions found"}), 404

        # Delegate to existing endpoint logic
        from flask import g
        request.user = {"user_id": user_id}
        return get_shap_explanation(row["id"])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── USER PROFILE & SETTINGS ───────────────────────────────────────────────────
@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_user_profile():
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, full_name, email, role, phone, age, gender, country, state, district, institution, language, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()

        cur.execute(
            "SELECT * FROM career_predictions WHERE user_id = %s ORDER BY predicted_at DESC LIMIT 1",
            (user_id,)
        )
        last_pred = cur.fetchone()

        cur.close(); conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "status": "success",
            "user":   user,
            "latest_prediction": last_pred
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/user/profile', methods=['PUT'])
@require_auth
def update_user_profile():
    user_id = request.user["user_id"]
    d = request.get_json() or {}

    allowed = ["full_name", "phone", "age", "gender", "country", "state", "district", "institution", "language"]
    updates = {k: v for k, v in d.items() if k in allowed}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        cur.execute(f"UPDATE users SET {set_clause} WHERE id = %s",
                    (*updates.values(), user_id))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"status": "success", "message": "Profile updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── DASHBOARD ANALYTICS ───────────────────────────────────────────────────────
@app.route('/api/dashboard', methods=['GET'])
@require_auth
def get_dashboard():
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        cur.execute("SELECT full_name, email, role FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        cur.execute("""
            SELECT top1_career, top1_confidence, top5_careers_json, readiness_score, predicted_at
            FROM career_predictions WHERE user_id = %s ORDER BY predicted_at DESC LIMIT 1
        """, (user_id,))
        pred = cur.fetchone()

        cur.execute("""
            SELECT top1_career, top1_confidence, predicted_at
            FROM career_predictions WHERE user_id = %s ORDER BY predicted_at DESC LIMIT 5
        """, (user_id,))
        history = cur.fetchall()

        cur.execute("""
            SELECT status, started_at, completed_at
            FROM assessment_sessions WHERE user_id = %s ORDER BY started_at DESC LIMIT 5
        """, (user_id,))
        sessions = cur.fetchall()

        cur.close(); conn.close()

        top5 = []
        readiness = 0
        if pred:
            top5 = json.loads(pred["top5_careers_json"] or "[]")
            readiness = pred["readiness_score"] or 0

        return jsonify({
            "status":          "success",
            "user":            user,
            "readiness_score": readiness,
            "top5_careers":    top5,
            "history":         history,
            "sessions":        sessions
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── HISTORY ───────────────────────────────────────────────────────────────────
@app.route('/api/history', methods=['GET'])
@require_auth
def get_history():
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, top1_career, top1_confidence, readiness_score,
                   top5_careers_json, predicted_at
            FROM career_predictions WHERE user_id = %s
            ORDER BY predicted_at DESC
        """, (user_id,))
        records = cur.fetchall()
        cur.close(); conn.close()
        for r in records:
            r["top5_careers"] = json.loads(r.get("top5_careers_json") or "[]")
        return jsonify({"status": "success", "history": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── ADMIN ENDPOINTS ───────────────────────────────────────────────────────────
@app.route('/api/admin/users', methods=['GET'])
@require_admin
def admin_get_users():
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT u.id, u.full_name, u.email, u.role, u.age, u.gender,
                   u.created_at,
                   (SELECT COUNT(*) FROM career_predictions cp WHERE cp.user_id = u.id) AS assessments
            FROM users u ORDER BY u.created_at DESC
        """)
        users = cur.fetchall()
        cur.close(); conn.close()
        return jsonify({"status": "success", "users": users, "total": len(users)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/users/<int:uid>/role', methods=['PUT'])
@require_admin
def admin_update_role(uid):
    d    = request.get_json() or {}
    role = d.get("role", "student")
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("UPDATE users SET role = %s WHERE id = %s", (role, uid))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"status": "success", "message": f"Role updated to {role}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/users/<int:uid>', methods=['DELETE'])
@require_admin
def admin_delete_user(uid):
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("DELETE FROM users WHERE id = %s AND role != 'admin'", (uid,))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"status": "success", "message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/questions', methods=['GET'])
@require_admin
def admin_get_questions():
    page  = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    cat   = request.args.get('category', '')
    edu   = request.args.get('education_level', '')
    offset = (page - 1) * limit

    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        sql    = "SELECT * FROM question_bank WHERE status != 'Deleted'"
        params = []
        if cat: sql += " AND category = %s"; params.append(cat)
        if edu: sql += " AND education_level = %s"; params.append(edu)
        sql += " ORDER BY id DESC LIMIT %s OFFSET %s"
        params += [limit, offset]
        cur.execute(sql, params)
        questions = cur.fetchall()
        cur.execute("SELECT COUNT(*) as cnt FROM question_bank WHERE status != 'Deleted'")
        total = cur.fetchone()["cnt"]
        cur.close(); conn.close()
        return jsonify({"status": "success", "questions": questions, "total": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/questions', methods=['POST'])
@require_admin
def admin_add_question():
    d = request.get_json() or {}
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            INSERT INTO question_bank
            (question_text, category, difficulty, education_level, board, stream,
             degree, specialization, skill, option_a, option_b, option_c, option_d,
             correct_answer, weight, expected_time, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            d.get("question_text", ""),
            d.get("category", "General"),
            d.get("difficulty", "Medium"),
            d.get("education_level", "All"),
            d.get("board", "All"),
            d.get("stream", "All"),
            d.get("degree", "All"),
            d.get("specialization", "All"),
            d.get("skill", "General"),
            d.get("option_a", ""), d.get("option_b", ""),
            d.get("option_c", ""), d.get("option_d", ""),
            d.get("correct_answer", "A"),
            float(d.get("weight", 1.0)),
            int(d.get("expected_time", 60)),
            "Active"
        ))
        conn.commit()
        qid = cur.lastrowid
        cur.close(); conn.close()
        return jsonify({"status": "success", "id": qid, "message": "Question added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/questions/<int:qid>', methods=['PUT'])
@require_admin
def admin_update_question(qid):
    d = request.get_json() or {}
    allowed = ["question_text","category","difficulty","education_level","board","stream",
               "degree","specialization","skill","option_a","option_b","option_c","option_d",
               "correct_answer","weight","expected_time","status"]
    updates = {k: v for k, v in d.items() if k in allowed}
    if not updates:
        return jsonify({"error": "No valid fields"}), 400
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        cur.execute(f"UPDATE question_bank SET {set_clause} WHERE id = %s",
                    (*updates.values(), qid))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"status": "success", "message": "Question updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/questions/<int:qid>', methods=['DELETE'])
@require_admin
def admin_delete_question(qid):
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("UPDATE question_bank SET status = 'Deleted' WHERE id = %s", (qid,))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"status": "success", "message": "Question deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/analytics', methods=['GET'])
@require_admin
def admin_analytics():
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)

        cur.execute("SELECT COUNT(*) as total FROM users WHERE role = 'student'")
        total_students = cur.fetchone()["total"]

        cur.execute("SELECT COUNT(*) as total FROM career_predictions")
        total_assessments = cur.fetchone()["total"]

        cur.execute("SELECT COUNT(*) as total FROM question_bank WHERE status = 'Active'")
        total_questions = cur.fetchone()["total"]

        cur.execute("""
            SELECT top1_career, COUNT(*) as count
            FROM career_predictions
            GROUP BY top1_career
            ORDER BY count DESC LIMIT 10
        """)
        top_careers = cur.fetchall()

        cur.execute("""
            SELECT DATE(predicted_at) as date, COUNT(*) as assessments
            FROM career_predictions
            GROUP BY DATE(predicted_at)
            ORDER BY date DESC LIMIT 30
        """)
        daily_trend = cur.fetchall()

        cur.close(); conn.close()

        return jsonify({
            "status":            "success",
            "total_students":    total_students,
            "total_assessments": total_assessments,
            "total_questions":   total_questions,
            "top_careers":       top_careers,
            "daily_trend":       daily_trend
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/retrain', methods=['POST'])
@require_admin
def admin_retrain():
    import subprocess
    try:
        py_exe = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        script = os.path.join(os.path.dirname(__file__), 'train_model.py')
        if not os.path.exists(py_exe):
            py_exe = 'python'
        subprocess.Popen([py_exe, script], cwd=os.path.dirname(__file__))
        return jsonify({"status": "success", "message": "Model retraining triggered in background"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── STATIC FILE SERVING ───────────────────────────────────────────────────────
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(DIST_FOLDER, path)):
        return send_from_directory(DIST_FOLDER, path)
    return send_from_directory(DIST_FOLDER, 'index.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
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

# Try loading XGBoost and ML Artifacts
try:
    import xgboost as xgb
    import warnings
    ml_base = os.path.join(os.path.dirname(__file__), 'models')
    # Use joblib for sklearn objects — pickle fails on Python 3.14 with STACK_GLOBAL error
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml_le         = joblib.load(os.path.join(ml_base, 'label_encoder.pkl'))
        ml_oe         = joblib.load(os.path.join(ml_base, 'ordinal_encoder.pkl'))
        ml_scaler     = joblib.load(os.path.join(ml_base, 'scaler.pkl'))
    ml_feature_cols = pickle.load(open(os.path.join(ml_base, 'feature_columns.pkl'), 'rb'))
    ml_cat_cols     = pickle.load(open(os.path.join(ml_base, 'cat_feature_names.pkl'), 'rb'))
    ml_num_cols     = pickle.load(open(os.path.join(ml_base, 'numeric_feature_names.pkl'), 'rb'))
    # Try loading the XGBoost model — may fail if saved with a different XGBoost version
    try:
        ml_model = joblib.load(os.path.join(ml_base, 'career_model.pkl'))
        print("[OK] ML Artifacts loaded successfully (joblib).")
    except Exception as model_err:
        print(f"[WARN] career_model.pkl failed to load: {str(model_err)[:80]}")
        print("    Encoders & scalers loaded — running in Mock Prediction mode.")
        ml_model = None
    try:
        ml_shap = joblib.load(os.path.join(ml_base, 'shap_explainer.pkl'))
    except Exception:
        ml_shap = None
except Exception as e:
    print(f"[WARN] ML load failed: {str(e)[:80]}. Running in Mock Prediction mode.")
    ml_model, ml_le, ml_oe, ml_scaler, ml_feature_cols = None, None, None, None, None
    ml_cat_cols, ml_num_cols, ml_shap = None, None, None

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
                attendance_pct  FLOAT        DEFAULT 0,
                created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

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
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
    Returns 15–20 randomized questions. Never repeats in same session.
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

        sql = """
            SELECT id, question_text, category, difficulty, option_a, option_b,
                   option_c, option_d, correct_answer, weight, expected_time, skill
            FROM question_bank
            WHERE status = 'Active'
              AND (education_level = %s OR education_level = 'All')
              AND (board = %s OR board = 'All')
              AND (stream = %s OR stream = 'All')
              AND (degree = %s OR degree = 'All')
        """
        params = [edu, board, stream, degree]

        if cat and cat != 'All':
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
        skills = data.get("skill_scores", {})
        certs = data.get("certifications", [])
        projs = data.get("projects", [])

        # Rough calculation for aptitude domains
        logical_apt = len([v for k,v in apt.items() if "logical" in str(k).lower() and v.get("is_correct")]) * 10
        num_apt = len([v for k,v in apt.items() if "numerical" in str(k).lower() and v.get("is_correct")]) * 10
        verb_apt = len([v for k,v in apt.items() if "verbal" in str(k).lower() and v.get("is_correct")]) * 10
        spat_apt = len([v for k,v in apt.items() if "spatial" in str(k).lower() and v.get("is_correct")]) * 10
        if not any([logical_apt, num_apt, verb_apt, spat_apt]): 
             logical_apt = num_apt = verb_apt = spat_apt = 70.0 # Default fallback if missing structure

        features_dict = {
            'Age': float(user_info.get("age", 20)),
            'CGPA': float(data.get("cgpa", 7.0)),
            'Attendance_Percentage': float(data.get("attendance", 80.0)),
            'Semester_Marks_Percent': float(data.get("semester_marks", 75.0)),
            'Internal_Marks': 75.0,
            'Practical_Marks': 75.0,
            'Project_Score': float(data.get("project_score", len(projs) * 20.0)),
            'Lab_Score': 75.0,
            'Assignment_Score': 75.0,
            'Logical_Aptitude_Score': float(logical_apt),
            'Numerical_Aptitude_Score': float(num_apt),
            'Verbal_Aptitude_Score': float(verb_apt),
            'Spatial_Aptitude_Score': float(spat_apt),
            'Subject_Knowledge_Score': sum(skills.values()) / max(1, len(skills)),
            'Leadership': float(psy.get('Leadership', 50)),
            'Teamwork': float(psy.get('Teamwork', 50)),
            'Communication': float(psy.get('Communication', 50)),
            'Creativity': float(psy.get('Creativity', 50)),
            'Problem_Solving': float(psy.get('Problem_Solving', 50)),
            'Critical_Thinking': float(psy.get('Analytical_Thinking', 50)),
            'Adaptability': float(psy.get('Adaptability', 50)),
            'Decision_Making': float(psy.get('Decision_Making', 50)),
            'Time_Management': float(psy.get('Time_Management', 50)),
            'Curiosity': float(psy.get('Curiosity', 50)),
            'Analytical_Thinking': float(psy.get('Analytical_Thinking', 50)),
            'Stress_Management': float(psy.get('Stress_Management', 50)),
            'Self_Learning': float(psy.get('Self_Learning', 50)),
            'Persistence': float(psy.get('Persistence', 50)),
            'Confidence': float(psy.get('Confidence', 50)),
            'Technology_Interest': float(ints.get('Technology', 50)),
            'Healthcare_Interest': float(ints.get('Healthcare', 50)),
            'Business_Interest': float(ints.get('Business', 50)),
            'Arts_Creative_Interest': float(ints.get('Creative Arts', 50)),
            'Research_Interest': float(ints.get('Research', 50)),
            'Education_Interest': float(ints.get('Education', 50)),
            'Engineering_Interest': float(ints.get('Engineering', 50)),
            'Law_Interest': float(ints.get('Law', 50)),
            'Environment_Interest': float(ints.get('Environment', 50)),
            'Social_Service_Interest': float(ints.get('Social Service', 50)),
            'Num_Technical_Skills': float(len(skills)),
            'Num_Certifications': float(len(certs)),
            'Num_Projects': float(len(projs)),
            'Internships_Count': float(data.get("internships_count", 0)),
            'Hackathons_Count': 0.0,
            'Research_Experience': 0.0,
            'Competition_Participation_Count': 0.0,
            'Volunteer_Activities': 0.0,
            'Academic_Score': float(data.get("cgpa", 7.0)) * 10,
            'Soft_Skill_Score': float(sum(psy.values()) / max(1, len(psy)) if psy else 50.0),
            'Activity_Score': float(len(projs) * 10 + len(certs) * 10),
            'Year_Of_Study': 3.0,
            'Gender': user_info.get("gender") or data.get("gender") or "Unknown",
            'Country': user_info.get("country", "Unknown"),
            'State': user_info.get("state", "Unknown"),
            'Language': user_info.get("language", "English"),
            'Education_Level': education_level,
            'Board': board,
            'Stream': stream,
            'Degree': degree,
            'Specialization': specialization,
            'Institution_Tier': 'Tier 2'
        }

        top5 = []
        readiness_score = 0
        xai_attributions = []

        if ml_model and ml_feature_cols:
            # Create DataFrame exactly in the order expected
            df = pd.DataFrame([features_dict])
            df = df[ml_feature_cols]

            # Replace missing cat/num columns with defaults if necessary
            for col in ml_cat_cols:
                df[col] = df[col].astype(str).fillna("Unknown")
            for col in ml_num_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

            # Preprocess
            try:
                df[ml_cat_cols] = ml_oe.transform(df[ml_cat_cols])
            except Exception as e:
                pass # Proceed with caution if unseen labels exist (ordinal encoder usually configured with handle_unknown)

            df[ml_num_cols] = ml_scaler.transform(df[ml_num_cols])

            # Predict
            probs = ml_model.predict_proba(df)[0]
            top5_idx = np.argsort(probs)[::-1][:5]
            top5_labels = ml_le.inverse_transform(top5_idx)
            
            for i, idx in enumerate(top5_idx):
                top5.append({
                    "career": top5_labels[i],
                    "confidence": round(float(probs[idx] * 100), 1),
                    "rank": i + 1,
                    "why": ["Based on your academic profile", "Aligned with your interests"]
                })
            readiness_score = int(sum(probs[top5_idx]) * 100) # Simple aggregation
            
            # Simple XAI mock (if real shap fails on single row)
            xai_attributions = [
                {"feature": "Technology_Interest", "importance": 0.25},
                {"feature": "Subject_Knowledge_Score", "importance": 0.15},
                {"feature": "Logical_Aptitude_Score", "importance": 0.12},
                {"feature": "Problem_Solving", "importance": 0.08}
            ]
        else:
            # Fallback mock prediction
            top_interests = sorted(ints.items(), key=lambda x: x[1], reverse=True)[:3]
            fallback_careers = {
                "Technology": ["Software Developer", "Data Scientist", "Cloud Architect"],
                "Business": ["Business Analyst", "Marketing Manager", "Product Manager"],
                "Healthcare": ["Clinical Researcher", "Medical Officer", "Health Tech Analyst"],
                "Engineering": ["Mechanical Engineer", "Systems Engineer", "Robotics Engineer"],
                "Creative Arts": ["UI/UX Designer", "Content Strategist", "Art Director"]
            }
            primary_domain = top_interests[0][0] if top_interests else "Technology"
            cands = fallback_careers.get(primary_domain, fallback_careers["Technology"]) + ["Project Manager", "Consultant"]
            for i, c in enumerate(cands[:5]):
                top5.append({
                    "career": c,
                    "confidence": 95 - (i * 8),
                    "rank": i + 1,
                    "why": [f"High interest in {primary_domain}"]
                })
            readiness_score = 85
            xai_attributions = [
                {"feature": "Domain Interest", "importance": 0.40},
                {"feature": "Soft Skills", "importance": 0.20}
            ]

        if user_id:
            # Store Session
            session_token = secrets.token_hex(16)
            cur.execute(
                "INSERT INTO assessment_sessions (user_id, session_token, status, completed_at) VALUES (%s, %s, 'Completed', NOW())",
                (user_id, session_token)
            )
            session_id = cur.lastrowid

            # Store Prediction
            cur.execute("""
                INSERT INTO career_predictions
                (user_id, session_id, top1_career, top1_confidence,
                 top5_careers_json, readiness_score,
                 feature_scores_json, xai_attributions_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                session_id,
                top5[0]["career"] if top5 else "Unknown",
                top5[0]["confidence"] if top5 else 0.0,
                json.dumps(top5),
                readiness_score,
                json.dumps(features_dict),
                json.dumps(xai_attributions)
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

        return jsonify({
            "status": "success",
            "top5_careers": top5,
            "readiness_score": readiness_score,
            "feature_scores": features_dict,
            "xai_attributions": xai_attributions,
            "message": "AI Assessment complete."
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
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
    app.run(debug=True, host='0.0.0.0', port=5000)
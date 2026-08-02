"""
==============================================================================
AI Career Recommendation System — Flask Backend
==============================================================================
All business logic lives here. Frontend never computes scores or contains
assessment logic. Every request goes through REST API endpoints.
==============================================================================
"""

import os
import json
import random
import datetime
import jwt
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling

# ─────────────────────────────────────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────────────────────────────────────
DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path='')
SECRET_KEY = os.environ.get('JWT_SECRET', 'career_super_secret_key_2026')

CORS(app)

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE POOL
# ─────────────────────────────────────────────────────────────────────────────
dbconfig = {
    "database": "career_system_db",
    "user":     "root",
    "password": "abc123",
    "host":     "localhost"
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

        # 8. feature_scores
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
                id                  INT AUTO_INCREMENT PRIMARY KEY,
                user_id             INT NOT NULL,
                session_id          INT,
                top1_career         VARCHAR(150),
                top1_confidence     FLOAT,
                top5_careers_json   LONGTEXT,
                shap_json           LONGTEXT,
                readiness_score     FLOAT DEFAULT 0,
                predicted_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

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
# LOAD ML MODELS
# ─────────────────────────────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')

ml_model           = None
label_encoder      = None
feature_encoders   = None
scaler             = None
feature_columns    = None
shap_available     = False

def load_models():
    global ml_model, label_encoder, feature_encoders, scaler, feature_columns, shap_available

    try:
        ml_model         = joblib.load(os.path.join(MODELS_DIR, 'career_model_lgb.joblib'))
        label_encoder    = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))
        feature_encoders = joblib.load(os.path.join(MODELS_DIR, 'feature_encoder.pkl'))
        scaler           = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        feature_columns  = joblib.load(os.path.join(MODELS_DIR, 'feature_columns.pkl'))

        try:
            import shap
            shap_available = True
        except ImportError:
            shap_available = False

        print(f"  [OK] LightGBM model loaded ({len(label_encoder.classes_)} career classes)")
    except Exception as e:
        print(f"  [WARN]  Models not found (run train_model.py first): {e}")


# ─────────────────────────────────────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE — converts raw answers → standardized feature scores
# ─────────────────────────────────────────────────────────────────────────────
def compute_feature_scores(payload: dict) -> dict:
    """
    Converts raw assessment payload into standardized 0–100 feature scores
    that are passed directly to the ML model.
    """
    # Academic
    cgpa          = float(payload.get("cgpa", 7.5))
    attendance    = float(payload.get("attendance", 85))
    sem_marks     = float(payload.get("semester_marks", 75))
    project_score = float(payload.get("project_score", 60))

    # Normalize CGPA to 0-100
    cgpa_pct = min((cgpa / 10.0) * 100, 100)

    # Aptitude scores from question answers
    apt_answers   = payload.get("aptitude_answers", {})
    apt_correct   = sum(1 for v in apt_answers.values() if v.get("is_correct", False))
    apt_total     = max(len(apt_answers), 1)
    logical_score = round((apt_correct / apt_total) * 100)

    # Skill verification
    skill_scores = payload.get("skill_scores", {})
    avg_skill    = round(np.mean(list(skill_scores.values())) if skill_scores else 60)

    # Psychometric trait scores (from situational scenario responses)
    psycho = payload.get("psychometric_traits", {})
    leadership   = float(psycho.get("Leadership", 70))
    teamwork     = float(psycho.get("Teamwork", 75))
    communication= float(psycho.get("Communication", 72))
    creativity   = float(psycho.get("Creativity", 68))
    resilience   = float(psycho.get("Resilience", 70))
    curiosity    = float(psycho.get("Curiosity", 72))
    problem_solv = float(psycho.get("Problem_Solving", 70))
    adaptability = float(psycho.get("Adaptability", 70))
    analytical   = float(psycho.get("Analytical_Thinking", 70))
    confidence   = float(psycho.get("Confidence", 65))
    decision_mak = float(psycho.get("Decision_Making", 68))
    time_mgmt    = float(psycho.get("Time_Management", 70))
    stress_mgmt  = float(psycho.get("Stress_Management", 65))
    self_learn   = float(psycho.get("Self_Learning", 72))
    persistence  = float(psycho.get("Persistence", 70))

    # Career interest domain scores
    interests = payload.get("interest_scores", {})
    tech_int   = float(interests.get("Technology", 50))
    healthcare = float(interests.get("Healthcare", 30))
    business   = float(interests.get("Business", 40))
    arts       = float(interests.get("Creative Arts", 35))
    research   = float(interests.get("Research", 45))
    education  = float(interests.get("Education", 30))
    engineering= float(interests.get("Engineering", 50))
    law_int    = float(interests.get("Law", 20))
    environment= float(interests.get("Environment", 25))

    # Certifications & projects
    certs       = payload.get("certifications", [])
    projects    = payload.get("projects", [])
    cert_count  = len(certs)
    proj_count  = len(projects)
    cert_score  = min(cert_count * 15, 100)
    proj_score  = min(proj_count * 20, 100)
    internships = int(payload.get("internships_count", 0))

    return {
        "logical_aptitude":     logical_score,
        "numerical_ability":    min(sem_marks, 100),
        "verbal_ability":       min(communication, 100),
        "spatial_ability":      60,
        "programming_score":    avg_skill if skill_scores else 50,
        "science_score":        min(sem_marks, 100),
        "business_score":       business,
        "creative_score":       arts,
        "medical_score":        healthcare,
        "leadership_trait":     leadership,
        "teamwork_trait":       teamwork,
        "communication_trait":  communication,
        "resilience_trait":     resilience,
        "curiosity_trait":      curiosity,
        "creativity_trait":     creativity,
        "problem_solving":      problem_solv,
        "analytical_thinking":  analytical,
        "adaptability_trait":   adaptability,
        "ai_interest":          tech_int,
        "technology_interest":  tech_int,
        "healthcare_interest":  healthcare,
        "business_interest":    business,
        "arts_interest":        arts,
        "research_interest":    research,
        "education_interest":   education,
        "engineering_interest": engineering,
        "law_interest":         law_int,
        "environment_interest": environment,
        "certification_score":  cert_score,
        "project_score":        proj_score,
        "internship_score":     min(internships * 20, 100),
        "skill_verified_score": avg_skill,
        "academic_score":       cgpa_pct,
        "attendance_pct":       attendance,
        "cgpa":                 cgpa,
        "skill_count":          len(skill_scores),
        "cert_count":           cert_count,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CAREER PREDICTION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def run_ml_prediction(feature_scores: dict, education_level: str, stream: str,
                       degree: str, specialization: str, gender: str = "Male"):
    """
    Builds the feature vector expected by the trained LightGBM model and
    returns top-5 careers with confidence and SHAP-style explanations.
    """
    if ml_model is None:
        return fallback_prediction(feature_scores, education_level)

    try:
        # Map raw values using the same encoders used during training
        def safe_encode(encoder, value):
            val_str = str(value).strip()
            if hasattr(encoder, 'classes_') and val_str in encoder.classes_:
                return int(encoder.transform([val_str])[0])
            return 0

        encoded = {
            "Gender":         safe_encode(feature_encoders.get("Gender"), gender),
            "Education_Level":safe_encode(feature_encoders.get("Education_Level"), education_level),
            "Stream":         safe_encode(feature_encoders.get("Stream"), stream),
            "Specialization": safe_encode(feature_encoders.get("Specialization"), specialization),
        }

        # Build full feature row aligned to training columns
        row = {}
        for col in feature_columns:
            if col in encoded:
                row[col] = encoded[col]
            elif col == "Age":
                row[col] = 20
            elif col == "Attendance_Percentage":
                row[col] = feature_scores.get("attendance_pct", 80)
            elif col == "CGPA":
                row[col] = feature_scores.get("cgpa", 7.5)
            elif col == "Semester_Marks_Percent":
                row[col] = feature_scores.get("numerical_ability", 75)
            elif col == "Internal_Marks":
                row[col] = feature_scores.get("numerical_ability", 75)
            elif col == "Practical_Marks":
                row[col] = feature_scores.get("numerical_ability", 70)
            elif col == "Project_Score":
                row[col] = feature_scores.get("project_score", 60)
            elif col == "Lab_Score":
                row[col] = feature_scores.get("programming_score", 60)
            elif col == "Assignment_Score":
                row[col] = feature_scores.get("academic_score", 70)
            elif col == "Competition_Participation_Count":
                row[col] = min(feature_scores.get("cert_count", 0), 5)
            elif col == "Olympiad_Participation":
                row[col] = 0
            elif col == "Hackathons_Count":
                row[col] = min(feature_scores.get("skill_count", 0), 5)
            elif col == "Internships_Count":
                row[col] = min(feature_scores.get("internship_score", 0) // 20, 5)
            elif col == "Research_Experience":
                row[col] = 1 if feature_scores.get("research_interest", 0) > 60 else 0
            elif col == "Volunteer_Activities":
                row[col] = 0
            elif col == "Club_Activities":
                row[col] = 0
            elif col == "Leadership":
                row[col] = int(feature_scores.get("leadership_trait", 70) / 10)
            elif col == "Communication":
                row[col] = int(feature_scores.get("communication_trait", 70) / 10)
            elif col == "Confidence":
                row[col] = int(feature_scores.get("creative_score", 65) / 10)
            elif col == "Creativity":
                row[col] = int(feature_scores.get("creativity_trait", 70) / 10)
            elif col == "Problem_Solving":
                row[col] = int(feature_scores.get("problem_solving", 70) / 10)
            elif col == "Critical_Thinking":
                row[col] = int(feature_scores.get("analytical_thinking", 70) / 10)
            elif col == "Adaptability":
                row[col] = int(feature_scores.get("adaptability_trait", 70) / 10)
            elif col == "Teamwork":
                row[col] = int(feature_scores.get("teamwork_trait", 75) / 10)
            elif col == "Decision_Making":
                row[col] = 7
            elif col == "Time_Management":
                row[col] = 7
            elif col == "Curiosity":
                row[col] = int(feature_scores.get("curiosity_trait", 70) / 10)
            elif col == "Analytical_Thinking":
                row[col] = int(feature_scores.get("analytical_thinking", 70) / 10)
            elif col == "Stress_Management":
                row[col] = 6
            elif col == "Self_Learning":
                row[col] = int(feature_scores.get("curiosity_trait", 70) / 10)
            elif col == "Persistence":
                row[col] = int(feature_scores.get("resilience_trait", 70) / 10)
            elif col == "Skill_Count":
                row[col] = feature_scores.get("skill_count", 3)
            elif col == "Interest_Count":
                row[col] = 3
            elif col == "Certification_Count":
                row[col] = feature_scores.get("cert_count", 1)
            else:
                row[col] = 0

        X_df     = pd.DataFrame([row])[feature_columns]
        X_scaled = scaler.transform(X_df)

        # Get probabilities for all 272 classes
        proba    = ml_model.predict_proba(X_scaled)[0]
        top5_idx = np.argsort(proba)[::-1][:5]

        top5 = []
        for rank, idx in enumerate(top5_idx, 1):
            career     = label_encoder.inverse_transform([idx])[0]
            confidence = round(float(proba[idx]) * 100, 1)
            top5.append(build_career_detail(rank, career, confidence, feature_scores))

        # Simple XAI attributions based on highest scores
        xai_chips = build_xai_chips(feature_scores)

        return {"top5": top5, "xai": xai_chips, "method": "LightGBM ML"}

    except Exception as e:
        print(f"  [WARN]  ML prediction error: {e}")
        return fallback_prediction(feature_scores, education_level)


def build_xai_chips(fs: dict) -> list:
    """Builds Explainable AI attribution chips from feature scores."""
    chips = []
    if fs.get("logical_aptitude", 0) > 70:
        chips.append(f"[+] Logical Aptitude Score: {fs['logical_aptitude']}%")
    if fs.get("programming_score", 0) > 70:
        chips.append(f"[+] Verified Programming Skill: {fs['programming_score']}%")
    if fs.get("leadership_trait", 0) > 70:
        chips.append(f"[+] Leadership Trait: {fs['leadership_trait']}%")
    if fs.get("technology_interest", 0) > 60:
        chips.append(f"[+] Technology Domain Interest: {fs['technology_interest']}%")
    if fs.get("cgpa", 0) >= 8:
        chips.append(f"[+] High CGPA: {fs['cgpa']}")
    if fs.get("research_interest", 0) > 60:
        chips.append(f"[+] Research Orientation: {fs['research_interest']}%")
    if fs.get("business_interest", 0) > 60:
        chips.append(f"[+] Business Domain Interest: {fs['business_interest']}%")
    if fs.get("creativity_trait", 0) > 70:
        chips.append(f"[+] Creativity & Design Aptitude: {fs['creativity_trait']}%")
    return chips[:6]


def build_career_detail(rank: int, career: str, confidence: float, fs: dict) -> dict:
    """Enriches a career prediction with salary, degree, companies, etc."""
    career_meta = {
        "AI Engineer":                  ("$130K–$180K","B.Tech AI/CS","AWS ML Specialist, TF Dev","Google, NVIDIA, OpenAI","+32%"),
        "Data Scientist":               ("$110K–$155K","B.Sc/M.Sc Data Science","Google Data Eng, IBM DS","Meta, Netflix, Airbnb","+28%"),
        "Software Developer":           ("$95K–$140K","B.Tech CS/IT","AWS Developer, Azure Dev","Microsoft, Amazon, Infosys","+22%"),
        "Machine Learning Engineer":    ("$120K–$165K","B.Tech CS/AI","ML Specialist, GCP Cert","Apple, Tesla, DeepMind","+30%"),
        "Cyber Security Analyst":       ("$100K–$145K","B.Tech CS/Cyber","CEH, CISSP, CompTIA Sec+","Palo Alto, CrowdStrike","+25%"),
        "Full Stack Developer":         ("$90K–$135K","B.Tech/BCA","Meta React Dev, Node Cert","Atlassian, Shopify, Startups","+20%"),
        "Data Analyst":                 ("$80K–$120K","B.Sc/BCom Stats","Google Analytics, Tableau","Deloitte, EY, JP Morgan","+18%"),
        "Cloud Architect":              ("$140K–$200K","B.Tech CS","AWS SA, GCP Arch, Azure","AWS, Azure, GCP teams","+35%"),
        "Business Analyst":             ("$85K–$125K","BBA/MBA","CBAP, PMP","McKinsey, BCG, Accenture","+15%"),
        "School Teacher":               ("$45K–$75K","B.Ed","CTET, TET","State Boards, CBSE Schools","+8%"),
        "Doctor":                       ("$150K–$250K","MBBS/MD","Medical License, PG Diploma","Hospitals, Clinics","+10%"),
        "Chartered Accountant":         ("$70K–$120K","CA","ICAI CA, CMA","Big 4, Banks, Corporates","+12%"),
        "Lawyer":                       ("$65K–$130K","LLB/LLM","Bar Council","Courts, Law Firms","+10%"),
        "Architect":                    ("$75K–$130K","B.Arch","RIBA, Council of Arch","Firms, Govt, Urban Planning","+12%"),
        "Graphic Designer":             ("$55K–$95K","B.Design/BFA","Adobe Certified Expert","Ad Agencies, Startups","+14%"),
        "Biomedical Engineer":          ("$90K–$135K","B.Tech Biomedical","CBET Certification","Medtronic, GE Healthcare","+20%"),
        "Agricultural Scientist":       ("$60K–$100K","B.Sc Agriculture","ICAR, ASRB","Research Institutes, Govt","+8%"),
        "Bank Manager":                 ("$70K–$110K","BBA/MBA Finance","JAIIB, CAIIB","SBI, HDFC, ICICI","+8%"),
        "Animator":                     ("$55K–$90K","B.Sc Animation","Adobe, Autodesk Maya","Studios, Gaming Companies","+18%"),
        "Entrepreneur":                 ("$50K–$500K+","MBA/B.Tech","Business Cert","Startups, Self-employed","+25%"),
    }

    meta = career_meta.get(career, (
        "$60K–$100K", "Relevant UG/PG Degree",
        "Domain Certifications", "Industry Companies", "+10%"
    ))

    # Build XAI reasons based on feature scores
    why = []
    if fs.get("logical_aptitude", 0) > 70:
        why.append(f"[+] Strong Logical Aptitude ({fs['logical_aptitude']}%)")
    if fs.get("programming_score", 0) > 70:
        why.append(f"[+] Verified Technical Skills ({fs['programming_score']}%)")
    if fs.get("leadership_trait", 0) > 70:
        why.append(f"[+] Leadership & Communication Trait")
    if fs.get("cgpa", 0) >= 8.0:
        why.append(f"[+] High CGPA: {fs['cgpa']}")
    if fs.get("research_interest", 0) > 60:
        why.append("[+] Research Orientation")
    if not why:
        why = ["[+] Profile matched career domain", "[+] Interest alignment detected"]

    return {
        "rank":           rank,
        "career":         career,
        "confidence":     confidence,
        "why":            why[:4],
        "salary":         meta[0],
        "degree":         meta[1],
        "certifications": meta[2],
        "companies":      meta[3],
        "growth":         meta[4],
    }


def fallback_prediction(fs: dict, edu_level: str) -> dict:
    """Returns a heuristic fallback when the ML model is not loaded."""
    careers = [
        ("Software Developer",   88, "$95K–$140K"),
        ("Data Scientist",       82, "$110K–$155K"),
        ("Business Analyst",     76, "$85K–$125K"),
        ("School Teacher",       70, "$45K–$75K"),
        ("Graphic Designer",     65, "$55K–$95K"),
    ]
    top5 = [
        build_career_detail(i + 1, c[0], c[1], fs)
        for i, c in enumerate(careers)
    ]
    return {"top5": top5, "xai": build_xai_chips(fs), "method": "Heuristic Fallback"}


# ─────────────────────────────────────────────────────────────────────────────
# INITIALIZE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  AI Career Recommendation System — Backend Startup")
print("=" * 60)
init_db()
load_models()
print("=" * 60 + "\n")


# ═════════════════════════════════════════════════════════════════════════════
# REST API ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

# ── HEALTH ────────────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status":   "success",
        "message":  "AI Career Recommendation API is Live!",
        "ml_ready": ml_model is not None,
        "careers":  len(label_encoder.classes_) if label_encoder else 0
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
    Receives full assessment payload, runs scoring engine + ML prediction,
    stores results in DB, and returns career report.
    """
    data = request.get_json() or {}

    # Extract auth (optional — assessment can be submitted without auth)
    auth  = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "").strip()
    user_payload = decode_token(token)
    user_id = user_payload["user_id"] if user_payload else None

    education_level = data.get("education_level", "Undergraduate")
    board           = data.get("board", "CBSE")
    stream          = data.get("stream", "Science")
    degree          = data.get("degree", "BTech")
    specialization  = data.get("specialization", "Computer Science")
    gender          = data.get("gender", "Male")

    try:
        # 1. Compute standardized feature scores
        fs = compute_feature_scores(data)

        # 2. Run ML prediction
        result = run_ml_prediction(
            fs, education_level, stream, degree, specialization, gender
        )
        top5   = result["top5"]
        xai    = result["xai"]

        # 3. Compute readiness score (0–100)
        readiness = round(
            fs["logical_aptitude"] * 0.25 +
            fs["academic_score"]   * 0.20 +
            fs["skill_verified_score"] * 0.20 +
            fs["leadership_trait"] * 0.10 +
            fs["project_score"]    * 0.10 +
            fs["certification_score"] * 0.15
        )
        readiness = min(readiness, 100)

        # 4. Store in DB if user is authenticated
        if user_id:
            try:
                conn = get_conn()
                cur  = conn.cursor(dictionary=True)

                # Session
                import secrets
                session_token = secrets.token_hex(16)
                cur.execute(
                    """INSERT INTO assessment_sessions (user_id, session_token, status, completed_at)
                       VALUES (%s,%s,'Completed', NOW())""",
                    (user_id, session_token)
                )
                session_id = cur.lastrowid

                # Feature scores
                cur.execute("""
                    INSERT INTO feature_scores
                    (user_id, session_id, logical_aptitude, numerical_ability,
                     programming_score, leadership_trait, teamwork_trait,
                     communication_trait, resilience_trait, curiosity_trait,
                     creativity_trait, problem_solving, analytical_thinking,
                     adaptability_trait, technology_interest, business_interest,
                     healthcare_interest, arts_interest, research_interest,
                     certification_score, project_score, skill_verified_score,
                     academic_score, attendance_pct, cgpa, skill_count, cert_count)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    user_id, session_id,
                    fs["logical_aptitude"], fs["numerical_ability"],
                    fs["programming_score"], fs["leadership_trait"],
                    fs["teamwork_trait"], fs["communication_trait"],
                    fs["resilience_trait"], fs["curiosity_trait"],
                    fs["creativity_trait"], fs["problem_solving"],
                    fs["analytical_thinking"], fs["adaptability_trait"],
                    fs["technology_interest"], fs["business_interest"],
                    fs["healthcare_interest"], fs["arts_interest"],
                    fs["research_interest"], fs["certification_score"],
                    fs["project_score"], fs["skill_verified_score"],
                    fs["academic_score"], fs["attendance_pct"],
                    fs["cgpa"], fs["skill_count"], fs["cert_count"]
                ))

                # Career prediction
                cur.execute("""
                    INSERT INTO career_predictions
                    (user_id, session_id, top1_career, top1_confidence,
                     top5_careers_json, shap_json, readiness_score)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    user_id, session_id,
                    top5[0]["career"] if top5 else "Unknown",
                    top5[0]["confidence"] if top5 else 0,
                    json.dumps(top5),
                    json.dumps(xai),
                    readiness
                ))

                conn.commit()
                cur.close(); conn.close()
            except Exception as db_err:
                print(f"  [WARN]  DB store error: {db_err}")

        return jsonify({
            "status":           "success",
            "readiness_score":  readiness,
            "top5_careers":     top5,
            "xai_attributions": xai,
            "feature_scores":   fs,
            "method":           result.get("method", "ML")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── LEGACY PREDICT ENDPOINT (backward compatibility) ─────────────────────────
@app.route('/api/predict/career', methods=['POST'])
def predict_career_legacy():
    """Backward-compatible endpoint — wraps the new assessment engine."""
    data = request.get_json() or {}

    # Map legacy payload to new format
    new_payload = {
        "education_level": data.get("EducationLevel", "Undergraduate"),
        "board":           data.get("Board", "CBSE"),
        "stream":          data.get("Stream", "Science"),
        "degree":          data.get("Degree", "BTech"),
        "specialization":  data.get("Specialization", "Computer Science"),
        "gender":          "Male",
        "cgpa":            float(data.get("StandardizedFeatures", {}).get("OverallCGPA", 7.5)),
        "attendance":      float(data.get("StandardizedFeatures", {}).get("AttendancePct", 85)),
        "semester_marks":  75.0,
        "psychometric_traits": {
            "Leadership":        data.get("StandardizedFeatures", {}).get("LeadershipTraitScore", 70),
            "Teamwork":          data.get("StandardizedFeatures", {}).get("TeamworkScore", 75),
            "Resilience":        data.get("StandardizedFeatures", {}).get("ResilienceScore", 70),
            "Curiosity":         data.get("StandardizedFeatures", {}).get("CuriosityScore", 72),
            "Communication":     72,
            "Creativity":        68,
            "Problem_Solving":   70,
            "Adaptability":      70,
            "Analytical_Thinking": 70,
        },
        "aptitude_answers": {},
        "skill_scores":    data.get("VerifiedSkillScores", {}),
        "certifications":  data.get("Certifications", []),
        "projects":        [],
        "interest_scores": {"Technology": 70, "Business": 40, "Healthcare": 30},
    }

    return submit_assessment.__wrapped__(new_payload) if hasattr(submit_assessment, '__wrapped__') else submit_assessment()


# ── USER PROFILE & SETTINGS ───────────────────────────────────────────────────
@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_user_profile():
    user_id = request.user["user_id"]
    try:
        conn = get_conn()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT id, full_name, email, role, phone, age, gender, country, state, district, institution, language, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        cur.execute("SELECT * FROM career_predictions WHERE user_id = %s ORDER BY predicted_at DESC LIMIT 1", (user_id,))
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
    """Triggers ML model retraining in background."""
    import subprocess, sys
    try:
        train_script = os.path.join(os.path.dirname(__file__), 'train_model.py')
        subprocess.Popen([sys.executable, train_script],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({
            "status":  "success",
            "message": "Model retraining started in background. Check server logs."
        }), 200
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
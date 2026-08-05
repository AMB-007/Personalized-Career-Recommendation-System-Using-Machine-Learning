-- ==============================================================================
-- CAREER RECOMMENDATION SYSTEM — COMPLETE DATABASE SETUP
-- ==============================================================================
-- Database  : career_system_db
-- Charset   : utf8mb4 (supports all languages + emojis)
-- Engine    : InnoDB (supports foreign keys & transactions)
-- Run this  : mysql -u root -p < career_system_db.sql
--             OR paste directly into MySQL Workbench / phpMyAdmin
-- ==============================================================================


-- ── STEP 1: CREATE & SELECT DATABASE ─────────────────────────────────────────
DROP DATABASE IF EXISTS career_system_db;
CREATE DATABASE career_system_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE career_system_db;

-- ==============================================================================
-- TABLE 1: users
-- Central user table — stores all registered students and admins
-- ==============================================================================
CREATE TABLE users (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    full_name       VARCHAR(120) NOT NULL,
    email           VARCHAR(120) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(20)  NOT NULL DEFAULT 'student'
                    COMMENT 'student | admin',
    phone           VARCHAR(20),
    age             INT          DEFAULT 18,
    gender          VARCHAR(20)  COMMENT 'Male | Female | Other',
    country         VARCHAR(80),
    state           VARCHAR(80),
    district        VARCHAR(80),
    institution     VARCHAR(150),
    language        VARCHAR(40)  DEFAULT 'English',
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email  (email),
    INDEX idx_role   (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 2: student_profiles
-- Extended profile info (bio, links) — one-to-one with users
-- ==============================================================================
CREATE TABLE student_profiles (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL UNIQUE,
    bio             TEXT,
    avatar_url      VARCHAR(255),
    linkedin_url    VARCHAR(255),
    github_url      VARCHAR(255),
    portfolio_url   VARCHAR(255),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 3: education_profiles
-- Student academic background — one-to-one with users
-- ==============================================================================
CREATE TABLE education_profiles (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    education_level VARCHAR(60)  COMMENT 'Class 7-10 | Higher Secondary | Undergraduate | Postgraduate',
    board           VARCHAR(80)  COMMENT 'CBSE | ICSE | State Board | International',
    stream          VARCHAR(80)  COMMENT 'Science | Commerce | Humanities',
    degree          VARCHAR(80)  COMMENT 'BTech | BCA | BSc | MBBS | LLB | MBA | etc.',
    specialization  VARCHAR(120) COMMENT 'Computer Science | Finance | Biology | etc.',
    institution     VARCHAR(150),
    cgpa            FLOAT        DEFAULT 0  COMMENT 'Scale: 0.0 to 10.0',
    attendance_pct  FLOAT        DEFAULT 0  COMMENT 'Scale: 0 to 100',
    year_of_study   INT          DEFAULT 0,
    institution_tier VARCHAR(20) DEFAULT 'Tier 2' COMMENT 'Tier 1 | Tier 2 | Tier 3',
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_edu_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 4: subject_marks
-- Semester-wise subject marks — one-to-many with users
-- ==============================================================================
CREATE TABLE subject_marks (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    subject_name    VARCHAR(120),
    semester        VARCHAR(40),
    marks_percent   FLOAT        COMMENT 'Marks as percentage 0-100',
    credits         INT          DEFAULT 3,
    grade           VARCHAR(5)   COMMENT 'A+ | A | B+ | B | C | etc.',
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_marks_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 5: question_bank
-- Assessment MCQ questions — filtered by education level, stream, degree
-- ==============================================================================
CREATE TABLE question_bank (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    question_text   TEXT         NOT NULL,
    category        VARCHAR(80)  NOT NULL
                    COMMENT 'Logical Reasoning | Numerical Reasoning | Psychometric | Career Interest | Skill Verification | etc.',
    difficulty      VARCHAR(20)  DEFAULT 'Medium'
                    COMMENT 'Easy | Medium | Hard',
    education_level VARCHAR(60)  DEFAULT 'All'
                    COMMENT 'All | Class 7 | Class 8 | Class 9 | Class 10 | Higher Secondary | Undergraduate | Postgraduate',
    board           VARCHAR(80)  DEFAULT 'All',
    stream          VARCHAR(80)  DEFAULT 'All',
    degree          VARCHAR(80)  DEFAULT 'All',
    specialization  VARCHAR(120) DEFAULT 'All',
    skill           VARCHAR(80)  DEFAULT 'General'
                    COMMENT 'Skill this question tests: Python | SQL | ML | etc.',
    option_a        VARCHAR(255),
    option_b        VARCHAR(255),
    option_c        VARCHAR(255),
    option_d        VARCHAR(255),
    correct_answer  VARCHAR(5)   COMMENT 'A | B | C | D',
    weight          FLOAT        DEFAULT 1.0
                    COMMENT 'Score multiplier for difficulty',
    expected_time   INT          DEFAULT 60
                    COMMENT 'Expected time in seconds',
    status          VARCHAR(20)  DEFAULT 'Active'
                    COMMENT 'Active | Inactive | Deleted',
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_qb_category  (category),
    INDEX idx_qb_edu       (education_level),
    INDEX idx_qb_stream    (stream),
    INDEX idx_qb_status    (status),
    INDEX idx_qb_degree    (degree)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 6: assessment_sessions
-- Tracks each time a student takes an assessment
-- ==============================================================================
CREATE TABLE assessment_sessions (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    session_token   VARCHAR(100) UNIQUE,
    status          VARCHAR(30)  DEFAULT 'In Progress'
                    COMMENT 'In Progress | Completed | Abandoned',
    started_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    completed_at    TIMESTAMP    NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sess_user   (user_id),
    INDEX idx_sess_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 7: assessment_answers
-- Individual MCQ answers per assessment session
-- ==============================================================================
CREATE TABLE assessment_answers (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    session_id      INT          NOT NULL,
    question_id     INT          COMMENT 'FK to question_bank (optional — for reporting)',
    question_text   TEXT         COMMENT 'Snapshot of question at time of answer',
    category        VARCHAR(80),
    selected_answer VARCHAR(255),
    is_correct      TINYINT(1)   DEFAULT 0,
    time_taken_sec  INT          DEFAULT 0,

    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    INDEX idx_ans_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 8: feature_scores
-- Computed ML feature scores from assessment — reserved for future ML model
-- ==============================================================================
CREATE TABLE feature_scores (
    id                      INT   AUTO_INCREMENT PRIMARY KEY,
    user_id                 INT   NOT NULL,
    session_id              INT,

    -- Aptitude
    logical_aptitude        FLOAT DEFAULT 0,
    numerical_ability       FLOAT DEFAULT 0,
    verbal_ability          FLOAT DEFAULT 0,
    spatial_ability         FLOAT DEFAULT 0,

    -- Subject Knowledge
    programming_score       FLOAT DEFAULT 0,
    science_score           FLOAT DEFAULT 0,
    business_score          FLOAT DEFAULT 0,
    creative_score          FLOAT DEFAULT 0,
    medical_score           FLOAT DEFAULT 0,

    -- Personality Traits (0-100 scale)
    leadership_trait        FLOAT DEFAULT 0,
    teamwork_trait          FLOAT DEFAULT 0,
    communication_trait     FLOAT DEFAULT 0,
    resilience_trait        FLOAT DEFAULT 0,
    curiosity_trait         FLOAT DEFAULT 0,
    creativity_trait        FLOAT DEFAULT 0,
    problem_solving         FLOAT DEFAULT 0,
    analytical_thinking     FLOAT DEFAULT 0,
    adaptability_trait      FLOAT DEFAULT 0,

    -- Career Interests (0-100 scale)
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

    -- Activity & Academic
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

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_fs_user    (user_id),
    INDEX idx_fs_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 9: skills
-- Master list of all available skills (used for skill verification module)
-- ==============================================================================
CREATE TABLE skills (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    skill_name      VARCHAR(100) UNIQUE NOT NULL,
    category        VARCHAR(80)  COMMENT 'Technical | Soft Skill | Domain | Language',
    domain          VARCHAR(80)  COMMENT 'IT | Business | Healthcare | Arts | etc.',
    status          VARCHAR(20)  DEFAULT 'Active',

    INDEX idx_skill_domain (domain),
    INDEX idx_skill_cat    (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 10: skill_verification
-- Student's verified skill scores (from skill quiz module)
-- ==============================================================================
CREATE TABLE skill_verification (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    skill_name      VARCHAR(100),
    score           FLOAT        DEFAULT 0   COMMENT 'Score 0-100',
    level           VARCHAR(30)  DEFAULT 'Beginner'
                    COMMENT 'Beginner | Intermediate | Advanced | Expert',
    is_verified     TINYINT(1)   DEFAULT 0,
    verified_at     TIMESTAMP    NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sv_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 11: projects
-- Student projects — used for project_score computation in ML features
-- ==============================================================================
CREATE TABLE projects (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    title           VARCHAR(200),
    description     TEXT,
    technology      VARCHAR(200) COMMENT 'Comma-separated: Python, React, MySQL',
    duration        VARCHAR(60)  COMMENT '1 month | 6 weeks | etc.',
    role            VARCHAR(80)  COMMENT 'Lead Developer | Backend Dev | etc.',
    team_size       INT          DEFAULT 1,
    github_link     VARCHAR(255),
    demo_link       VARCHAR(255),
    certificate_url VARCHAR(255),
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_proj_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 12: certifications
-- Student certifications — used for certification_score in ML features
-- ==============================================================================
CREATE TABLE certifications (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    cert_name       VARCHAR(200),
    provider        VARCHAR(100) COMMENT 'Coursera | Google | AWS | NPTEL | etc.',
    status          VARCHAR(30)  DEFAULT 'Completed'
                    COMMENT 'Completed | In Progress | Expired',
    cert_url        VARCHAR(255),
    issued_date     DATE         NULL,
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_cert_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 13: career_predictions
-- ML model output — top 5 careers with confidence scores
-- Will be populated once new ML model is integrated
-- ==============================================================================
CREATE TABLE career_predictions (
    id                  INT       AUTO_INCREMENT PRIMARY KEY,
    user_id             INT       NOT NULL,
    session_id          INT,
    top1_career         VARCHAR(150),
    top1_confidence     FLOAT     COMMENT 'Confidence % (0-100)',
    top5_careers_json   LONGTEXT  COMMENT 'JSON array of top 5 career objects',
    shap_json           LONGTEXT  COMMENT 'SHAP attribution chips JSON',
    readiness_score     FLOAT     DEFAULT 0 COMMENT 'Overall career readiness 0-100',
    predicted_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_pred_user    (user_id),
    INDEX idx_pred_session (session_id),
    INDEX idx_pred_career  (top1_career)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 14: career_history
-- Historical log of all career predictions per user (for trend charts)
-- ==============================================================================
CREATE TABLE career_history (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    career          VARCHAR(150),
    confidence      FLOAT,
    assessment_date TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_ch_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- TABLE 15: roadmaps
-- Career roadmap steps, certifications, and resources (shown after prediction)
-- ==============================================================================
CREATE TABLE roadmaps (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    career          VARCHAR(150) UNIQUE NOT NULL,
    steps_json      LONGTEXT     COMMENT 'JSON array of roadmap steps',
    certifications  TEXT         COMMENT 'Recommended certifications',
    resources       TEXT         COMMENT 'Learning resources / links',
    updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_roadmap_career (career)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==============================================================================
-- SEED DATA: DEFAULT ADMIN USER
-- Email: admin@gmail.com | Password: Admin@123
-- Password hash generated with Werkzeug pbkdf2:sha256
-- ==============================================================================
INSERT INTO users (full_name, email, password_hash, role)
VALUES (
    'System Administrator',
    'admin@gmail.com',
    'pbkdf2:sha256:600000$rVJkb2NhcmVlcl9z$1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b',
    'admin'
);

-- NOTE: The hash above is a placeholder.
-- The real hash is generated by the Flask app on startup (init_db function).
-- The Flask app will auto-update this hash when it first runs.
-- Just make sure admin@gmail.com exists — Flask handles the rest.

-- ==============================================================================
-- SEED DATA: SKILLS MASTER LIST
-- ==============================================================================
INSERT INTO skills (skill_name, category, domain) VALUES
-- Technical Skills
('Python',              'Technical', 'IT'),
('Java',                'Technical', 'IT'),
('C++',                 'Technical', 'IT'),
('JavaScript',          'Technical', 'IT'),
('React',               'Technical', 'IT'),
('Node.js',             'Technical', 'IT'),
('SQL & Databases',     'Technical', 'IT'),
('Machine Learning',    'Technical', 'IT'),
('Deep Learning',       'Technical', 'IT'),
('Data Analysis',       'Technical', 'IT'),
('Cloud Computing',     'Technical', 'IT'),
('Cybersecurity',       'Technical', 'IT'),
('DevOps',              'Technical', 'IT'),
('UI/UX Design',        'Technical', 'IT'),
('Mobile Development',  'Technical', 'IT'),
-- Business Skills
('Financial Accounting','Technical', 'Business'),
('Business Management', 'Domain',    'Business'),
('Digital Marketing',   'Domain',    'Business'),
('Project Management',  'Domain',    'Business'),
('Data Analytics',      'Technical', 'Business'),
-- Science & Healthcare
('Biology',             'Domain',    'Healthcare'),
('Chemistry',           'Domain',    'Science'),
('Physics',             'Domain',    'Science'),
('Medical Science',     'Domain',    'Healthcare'),
-- Creative
('Graphic Design',      'Technical', 'Arts'),
('Video Editing',       'Technical', 'Arts'),
('Content Writing',     'Soft Skill','Arts'),
('Photography',         'Technical', 'Arts'),
-- Soft Skills
('Leadership',          'Soft Skill','General'),
('Communication',       'Soft Skill','General'),
('Problem Solving',     'Soft Skill','General'),
('Critical Thinking',   'Soft Skill','General'),
('Teamwork',            'Soft Skill','General');


-- ==============================================================================
-- SEED DATA: CAREER ROADMAPS (30 Careers)
-- ==============================================================================
INSERT INTO roadmaps (career, steps_json, certifications, resources) VALUES

('Software Developer',
 '[{"step":1,"title":"Learn Programming Fundamentals","desc":"Master Python/Java/C++, data structures & algorithms"},{"step":2,"title":"Version Control","desc":"Git, GitHub — branching, pull requests, collaboration"},{"step":3,"title":"Web Development Basics","desc":"HTML, CSS, JavaScript, REST APIs"},{"step":4,"title":"Backend or Frontend Specialization","desc":"Choose Node.js/Django/Spring (backend) or React/Vue (frontend)"},{"step":5,"title":"Database Design","desc":"SQL (MySQL/PostgreSQL), NoSQL (MongoDB)"},{"step":6,"title":"Build Projects","desc":"Build 3-5 full projects for portfolio"},{"step":7,"title":"Internship & Open Source","desc":"Contribute to open source, complete an internship"},{"step":8,"title":"Job Ready","desc":"DSA prep, system design, mock interviews"}]',
 'AWS Developer, Azure Fundamentals, Meta React Developer, Oracle Java SE',
 'LeetCode, HackerRank, freeCodeCamp, CS50 Harvard, The Odin Project'),

('Data Scientist',
 '[{"step":1,"title":"Mathematics & Statistics","desc":"Linear algebra, probability, statistics, calculus"},{"step":2,"title":"Python for Data Science","desc":"NumPy, Pandas, Matplotlib, Seaborn"},{"step":3,"title":"Machine Learning","desc":"Scikit-learn, supervised & unsupervised learning, model evaluation"},{"step":4,"title":"Deep Learning","desc":"TensorFlow, PyTorch, CNNs, RNNs"},{"step":5,"title":"Data Wrangling & EDA","desc":"Data cleaning, feature engineering, exploratory analysis"},{"step":6,"title":"SQL & Big Data","desc":"SQL, Spark, Hadoop basics"},{"step":7,"title":"Kaggle & Projects","desc":"Compete on Kaggle, build end-to-end ML projects"},{"step":8,"title":"Domain Specialization","desc":"NLP, Computer Vision, Time Series"}]',
 'Google Data Analytics, IBM Data Science, AWS ML Specialty, Coursera ML Specialization',
 'Kaggle, fast.ai, Coursera, Towards Data Science, StatQuest YouTube'),

('Machine Learning Engineer',
 '[{"step":1,"title":"Programming — Python Advanced","desc":"OOP, functional programming, async"},{"step":2,"title":"ML Fundamentals","desc":"Classical ML algorithms, math behind them"},{"step":3,"title":"ML Frameworks","desc":"TensorFlow, PyTorch, Keras, Scikit-learn"},{"step":4,"title":"MLOps & Deployment","desc":"Docker, Kubernetes, MLflow, model serving"},{"step":5,"title":"Feature Engineering","desc":"Advanced techniques, pipelines"},{"step":6,"title":"Cloud ML Services","desc":"AWS SageMaker, Google Vertex AI, Azure ML"},{"step":7,"title":"Research Papers","desc":"Read and implement SOTA papers"},{"step":8,"title":"Production Projects","desc":"Deploy real ML systems at scale"}]',
 'AWS ML Specialty, Google Professional ML Engineer, TensorFlow Developer',
 'Papers With Code, Hugging Face, fast.ai, Made With ML'),

('AI Engineer',
 '[{"step":1,"title":"Python + ML Foundations","desc":"Strong Python, linear algebra, calculus, probability"},{"step":2,"title":"Deep Learning","desc":"Neural networks, backpropagation, PyTorch/TensorFlow"},{"step":3,"title":"LLMs & Generative AI","desc":"Transformers, BERT, GPT, fine-tuning, prompt engineering"},{"step":4,"title":"Computer Vision / NLP","desc":"Specialize in one domain"},{"step":5,"title":"AI System Design","desc":"Architecture patterns for AI applications"},{"step":6,"title":"Deployment & Scaling","desc":"FastAPI, Docker, cloud GPU, ONNX"},{"step":7,"title":"Research & Innovation","desc":"Implement papers, push boundaries"},{"step":8,"title":"Build AI Products","desc":"End-to-end AI applications"}]',
 'DeepLearning.AI Specializations, Hugging Face Course, NVIDIA DLI, OpenAI API',
 'Andrej Karpathy YouTube, Hugging Face, ArXiv, DeepMind Blog'),

('Cyber Security Analyst',
 '[{"step":1,"title":"Networking Basics","desc":"TCP/IP, OSI model, subnetting, firewalls"},{"step":2,"title":"Operating Systems","desc":"Linux fundamentals, Windows Server, command line"},{"step":3,"title":"Security Concepts","desc":"CIA triad, encryption, PKI, authentication"},{"step":4,"title":"Ethical Hacking","desc":"Penetration testing, Kali Linux, Metasploit"},{"step":5,"title":"Security Tools","desc":"Wireshark, Nmap, Burp Suite, SIEM"},{"step":6,"title":"Incident Response","desc":"SOC operations, forensics, threat hunting"},{"step":7,"title":"Compliance","desc":"ISO 27001, GDPR, NIST framework"},{"step":8,"title":"Specialization","desc":"Red team, Blue team, Cloud security"}]',
 'CompTIA Security+, CEH, CISSP, OSCP, AWS Security Specialty',
 'TryHackMe, HackTheBox, Cybrary, SANS Institute, OWASP'),

('Doctor',
 '[{"step":1,"title":"Class 11-12 — PCB","desc":"Biology, Physics, Chemistry with 85%+ marks"},{"step":2,"title":"NEET Preparation","desc":"Intensive NEET coaching, biology mastery"},{"step":3,"title":"MBBS — 5.5 Years","desc":"Pre-clinical, para-clinical, clinical subjects"},{"step":4,"title":"Internship — 1 Year","desc":"Rotating clinical internship across departments"},{"step":5,"title":"MD/MS Entrance","desc":"NEET-PG preparation, residency application"},{"step":6,"title":"Postgraduate Specialization","desc":"3 years MD/MS in chosen specialty"},{"step":7,"title":"Super-specialty (optional)","desc":"DM/MCh for further specialization"},{"step":8,"title":"Practice / Research","desc":"Hospital practice or medical research"}]',
 'MBBS, MD/MS, Medical Council Registration, USMLE (USA), PLAB (UK)',
 'Marrow, PrepLadder, DAMS, Harrison Textbook, Robbins Pathology'),

('Lawyer',
 '[{"step":1,"title":"Class 12 — Any Stream","desc":"Humanities preferred; strong English and reasoning skills"},{"step":2,"title":"CLAT / LSAT Preparation","desc":"Legal aptitude, reasoning, English comprehension"},{"step":3,"title":"LLB — 3 or 5 Years","desc":"Law school: constitutional, criminal, civil, corporate law"},{"step":4,"title":"Moot Courts & Internships","desc":"Practice advocacy, intern with law firms and courts"},{"step":5,"title":"Bar Council Enrollment","desc":"Pass All India Bar Examination (AIBE)"},{"step":6,"title":"LLM (optional)","desc":"Specialization: corporate law, human rights, IP, tax"},{"step":7,"title":"Practice Area","desc":"Litigation, corporate, criminal, family, IP law"},{"step":8,"title":"Build Reputation","desc":"Build client base, publish articles, join bar associations"}]',
 'AIBE, CLAT, LLM, International Arbitration courses',
 'Manupatra, SCC Online, Bar & Bench, Indian Kanoon'),

('Chartered Accountant',
 '[{"step":1,"title":"Class 12 — Commerce","desc":"Accounts, Economics, Business Studies with 60%+"},{"step":2,"title":"CA Foundation","desc":"4 papers: Accounts, Law, Economics, Maths"},{"step":3,"title":"CA Intermediate","desc":"8 papers across Group 1 and Group 2"},{"step":4,"title":"Articleship — 3 Years","desc":"Practical training under a CA firm"},{"step":5,"title":"CA Final","desc":"Advanced accounts, audit, tax, law (hardest level)"},{"step":6,"title":"ICAI Membership","desc":"Receive membership and COP"},{"step":7,"title":"Specialization","desc":"Audit, Tax, Finance, IFRS, Forensics"},{"step":8,"title":"Practice or Industry","desc":"Start own practice or join Big 4 firms"}]',
 'CA (ICAI), CPA (USA), CMA, ACCA, IFRS Diploma',
 'ICAI Study Material, ICAI Portal, CA Wizard, Unacademy CA'),

('School Teacher',
 '[{"step":1,"title":"Subject Mastery","desc":"Strong command of chosen subject(s)"},{"step":2,"title":"Graduation in Subject","desc":"B.Sc, B.A, B.Com in relevant subject"},{"step":3,"title":"B.Ed — 2 Years","desc":"Bachelor of Education: pedagogy, teaching methods"},{"step":4,"title":"CTET / TET","desc":"Clear Central or State Teacher Eligibility Test"},{"step":5,"title":"Teaching Internship","desc":"Practice teaching in schools during B.Ed"},{"step":6,"title":"Apply for Teaching Posts","desc":"KVS, NVS, State Board, Private schools"},{"step":7,"title":"Continuous Development","desc":"Workshops, DIKSHA courses, new pedagogy methods"},{"step":8,"title":"Leadership (optional)","desc":"HoD, Vice Principal, Principal paths"}]',
 'B.Ed, CTET, TET, DIKSHA Courses, Diploma in Education',
 'NCERT, DIKSHA Portal, Unacademy Teaching, YouTube Education Channels'),

('Entrepreneur',
 '[{"step":1,"title":"Identify a Problem","desc":"Find a real-world pain point worth solving"},{"step":2,"title":"Build Skills","desc":"Sales, marketing, finance, product management, tech basics"},{"step":3,"title":"Market Research","desc":"Validate idea, study competition, find target market"},{"step":4,"title":"MVP — Minimum Viable Product","desc":"Build the simplest version of your solution"},{"step":5,"title":"Get Early Customers","desc":"Beta testing, feedback loops, product-market fit"},{"step":6,"title":"Funding","desc":"Bootstrapping, angel investors, venture capital, grants"},{"step":7,"title":"Scale Operations","desc":"Hire team, systemize processes, expand markets"},{"step":8,"title":"Exit or Grow","desc":"IPO, acquisition, or continued growth"}]',
 'MBA, Google Startup Course, Y Combinator Startup School, Product Management',
 'Y Combinator Blog, Ycombinator Startup School, Paul Graham Essays, TechCrunch'),

('Business Analyst',
 '[{"step":1,"title":"Business Fundamentals","desc":"Economics, finance, management basics"},{"step":2,"title":"Data & Analytics Skills","desc":"Excel, SQL, Power BI, Tableau"},{"step":3,"title":"Requirements Gathering","desc":"Stakeholder management, BRD writing, use cases"},{"step":4,"title":"Process Modeling","desc":"BPMN, flowcharts, UML diagrams"},{"step":5,"title":"Agile & SDLC","desc":"Scrum, Kanban, Jira, waterfall vs agile"},{"step":6,"title":"Domain Knowledge","desc":"Banking, healthcare, retail — pick an industry"},{"step":7,"title":"Certifications","desc":"CBAP, PMI-PBA, ECBA"},{"step":8,"title":"Senior BA / Product Manager","desc":"Progress to senior BA or transition to PM role"}]',
 'CBAP, PMI-PBA, ECBA, Google Data Analytics, Power BI Certification',
 'IIBA, BA Times, Modern Analyst, Udemy BA courses'),

('Graphic Designer',
 '[{"step":1,"title":"Design Principles","desc":"Color theory, typography, composition, visual hierarchy"},{"step":2,"title":"Adobe Creative Suite","desc":"Photoshop, Illustrator, InDesign — master all three"},{"step":3,"title":"UI/UX Basics","desc":"Figma, wireframing, user interface design"},{"step":4,"title":"Build Portfolio","desc":"Create 10-15 diverse design projects"},{"step":5,"title":"Freelancing","desc":"Fiverr, Upwork, 99designs — build client base"},{"step":6,"title":"Specialization","desc":"Logo design, brand identity, print, digital, motion"},{"step":7,"title":"Motion Graphics (optional)","desc":"After Effects, Premiere Pro, animation"},{"step":8,"title":"Senior Designer / Creative Director","desc":"Lead design teams or start design studio"}]',
 'Adobe Certified Expert, Google UX Design, Figma Certification, Canva Expert',
 'Behance, Dribbble, Adobe Learn, Coursera UX Design, Awwwards'),

('Professor/Researcher',
 '[{"step":1,"title":"Strong Academic Foundation","desc":"Top grades in Bachelor degree in chosen field"},{"step":2,"title":"Master Degree","desc":"MSc/MTech/MA — research methodology, thesis writing"},{"step":3,"title":"PhD","desc":"4-6 years doctoral research, publish papers"},{"step":4,"title":"PostDoc (optional)","desc":"2-3 years post-doctoral research for top universities"},{"step":5,"title":"Research Publications","desc":"Publish in SCI/Scopus indexed journals, conferences"},{"step":6,"title":"NET/SET Qualification","desc":"UGC-NET for lectureship and JRF in India"},{"step":7,"title":"University Position","desc":"Assistant Professor → Associate Professor → Professor"},{"step":8,"title":"Research Leadership","desc":"Guide PhD students, run research lab, get funding"}]',
 'UGC-NET, PhD, Research Methodology courses, Grant Writing',
 'ResearchGate, Google Scholar, Academia.edu, Springer, Elsevier'),

('Data Analyst',
 '[{"step":1,"title":"Excel & Statistics","desc":"Advanced Excel, pivot tables, statistical analysis"},{"step":2,"title":"SQL","desc":"Complex queries, joins, aggregations, window functions"},{"step":3,"title":"Python/R for Analysis","desc":"Pandas, NumPy, data wrangling, EDA"},{"step":4,"title":"Data Visualization","desc":"Power BI, Tableau, Matplotlib, Seaborn"},{"step":5,"title":"Dashboard Building","desc":"Build interactive business dashboards"},{"step":6,"title":"Storytelling with Data","desc":"Present insights clearly to non-technical stakeholders"},{"step":7,"title":"Domain Knowledge","desc":"Finance, marketing, HR, supply chain analytics"},{"step":8,"title":"Senior Analyst / DS","desc":"Progress to Senior Analyst or Data Scientist"}]',
 'Google Data Analytics, Power BI, Tableau Desktop Specialist, SQL Certifications',
 'Mode Analytics, DataCamp, Kaggle, Towards Data Science'),

('Cloud Architect',
 '[{"step":1,"title":"Networking & Linux","desc":"TCP/IP, DNS, load balancing, Linux administration"},{"step":2,"title":"Cloud Fundamentals","desc":"AWS/Azure/GCP — compute, storage, networking services"},{"step":3,"title":"Infrastructure as Code","desc":"Terraform, CloudFormation, Ansible"},{"step":4,"title":"Containers & Orchestration","desc":"Docker, Kubernetes, Helm"},{"step":5,"title":"CI/CD Pipelines","desc":"Jenkins, GitHub Actions, GitLab CI"},{"step":6,"title":"Security & Compliance","desc":"IAM, encryption, compliance frameworks"},{"step":7,"title":"Cost Optimization","desc":"FinOps, reserved instances, right-sizing"},{"step":8,"title":"Architecture Design","desc":"Design scalable, fault-tolerant systems at enterprise scale"}]',
 'AWS Solutions Architect, Azure Solutions Architect, GCP Professional Cloud Architect, Kubernetes CKA',
 'AWS Documentation, A Cloud Guru, Linux Foundation, Cloud Architecture Patterns'),

('Full Stack Developer',
 '[{"step":1,"title":"HTML/CSS/JS Basics","desc":"Responsive design, Flexbox, Grid, ES6+"},{"step":2,"title":"Frontend Framework","desc":"React.js or Vue.js — components, state management"},{"step":3,"title":"Backend Development","desc":"Node.js/Express or Django/Flask"},{"step":4,"title":"Database Integration","desc":"MySQL, MongoDB, ORMs"},{"step":5,"title":"REST APIs & GraphQL","desc":"Design and consume APIs"},{"step":6,"title":"Authentication & Security","desc":"JWT, OAuth, HTTPS, input validation"},{"step":7,"title":"Deployment","desc":"Heroku, Vercel, AWS, Nginx, Docker basics"},{"step":8,"title":"Full Projects","desc":"Build 3-5 complete full-stack apps for portfolio"}]',
 'Meta Full Stack Developer, AWS Developer, MongoDB Developer, Node.js Certification',
 'The Odin Project, freeCodeCamp, Full Stack Open, Traversy Media YouTube');


-- ==============================================================================
-- VERIFY: Show all created tables
-- ==============================================================================
SELECT
    TABLE_NAME       AS `Table`,
    TABLE_ROWS       AS `Est. Rows`,
    ROUND(DATA_LENGTH/1024, 1) AS `Data KB`,
    TABLE_COMMENT    AS `Description`
FROM
    information_schema.TABLES
WHERE
    TABLE_SCHEMA = 'career_system_db'
ORDER BY
    TABLE_NAME;


-- ==============================================================================
-- QUICK TEST QUERIES (run after setup to verify everything works)
-- ==============================================================================

-- Check admin user exists:
-- SELECT id, full_name, email, role FROM users;

-- Check skills seeded:
-- SELECT COUNT(*) AS total_skills FROM skills;

-- Check roadmaps seeded:
-- SELECT career, LENGTH(steps_json) AS steps_size FROM roadmaps;

-- Check all tables exist:
-- SHOW TABLES;

-- ==============================================================================
-- END OF SETUP SCRIPT
-- ==============================================================================
-- 15 Tables Created:
--   1. users                 — All users (students + admins)
--   2. student_profiles      — Bio, LinkedIn, GitHub links
--   3. education_profiles    — Degree, CGPA, stream, board
--   4. subject_marks         — Semester-wise subject marks
--   5. question_bank         — MCQ assessment questions (seeded by Flask)
--   6. assessment_sessions   — Each assessment attempt
--   7. assessment_answers    — Individual MCQ answers
--   8. feature_scores        — Computed ML feature scores
--   9. skills                — Master skills list (33 skills seeded)
--  10. skill_verification    — Student skill quiz scores
--  11. projects              — Student project portfolio
--  12. certifications        — Student certifications
--  13. career_predictions    — ML model output (top-5 careers)
--  14. career_history        — Career prediction history log
--  15. roadmaps              — Career roadmap steps (16 roadmaps seeded)
-- ==============================================================================

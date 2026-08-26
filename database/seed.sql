-- ============================================================
-- Career Recommendation System - MySQL Seed Script
-- Database Name: career_recommendation_db
-- Target: MySQL 8.x Server & MySQL Workbench
-- ============================================================

USE `career_recommendation_db`;

-- ------------------------------------------------------------
-- 1. Insert Question Sections (19 Sections)
-- ------------------------------------------------------------
INSERT INTO `question_sections` (`id`, `name`, `description`, `display_order`, `is_active`) VALUES
(1, 'Academic', 'Self-reported academic marks and core subject proficiencies.', 1, 1),
(2, 'Mathematical Ability', 'Numerical problem solving, algebra, geometry, and arithmetic logic.', 2, 1),
(3, 'Logical Reasoning', 'Pattern identification, syllogisms, deductive reasoning, and sequence series.', 3, 1),
(4, 'Scientific Thinking', 'Hypothesis testing, empirical reasoning, physical laws, and cause-effect deduction.', 4, 1),
(5, 'Problem Solving', 'Troubleshooting complex multi-step scenarios, strategic decomposition, and decision making.', 5, 1),
(6, 'Analytical Thinking', 'Data interpretation, graphical analysis, and structured comparative logic.', 6, 1),
(7, 'Communication', 'Verbal articulation, reading comprehension, writing precision, and interpersonal expression.', 7, 1),
(8, 'Creativity', 'Original ideation, divergent thinking, aesthetic composition, and innovative design.', 8, 1),
(9, 'Digital Ability', 'Computational logic, software navigation, algorithmic thinking, and internet fluency.', 9, 1),
(10, 'Learning Ability', 'Rapid concept absorption, memory recall, intellectual curiosity, and cognitive agility.', 10, 1),
(11, 'Spatial Ability', 'Mental rotation, 3D visualization, map orientation, and structural geometry.', 11, 1),
(12, 'Practical Ability', 'Hands-on mechanical aptitude, tool handling, and physical troubleshooting.', 12, 1),
(13, 'Interests', 'Personal curiosity and intrinsic motivation across disciplinary fields.', 13, 1),
(14, 'Activities', 'Frequency and involvement in extracurriculars, clubs, projects, and hobbies.', 14, 1),
(15, 'Teamwork', 'Collaborative problem solving, empathy, active listening, and consensus building.', 15, 1),
(16, 'Leadership', 'Initiative taking, organizing peers, goal setting, and inspiring responsibility.', 16, 1),
(17, 'Work Preferences', 'Ideal working environments, pace, structure, autonomy, and collaboration style.', 17, 1),
(18, 'Career Awareness', 'Knowledge of modern career pathways, industry roles, and emerging disciplines.', 18, 1),
(19, 'Career Preferences', 'Aspirational vocational targets, impact preferences, and industry goals.', 19, 1)
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`), `display_order` = VALUES(`display_order`);

-- ------------------------------------------------------------
-- 2. Insert Career Domains (23 Domains)
-- ------------------------------------------------------------
INSERT INTO `career_domains` (`id`, `domain_name`, `description`, `icon`, `display_order`, `is_active`) VALUES
(1, 'Technology', 'Software engineering, artificial intelligence, cloud architecture, cybersecurity, and data analytics.', 'bi-cpu', 1, 1),
(2, 'Healthcare', 'Clinical medicine, surgery, nursing, dentistry, pharmacy, and mental healthcare.', 'bi-heart-pulse', 2, 1),
(3, 'Engineering', 'Mechanical, civil, electrical, robotics, aerospace, and chemical systems design.', 'bi-gear-wide-connected', 3, 1),
(4, 'Science', 'Pure physical sciences, chemistry, molecular biology, astronomy, and astrophysics.', 'bi-radioactive', 4, 1),
(5, 'Research', 'Academic inquiry, industrial R&D, clinical trials, and scientific discovery.', 'bi-search', 5, 1),
(6, 'Business', 'Corporate management, entrepreneurship, international business, and operations.', 'bi-briefcase', 6, 1),
(7, 'Finance', 'Investment banking, financial analysis, quantitative trading, and accounting.', 'bi-currency-exchange', 7, 1),
(8, 'Law', 'Constitutional law, corporate jurisprudence, litigation, and human rights advocacy.', 'bi-shield-check', 8, 1),
(9, 'Education', 'Pedagogy, higher education, curriculum design, and educational technology.', 'bi-book', 9, 1),
(10, 'Psychology', 'Clinical psychology, cognitive neuropsychology, counseling, and organizational behavior.', 'bi-person-heart', 10, 1),
(11, 'Arts', 'Fine arts, sculpture, illustration, theater, and performing arts.', 'bi-palette', 11, 1),
(12, 'Design', 'UI/UX design, industrial product design, architecture, and graphic styling.', 'bi-bezier2', 12, 1),
(13, 'Media', 'Journalism, film making, broadcast media, public relations, and content production.', 'bi-camera-reels', 13, 1),
(14, 'Government', 'Civil administrative services, diplomacy, public policy, and defense administration.', 'bi-bank', 14, 1),
(15, 'Agriculture', 'Agronomy, precision farming, horticulture, and sustainable food systems.', 'bi-tree', 15, 1),
(16, 'Environment', 'Ecology, renewable energy systems, conservation biology, and climate science.', 'bi-globe-americas', 16, 1),
(17, 'Sports', 'Athletic coaching, sports physiotherapy, sports analytics, and fitness management.', 'bi-trophy', 17, 1),
(18, 'Hospitality', 'Hotel management, culinary arts, tourism, and event coordination.', 'bi-cup-hot', 18, 1),
(19, 'Aviation', 'Commercial flight piloting, air traffic management, avionics, and flight operations.', 'bi-airplane', 19, 1),
(20, 'Manufacturing', 'Industrial automation, supply chain optimization, and precision tooling.', 'bi-tools', 20, 1),
(21, 'Construction', 'Structural engineering, construction project management, and urban development.', 'bi-building', 21, 1),
(22, 'Skilled Trades', 'Electrical grid systems, specialized machining, and technical fabrication.', 'bi-wrench-adjustable', 22, 1),
(23, 'Transportation', 'Logistics network management, maritime operations, and rail infrastructure.', 'bi-truck', 23, 1)
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`), `icon` = VALUES(`icon`);

-- ------------------------------------------------------------
-- 3. Insert Career Subdomains
-- ------------------------------------------------------------
INSERT INTO `career_subdomains` (`id`, `domain_id`, `name`, `description`) VALUES
(1, 1, 'Software & Web Development', 'Building scalable web, mobile, and enterprise software systems.'),
(2, 1, 'Data Science & Artificial Intelligence', 'Machine learning, statistical modeling, big data architectures, and AI systems.'),
(3, 1, 'Cybersecurity & Cloud Systems', 'Information security, network protection, cloud infrastructure, and DevOps.'),
(4, 2, 'Clinical Medicine & Surgery', 'Direct patient diagnosis, surgical intervention, and medical treatment.'),
(5, 2, 'Allied Health Sciences & Diagnostics', 'Radiology, medical laboratory diagnostics, physiotherapy, and pharmacology.'),
(6, 3, 'Mechanical & Robotics Engineering', 'Machine design, automation, thermal systems, and robotic kinematics.'),
(7, 3, 'Civil & Structural Engineering', 'Infrastructure design, structural stability, transport systems, and urban planning.'),
(8, 6, 'Corporate Strategy & Management', 'Business consulting, executive operations, and organizational management.'),
(9, 7, 'Banking & Financial Markets', 'Securities trading, portfolio management, auditing, and corporate finance.'),
(10, 8, 'Corporate & Commercial Law', 'Contracts, intellectual property, mergers & acquisitions, and compliance.'),
(11, 12, 'Digital & Interaction Design', 'User experience, product interfaces, wireframing, and interactive design.'),
(12, 15, 'Sustainable Agritech & Farming', 'Modern agricultural technology, soil science, and crop genetics.')
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`);

-- ------------------------------------------------------------
-- 4. Insert Career Clusters
-- ------------------------------------------------------------
INSERT INTO `career_clusters` (`id`, `subdomain_id`, `name`, `description`) VALUES
(1, 1, 'Full-Stack Software Engineering', 'End-to-end software application architecture, frontend logic, and backend databases.'),
(2, 2, 'Applied Machine Learning & AI', 'Predictive modeling, deep learning architectures, computer vision, and NLP.'),
(3, 3, 'Cloud Infrastructure & DevOps', 'Distributed server clusters, CI/CD pipelines, and cloud reliability.'),
(4, 4, 'General Medicine & Critical Care', 'Emergency medicine, internal medicine, and patient therapies.'),
(5, 6, 'Autonomous Robotics & Mechatronics', 'Robotic hardware integration, sensors, actuators, and embedded software.'),
(6, 9, 'Financial Analysis & Investment Advisory', 'Equities valuation, risk modeling, and capital markets investment.'),
(7, 10, 'Corporate Legal Advisory', 'Commercial contract governance and regulatory compliance.'),
(8, 11, 'UI/UX & Product Design', 'Human-computer interaction and user interface design systems.')
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`);

-- ------------------------------------------------------------
-- 5. Insert Sample Careers
-- ------------------------------------------------------------
INSERT INTO `careers` (
    `id`, `career_code`, `career_name`, `domain_id`, `subdomain_id`, `cluster_id`,
    `description`, `minimum_education`, `typical_education`,
    `preferred_subjects`, `work_environment`, `work_style`,
    `career_pathway`, `entry_level_role`, `advanced_role`,
    `related_careers`, `is_active`
) VALUES
(
    1, 'CAR-TECH-001', 'Software Development Engineer', 1, 1, 1,
    'Designs, builds, tests, and maintains scalable software applications, distributed microservices, and databases.',
    'B.Tech / B.E. / B.Sc in Computer Science / BCA', 'B.Tech / B.E. in Computer Science or M.Tech / MCA',
    'Mathematics, Computer Science, Physics', 'Office / Tech Campus / Remote', 'Analytical, Investigative, Team-Oriented',
    'Higher Secondary (PCM/CS) -> B.Tech CSE -> Junior Software Engineer -> Senior Software Engineer -> Principal Architect',
    'Junior Software Engineer / Frontend Developer', 'Principal Software Architect / VP of Engineering',
    'Data Scientist, Cloud Solutions Architect, DevOps Engineer', 1
),
(
    2, 'CAR-TECH-002', 'Data Scientist & AI Specialist', 1, 2, 2,
    'Extracts actionable insights from massive datasets using advanced mathematical modeling, machine learning algorithms, and statistical analysis.',
    'B.Tech / B.Sc in Statistics, Mathematics, or Data Science', 'M.Tech / M.Sc / Ph.D in Data Science or Machine Learning',
    'Mathematics, Statistics, Computer Science', 'Tech Labs / Corporate HQ / Remote', 'Analytical, Investigative, Research-Focused',
    'Higher Secondary (PCM/Statistics) -> B.Tech / B.Sc Data Science -> Data Analyst -> Machine Learning Engineer -> Chief Data Officer',
    'Associate Data Analyst / Junior ML Engineer', 'Lead Data Scientist / AI Research Director',
    'Software Engineer, Business Intelligence Analyst, Quantitative Researcher', 1
),
(
    3, 'CAR-TECH-003', 'Cybersecurity Specialist', 1, 3, 3,
    'Protects organizational information systems, computer networks, and cloud infrastructure from security breaches, cyber attacks, and data leaks.',
    'B.Tech / B.Sc in Cybersecurity / Information Technology', 'B.Tech IT / Cybersecurity + CISSP / CEH Certifications',
    'Computer Science, Mathematics, Physics', 'Security Operations Center (SOC) / Enterprise IT', 'Analytical, Structured, Vigilant',
    'Higher Secondary (PCM/CS) -> B.Tech CS/Cybersecurity -> SOC Analyst -> Security Engineer -> Chief Information Security Officer (CISO)',
    'Junior Cybersecurity Analyst / Penetration Tester', 'Chief Information Security Officer (CISO)',
    'Cloud Security Engineer, Network Engineer, Forensics Specialist', 1
),
(
    4, 'CAR-HLTH-001', 'Medical Practitioner (General Physician)', 2, 4, 4,
    'Diagnoses acute and chronic illnesses, prescribes treatments, conducts preventive health screenings, and manages primary patient care.',
    'MBBS (Bachelor of Medicine, Bachelor of Surgery)', 'MBBS + MD / DNB in General Medicine',
    'Biology, Chemistry, Physics, English', 'Hospitals, Clinics, Medical Research Centers', 'Empathetic, Investigative, Detail-Oriented',
    'Higher Secondary (PCB) -> NEET UG -> MBBS (5.5 yrs) -> Compulsory Internship -> MD General Medicine -> Consultant Physician',
    'Resident Medical Officer / Junior Doctor', 'Senior Consultant / Head of Department (HOD)',
    'Surgeon, Pediatrician, Medical Researcher, Epidemiologist', 1
),
(
    5, 'CAR-ENG-001', 'Robotics & Automation Engineer', 3, 6, 5,
    'Designs, programs, and integrates autonomous robotic hardware, robotic arms, sensors, and intelligent automation systems for industries.',
    'B.Tech / B.E. in Robotics, Mechatronics, or Mechanical Engineering', 'M.Tech in Robotics / Artificial Intelligence Systems',
    'Physics, Mathematics, Computer Science', 'Robotics R&D Laboratories, Manufacturing Facilities', 'Practical, Analytical, Innovative',
    'Higher Secondary (PCM) -> B.Tech Robotics/Mechatronics -> Robotics Developer -> Automation Lead -> Director of Robotics R&D',
    'Junior Automation Engineer / Robotic Programmer', 'Chief Robotics Engineer / R&D Director',
    'Mechanical Engineer, Embedded Systems Engineer, AI Engineer', 1
),
(
    6, 'CAR-FIN-001', 'Financial Analyst & Investment Banker', 7, 9, 6,
    'Evaluates financial market trends, corporate financial statements, valuations, investment portfolios, and risk mitigation strategies.',
    'B.Com / BBA in Finance / B.Sc Economics', 'MBA in Finance / Chartered Accountant (CA) / CFA Charterholder',
    'Mathematics, Economics, Accountancy, Business Studies', 'Investment Banks, Financial Brokerages, Corporate Finance Offices', 'Analytical, Quantitative, High-Pace',
    'Higher Secondary (Commerce/Science with Math) -> B.Com/BBA/Econ -> CA/CFA/MBA -> Junior Financial Analyst -> Portfolio Fund Manager',
    'Financial Analyst / Investment Research Associate', 'Managing Director of Investment Banking / Chief Financial Officer (CFO)',
    'Chartered Accountant, Risk Manager, Management Consultant', 1
),
(
    7, 'CAR-LAW-001', 'Corporate Legal Counsel', 8, 10, 7,
    'Advises corporations on legal rights, obligations, commercial contract negotiations, mergers and acquisitions, and regulatory compliance.',
    'BA LLB / BBA LLB (5-Year Integrated Course)', 'LL.M in Corporate & Commercial Law',
    'English, Political Science, History, Economics, Legal Studies', 'Corporate Law Firms, Multi-National Corporate Legal Departments', 'Structured, Communicative, Strategic',
    'Higher Secondary (Any Stream with English) -> CLAT Exam -> 5-Year Integrated LLB -> Associate Lawyer -> General Legal Counsel',
    'Junior Associate Legal Counsel', 'Partner at Law Firm / General Corporate Counsel',
    'Civil Litigator, Intellectual Property Attorney, Policy Advisor', 1
),
(
    8, 'CAR-DSGN-001', 'UI/UX & Digital Product Designer', 12, 11, 8,
    'Designs intuitive, accessible, and visually stunning digital user experiences, interfaces, wireframes, and design systems for web and mobile apps.',
    'B.Des in Interaction Design / B.Sc Visual Communication', 'M.Des in Human-Computer Interaction / Product Design',
    'Design, Fine Arts, Computer Science, Psychology', 'Design Agencies, Tech Product Companies, Remote Studios', 'Creative, Empathetic, Visual, Collaborative',
    'Higher Secondary (Any Stream) -> UCEED / NID Exam -> B.Des / M.Des -> Junior UI/UX Designer -> Product Design Lead -> Head of Design',
    'Junior UX Designer / Visual Interface Designer', 'VP of Design / Chief Design Officer',
    'Graphic Designer, Design Researcher, Creative Director', 1
)
ON DUPLICATE KEY UPDATE `career_name` = VALUES(`career_name`), `description` = VALUES(`description`);

-- ------------------------------------------------------------
-- 6. Insert Career Skills (Importance 1 to 5)
-- ------------------------------------------------------------
INSERT INTO `career_skills` (`career_id`, `skill_name`, `importance_level`) VALUES
-- Software Development Engineer
(1, 'Object-Oriented Programming (Python/Java/C++)', 5),
(1, 'Data Structures & Algorithms', 5),
(1, 'Database Architecture (SQL/NoSQL)', 4),
(1, 'System Design & Scalability', 4),
(1, 'Git Version Control & CI/CD', 4),
-- Data Scientist
(2, 'Machine Learning Algorithms', 5),
(2, 'Applied Statistics & Probability', 5),
(2, 'Python / R Programming', 5),
(2, 'Data Visualization & Storytelling', 4),
(2, 'SQL & Big Data Processing', 4),
-- Cybersecurity Specialist
(3, 'Network Security Protocols', 5),
(3, 'Penetration Testing & Vulnerability Assessment', 5),
(3, 'Incident Response & Threat Intelligence', 4),
(3, 'Cryptography & Public Key Infrastructure', 4),
-- General Physician
(4, 'Clinical Diagnostic Examination', 5),
(4, 'Pharmacology & Prescription Management', 5),
(4, 'Patient Empathy & Communication', 5),
(4, 'Emergency First Response Care', 4),
-- Robotics Engineer
(5, 'Kinematics & Dynamics of Mechanisms', 5),
(5, 'Embedded C / C++ Programming', 5),
(5, 'CAD / CAM 3D Modeling', 4),
(5, 'Sensor Integration & Signal Processing', 4),
-- Financial Analyst
(6, 'Financial Modeling & Valuation', 5),
(6, 'Excel & Quantitative Analysis', 5),
(6, 'Corporate Balance Sheet Auditing', 4),
(6, 'Macroeconomic Forecasting', 4),
-- Corporate Legal Counsel
(7, 'Contract Drafting & Negotiation', 5),
(7, 'Commercial Law Jurisprudence', 5),
(7, 'Legal Research & Case Analysis', 4),
(7, 'Oral & Written Argumentation', 4),
-- UI/UX Designer
(8, 'User Interface Prototyping (Figma)', 5),
(8, 'User Research & Usability Testing', 5),
(8, 'Information Architecture & Wireframing', 4),
(8, 'Design Systems & Typography', 4)
ON DUPLICATE KEY UPDATE `importance_level` = VALUES(`importance_level`);

-- ------------------------------------------------------------
-- 7. Insert Career Subjects (Importance 1 to 5)
-- ------------------------------------------------------------
INSERT INTO `career_subjects` (`career_id`, `subject_name`, `importance_level`) VALUES
-- Software Engineer
(1, 'Computer Science', 5),
(1, 'Mathematics', 5),
(1, 'Physics', 4),
-- Data Scientist
(2, 'Mathematics', 5),
(2, 'Computer Science', 5),
(2, 'Statistics', 5),
-- Cybersecurity
(3, 'Computer Science', 5),
(3, 'Mathematics', 4),
(3, 'Physics', 3),
-- Doctor
(4, 'Biology', 5),
(4, 'Chemistry', 5),
(4, 'Physics', 4),
(4, 'English', 4),
-- Robotics Engineer
(5, 'Physics', 5),
(5, 'Mathematics', 5),
(5, 'Computer Science', 4),
-- Financial Analyst
(6, 'Accountancy', 5),
(6, 'Economics', 5),
(6, 'Mathematics', 4),
(6, 'Business Studies', 4),
-- Corporate Lawyer
(7, 'Political Science', 5),
(7, 'English', 5),
(7, 'Economics', 4),
(7, 'History', 3),
-- UI/UX Designer
(8, 'Computer Science', 4),
(8, 'Psychology', 4),
(8, 'English', 4)
ON DUPLICATE KEY UPDATE `importance_level` = VALUES(`importance_level`);

-- ------------------------------------------------------------
-- 8. Insert Career Education Milestones
-- ------------------------------------------------------------
INSERT INTO `career_education` (`career_id`, `education_level`, `degree_name`, `description`, `sequence_order`) VALUES
(1, 'Higher Secondary (10+2)', 'Science Stream (PCM/CS)', 'Focus on core mathematics, physics, and computer science.', 1),
(1, 'Undergraduate (UG)', 'B.Tech / B.E. in Computer Science', '4-year foundational degree in algorithms, hardware, and software systems.', 2),
(1, 'Postgraduate (PG / Optional)', 'M.Tech / M.S. in Computer Science', 'Specialization in distributed computing or software architecture.', 3),
(4, 'Higher Secondary (10+2)', 'Science Stream (PCB)', 'Focus on biology, chemistry, and physics.', 1),
(4, 'Undergraduate (UG)', 'MBBS', '5.5-year clinical medicine degree including 1-year rotatory internship.', 2),
(4, 'Postgraduate (PG)', 'MD / MS in Internal Medicine / Surgery', '3-year specialty residency training.', 3),
(6, 'Higher Secondary (10+2)', 'Commerce / Science with Math', 'Focus on accountancy, economics, and mathematics.', 1),
(6, 'Undergraduate (UG)', 'B.Com / BBA / B.Sc Economics', '3-year foundational program in corporate financial structures.', 2),
(6, 'Postgraduate / Professional', 'MBA (Finance) / CFA / CA', 'Advanced financial charter or master of business administration.', 3),
(7, 'Higher Secondary (10+2)', 'Any Stream (Humanities/Commerce/Science)', 'Focus on language, analytical reading, and social sciences.', 1),
(7, 'Undergraduate (UG)', '5-Year Integrated B.A. LL.B / B.B.A. LL.B', 'Comprehensive law degree from recognized National Law University.', 2);

-- ------------------------------------------------------------
-- 9. Insert Career Pathways Stages
-- ------------------------------------------------------------
INSERT INTO `career_pathways` (`career_id`, `stage_number`, `stage_name`, `description`) VALUES
(1, 1, 'Academic Foundation', 'Excel in STEM subjects in grades 9-12 and participate in programming hackathons.'),
(1, 2, 'Undergraduate Engineering', 'Complete B.Tech in CSE, build full-stack projects, and secure industrial internships.'),
(1, 3, 'Junior Software Engineer', 'Work in development teams fixing bugs, building microservice features, and learning agile methodology.'),
(1, 4, 'Senior / Lead Engineer', 'Lead system design, mentor junior engineers, and manage high-traffic production releases.'),
(1, 5, 'Principal Architect / CTO', 'Define technology strategy, enterprise architecture, and technical innovation.');

-- ------------------------------------------------------------
-- 10. Insert Learning Resources
-- ------------------------------------------------------------
INSERT INTO `learning_resources` (`career_id`, `title`, `description`, `resource_type`, `url`, `difficulty`, `class_min`, `class_max`, `is_active`) VALUES
(1, 'CS50: Introduction to Computer Science', 'Harvard University foundation course in computational thinking and programming.', 'Online Course', 'https://cs50.harvard.edu', 'Beginner', 7, 12, 1),
(1, 'LeetCode Problem Solving Platform', 'Interactive algorithmic challenges across arrays, trees, graphs, and dynamic programming.', 'Practice Platform', 'https://leetcode.com', 'Intermediate', 9, 12, 1),
(2, 'Kaggle Machine Learning Track', 'Hands-on data science tutorials, datasets, and machine learning competitions.', 'Interactive Platform', 'https://www.kaggle.com/learn', 'Intermediate', 9, 12, 1),
(4, 'Khan Academy Human Biology & Anatomy', 'Comprehensive anatomical and physiological lesson modules for aspiring doctors.', 'Video Lessons', 'https://www.khanacademy.org/science/biology', 'Beginner', 7, 12, 1),
(8, 'Google UX Design Professional Certificate', 'Practical foundation in design thinking, user research, wireframing, and Figma.', 'Certification Course', 'https://grow.google/certificates/ux-design', 'Beginner', 8, 12, 1);

-- ------------------------------------------------------------
-- 11. Insert Adaptive Questions (Grades 7 to 12)
-- ------------------------------------------------------------
INSERT INTO `questions` (
    `id`, `question_code`, `question_text`, `section_id`, `question_type`,
    `class_min`, `class_max`, `difficulty`, `skill_category`,
    `is_required`, `display_order`, `explanation`, `is_active`
) VALUES
-- Section 2: Mathematical Ability
(1, 'MATH_01_SEQ', 'What is the next number in the arithmetic sequence: 4, 9, 16, 25, 36, ...?', 2, 'MCQ', 7, 12, 'Easy', 'mathematical_ability', 1, 1, 'The sequence represents consecutive squares: 2^2, 3^2, 4^2, 5^2, 6^2, so next is 7^2 = 49.', 1),
(2, 'MATH_02_ALG', 'If 3x + 15 = 45, what is the value of x?', 2, 'MCQ', 7, 12, 'Easy', 'mathematical_ability', 1, 2, '3x = 45 - 15 = 30 -> x = 10.', 1),
(3, 'MATH_03_PCT', 'A store offers a 20% discount on an item marked at Rs. 1500. What is the final selling price?', 2, 'MCQ', 8, 12, 'Medium', 'mathematical_ability', 1, 3, 'Discount = 20% of 1500 = 300. Selling Price = 1500 - 300 = Rs. 1200.', 1),
(4, 'MATH_04_PROB', 'In how many ways can a committee of 3 students be chosen from a group of 7 candidates?', 2, 'MCQ', 10, 12, 'Hard', 'mathematical_ability', 1, 4, 'Combination 7C3 = (7 * 6 * 5) / (3 * 2 * 1) = 35 ways.', 1),

-- Section 3: Logical Reasoning
(5, 'LOGIC_01_SER', 'Complete the pattern: AZ, BY, CX, DW, ...?', 3, 'MCQ', 7, 12, 'Easy', 'logical_reasoning', 1, 1, 'First letter goes forward (A, B, C, D, E), second letter goes backward (Z, Y, X, W, V). Next is EV.', 1),
(6, 'LOGIC_02_SYLL', 'Statement 1: All roses are flowers. Statement 2: Some flowers fade quickly. Which conclusion logically follows?', 3, 'MCQ', 8, 12, 'Medium', 'logical_reasoning', 1, 2, 'Only some flowers fade quickly; we cannot conclude all roses fade quickly.', 1),
(7, 'LOGIC_03_CODE', 'If CODE is written as DPEF in a cipher, how is SMART written in the same code?', 3, 'MCQ', 7, 12, 'Easy', 'logical_reasoning', 1, 3, 'Each letter is shifted by +1. S->T, M->N, A->B, R->S, T->U: TNBSU.', 1),

-- Section 4: Scientific Thinking
(8, 'SCI_01_EXP', 'When an apple falls from a tree to the ground, which fundamental force is primarily acting upon it?', 4, 'MCQ', 7, 12, 'Easy', 'scientific_reasoning', 1, 1, 'Earth exerts gravitational force pulling objects towards its center.', 1),
(9, 'SCI_02_CHEM', 'What happens to the rate of most chemical reactions when the temperature of reactants is increased?', 4, 'MCQ', 8, 12, 'Medium', 'scientific_reasoning', 1, 2, 'Higher temperature increases kinetic energy and collision frequency, increasing reaction rate.', 1),
(10, 'SCI_03_BIO', 'Which organelle in eukaryotic plant cells is responsible for converting sunlight into chemical glucose via photosynthesis?', 4, 'MCQ', 7, 12, 'Easy', 'scientific_reasoning', 1, 3, 'Chloroplasts contain chlorophyll pigments that capture light for photosynthesis.', 1),

-- Section 5: Problem Solving
(11, 'PS_01_SCENARIO', 'You are leading a science project team and your lab sensor breaks 2 hours before submission. What is your primary response?', 5, 'SCENARIO', 7, 12, 'Medium', 'problem_solving', 1, 1, 'Evaluate the failure point, check for backup components or simulate data, and reassign tasks calmly.', 1),

-- Section 8: Creativity
(12, 'CREAT_01_RATE', 'How frequently do you enjoy experimenting with original sketches, graphic design, writing stories, or building unique craft inventions?', 8, 'RATING', 7, 12, 'Easy', 'creativity', 1, 1, 'Self-reported engagement in creative and divergent pursuits.', 1),

-- Section 9: Digital Ability
(13, 'DIGIT_01_RATE', 'Rate your confidence in writing computer code, building scripts, troubleshooting software, or configuring smart devices:', 9, 'RATING', 7, 12, 'Easy', 'digital_ability', 1, 1, 'Self-reported computational confidence and technology comfort.', 1),

-- Section 13: Interests
(14, 'INT_TECH_RATE', 'How exciting do you find building apps, artificial intelligence, robotics, and futuristic computer technologies?', 13, 'RATING', 7, 12, 'Easy', 'technology_interest', 1, 1, 'Measures intrinsic affinity towards technology careers.', 1),
(15, 'INT_MED_RATE', 'How strongly are you interested in understanding human anatomy, curing medical diseases, and saving lives in healthcare?', 13, 'RATING', 7, 12, 'Easy', 'healthcare_interest', 1, 2, 'Measures intrinsic affinity towards medicine and healthcare.', 1),
(16, 'INT_BIZ_RATE', 'How interested are you in running a business enterprise, investing in financial markets, or managing global products?', 13, 'RATING', 7, 12, 'Easy', 'business_interest', 1, 3, 'Measures intrinsic affinity towards business and financial management.', 1),
(17, 'INT_LAW_RATE', 'How passionate are you about studying laws, debating human rights, constitution, and defending justice in courts?', 13, 'RATING', 7, 12, 'Easy', 'social_interest', 1, 4, 'Measures intrinsic affinity towards jurisprudence and public policy.', 1)
ON DUPLICATE KEY UPDATE `question_text` = VALUES(`question_text`), `explanation` = VALUES(`explanation`);

-- ------------------------------------------------------------
-- 12. Insert Question Options
-- ------------------------------------------------------------
INSERT INTO `question_options` (`id`, `question_id`, `option_text`, `option_value`, `score`, `is_correct`, `display_order`) VALUES
-- Q1: Next Square
(1, 1, '42', '42', 0.00, 0, 1),
(2, 1, '49', '49', 10.00, 1, 2),
(3, 1, '54', '54', 0.00, 0, 3),
(4, 1, '64', '64', 0.00, 0, 4),

-- Q2: 3x + 15 = 45
(5, 2, '5', '5', 0.00, 0, 1),
(6, 2, '10', '10', 10.00, 1, 2),
(7, 2, '15', '15', 0.00, 0, 3),
(8, 2, '30', '30', 0.00, 0, 4),

-- Q3: Discount
(9, 3, 'Rs. 1100', '1100', 0.00, 0, 1),
(10, 3, 'Rs. 1200', '1200', 10.00, 1, 2),
(11, 3, 'Rs. 1300', '1300', 0.00, 0, 3),
(12, 3, 'Rs. 1400', '1400', 0.00, 0, 4),

-- Q4: 7C3
(13, 4, '21', '21', 0.00, 0, 1),
(14, 4, '35', '35', 10.00, 1, 2),
(15, 4, '42', '42', 0.00, 0, 3),
(16, 4, '56', '56', 0.00, 0, 4),

-- Q5: AZ, BY, CX, DW...
(17, 5, 'EV', 'EV', 10.00, 1, 1),
(18, 5, 'EU', 'EU', 0.00, 0, 2),
(19, 5, 'FU', 'FU', 0.00, 0, 3),
(20, 5, 'FV', 'FV', 0.00, 0, 4),

-- Q6: Syllogism
(21, 6, 'All roses fade quickly.', 'all_fade', 0.00, 0, 1),
(22, 6, 'Some roses may fade quickly, but we cannot be certain for all.', 'some_fade', 10.00, 1, 2),
(23, 6, 'No roses fade quickly.', 'no_fade', 0.00, 0, 3),
(24, 6, 'Roses are not flowers.', 'not_flowers', 0.00, 0, 4),

-- Q7: SMART cipher
(25, 7, 'TNBSU', 'TNBSU', 10.00, 1, 1),
(26, 7, 'RLZQS', 'RLZQS', 0.00, 0, 2),
(27, 7, 'TOBTU', 'TOBTU', 0.00, 0, 3),
(28, 7, 'SNBSV', 'SNBSV', 0.00, 0, 4),

-- Q8: Apple Gravity
(29, 8, 'Magnetic Force', 'magnetic', 0.00, 0, 1),
(30, 8, 'Gravitational Force', 'gravity', 10.00, 1, 2),
(31, 8, 'Electrostatic Force', 'electrostatic', 0.00, 0, 3),
(32, 8, 'Nuclear Force', 'nuclear', 0.00, 0, 4),

-- Q9: Reaction Rate
(33, 9, 'The reaction rate increases.', 'increases', 10.00, 1, 1),
(34, 9, 'The reaction rate decreases.', 'decreases', 0.00, 0, 2),
(35, 9, 'The reaction completely stops.', 'stops', 0.00, 0, 3),
(36, 9, 'Temperature has no effect on reaction rates.', 'no_effect', 0.00, 0, 4),

-- Q10: Chloroplast
(37, 10, 'Mitochondria', 'mitochondria', 0.00, 0, 1),
(38, 10, 'Chloroplasts', 'chloroplasts', 10.00, 1, 2),
(39, 10, 'Endoplasmic Reticulum', 'er', 0.00, 0, 3),
(40, 10, 'Golgi Apparatus', 'golgi', 0.00, 0, 4),

-- Q11: Scenario
(41, 11, 'Panic and abandon the project submission.', 'panic', 1.00, 0, 1),
(42, 11, 'Troubleshoot the sensor circuit, inspect wires, test backup data, and update the report presentation.', 'troubleshoot', 10.00, 1, 2),
(43, 11, 'Blame a team member for the hardware failure.', 'blame', 0.00, 0, 3),
(44, 11, 'Wait passively for someone else to fix the hardware.', 'wait', 2.00, 0, 4),

-- Q12: Creativity Rating (1-5)
(45, 12, '1 - Rare / Never', '1', 2.00, 0, 1),
(46, 12, '2 - Occasionally', '2', 4.00, 0, 2),
(47, 12, '3 - Moderate', '3', 6.00, 0, 3),
(48, 12, '4 - Frequent', '4', 8.00, 0, 4),
(49, 12, '5 - Passionately / Constant', '5', 10.00, 1, 5),

-- Q13: Digital Ability Rating (1-5)
(50, 13, '1 - Basic / Limited', '1', 2.00, 0, 1),
(51, 13, '2 - Familiar with Office/Browsing', '2', 4.00, 0, 2),
(52, 13, '3 - Comfortable troubleshooting apps', '3', 6.00, 0, 3),
(53, 13, '4 - Basic coding & automation skills', '4', 8.00, 0, 4),
(54, 13, '5 - Advanced programming & tech projects', '5', 10.00, 1, 5),

-- Q14-Q17: Interest Ratings (1-5)
(55, 14, '1 - Not Interested', '1', 2.00, 0, 1),
(56, 14, '2 - Slightly Interested', '2', 4.00, 0, 2),
(57, 14, '3 - Moderately Interested', '3', 6.00, 0, 3),
(58, 14, '4 - Very Interested', '4', 8.00, 0, 4),
(59, 14, '5 - Extremely Passionate', '5', 10.00, 1, 5),

(60, 15, '1 - Not Interested', '1', 2.00, 0, 1),
(61, 15, '2 - Slightly Interested', '2', 4.00, 0, 2),
(62, 15, '3 - Moderately Interested', '3', 6.00, 0, 3),
(63, 15, '4 - Very Interested', '4', 8.00, 0, 4),
(64, 15, '5 - Extremely Passionate', '5', 10.00, 1, 5),

(65, 16, '1 - Not Interested', '1', 2.00, 0, 1),
(66, 16, '2 - Slightly Interested', '2', 4.00, 0, 2),
(67, 16, '3 - Moderately Interested', '3', 6.00, 0, 3),
(68, 16, '4 - Very Interested', '4', 8.00, 0, 4),
(69, 16, '5 - Extremely Passionate', '5', 10.00, 1, 5),

(70, 17, '1 - Not Interested', '1', 2.00, 0, 1),
(71, 17, '2 - Slightly Interested', '2', 4.00, 0, 2),
(72, 17, '3 - Moderately Interested', '3', 6.00, 0, 3),
(73, 17, '4 - Very Interested', '4', 8.00, 0, 4),
(74, 17, '5 - Extremely Passionate', '5', 10.00, 1, 5)
ON DUPLICATE KEY UPDATE `option_text` = VALUES(`option_text`), `score` = VALUES(`score`);

-- ------------------------------------------------------------
-- 13. Insert Default Users, Students & Academic Records
-- ------------------------------------------------------------
-- Password for all seed accounts: Admin@123 / Student@123 (scrypt / bcrypt hashed)
-- Hashed representation: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L656q0cx7E9f2ba
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'admin', 'admin@careerguidance.edu', '$2b$12$1uTq9qJ3Y8m07X6yE2wEPePqC89F.6D2uVzZ0w2a2E1b9K0P4g9k.', 'admin', NOW()),
(2, 'rahul_class8', 'rahul.sharma@school.edu', '$2b$12$1uTq9qJ3Y8m07X6yE2wEPePqC89F.6D2uVzZ0w2a2E1b9K0P4g9k.', 'student', NOW()),
(3, 'ananya_class10', 'ananya.iyer@school.edu', '$2b$12$1uTq9qJ3Y8m07X6yE2wEPePqC89F.6D2uVzZ0w2a2E1b9K0P4g9k.', 'student', NOW()),
(4, 'aravind_class12', 'aravind.nair@school.edu', '$2b$12$1uTq9qJ3Y8m07X6yE2wEPePqC89F.6D2uVzZ0w2a2E1b9K0P4g9k.', 'student', NOW())
ON DUPLICATE KEY UPDATE `email` = VALUES(`email`);

INSERT INTO `students` (
    `id`, `user_id`, `student_code`, `first_name`, `last_name`,
    `age`, `gender`, `class_level`, `board`, `medium`,
    `academic_year`, `stream`, `created_at`
) VALUES
(1, 2, 'STU-2026-0001', 'Rahul', 'Sharma', 13, 'Male', 8, 'CBSE', 'English', '2026-2027', 'General', NOW()),
(2, 3, 'STU-2026-0002', 'Ananya', 'Iyer', 15, 'Female', 10, 'ICSE', 'English', '2026-2027', 'General', NOW()),
(3, 4, 'STU-2026-0003', 'Aravind', 'Nair', 17, 'Male', 12, 'State Board', 'English', '2026-2027', 'Science-PCM', NOW())
ON DUPLICATE KEY UPDATE `student_code` = VALUES(`student_code`);

INSERT INTO `academic_scores` (
    `id`, `student_id`,
    `mathematics_score`, `science_score`, `physics_score`, `chemistry_score`,
    `computer_science_score`, `english_score`, `social_science_score`,
    `overall_percentage`, `created_at`
) VALUES
(1, 1, 88.00, 85.00, NULL, NULL, 90.00, 82.00, 78.00, 84.60, NOW()),
(2, 2, 94.00, 92.00, NULL, NULL, 96.00, 89.00, 84.00, 91.00, NOW()),
(3, 3, 91.00, NULL, 89.00, 86.00, 95.00, 85.00, NULL, 89.20, NOW())
ON DUPLICATE KEY UPDATE `overall_percentage` = VALUES(`overall_percentage`);

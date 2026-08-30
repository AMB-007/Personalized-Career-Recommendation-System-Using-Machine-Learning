"""
Build the Complete Unified All-In-One MySQL Database Setup Script.
Generates: database/setup.sql and setup.sql (in root folder)
"""

import io
import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def build_unified_sql():
    raw_setup = (BASE_DIR / "database" / "setup.sql").read_text(encoding='utf-8')
    raw_questions = (BASE_DIR / "database" / "questions_seed.sql").read_text(encoding='utf-8')

    out = []

    # 1. HEADER
    out.append("-- ============================================================")
    out.append("-- COMPLETE UNIFIED ALL-IN-ONE DATABASE INITIALIZATION SCRIPT")
    out.append("-- Project: Personalized Career Recommendation System Using ML (PathFinder)")
    out.append("-- Database Server: MySQL 8.x / MariaDB / MySQL Workbench Compatible")
    out.append("-- Target Database: career_recommendation_db")
    out.append("-- Contains: Complete DDL Schema (18 Tables) + Complete Seed Data")
    out.append("--           (Demo Users, 19 Sections, 413 Questions, 1,805 Options,")
    out.append("--            33 Domains, 389 Subdomains, 466 Clusters, 2,259 Careers,")
    out.append("--            Skills, Subjects, Education Milestones & Career Ladders)")
    out.append("-- ============================================================\n")

    out.append("CREATE DATABASE IF NOT EXISTS `career_recommendation_db`")
    out.append("CHARACTER SET utf8mb4")
    out.append("COLLATE utf8mb4_unicode_ci;\n")

    out.append("USE `career_recommendation_db`;\n")
    out.append("SET NAMES utf8mb4;")
    out.append("SET FOREIGN_KEY_CHECKS = 0;\n")

    # 2. DROP TABLES
    out.append("-- ------------------------------------------------------------")
    out.append("-- Drop existing tables in reverse dependency order")
    out.append("-- ------------------------------------------------------------")
    drop_tables = [
        "career_recommendations", "career_pathways", "career_education",
        "career_subjects", "career_skills", "careers", "career_clusters",
        "career_subdomains", "career_domains", "assessment_scores",
        "student_answers", "assessment_sessions", "question_options",
        "questions", "question_sections", "academic_scores", "students", "users",
        "learning_resources", "resources", "recommendation_feedback", "temp_recommendations"
    ]
    for dt in drop_tables:
        out.append(f"DROP TABLE IF EXISTS `{dt}`;")
    out.append("SET FOREIGN_KEY_CHECKS = 1;\n")

    # 3. DDL DEFINITIONS (18 TABLES)
    out.append("-- ============================================================")
    out.append("-- 1. DDL TABLE DEFINITIONS (18 ACTIVE NORMALIZED TABLES)")
    out.append("-- ============================================================\n")

    # 1.1 users
    out.append("""-- 1.1 Table: users
CREATE TABLE `users` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` ENUM('student', 'admin') NOT NULL DEFAULT 'student',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_users_role` (`role`),
    INDEX `idx_users_email` (`email`),
    INDEX `idx_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.2 students
    out.append("""-- 1.2 Table: students
CREATE TABLE `students` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `student_code` VARCHAR(50) NOT NULL UNIQUE,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NULL,
    `age` TINYINT UNSIGNED NULL,
    `gender` VARCHAR(30) NULL,
    `class_level` TINYINT UNSIGNED NOT NULL,
    `board` VARCHAR(100) NULL DEFAULT 'CBSE',
    `medium` VARCHAR(50) NULL DEFAULT 'English',
    `stream` VARCHAR(100) NULL DEFAULT 'General',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_students_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    INDEX `idx_students_class` (`class_level`),
    INDEX `idx_students_stream` (`stream`),
    INDEX `idx_students_code` (`student_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.3 academic_scores
    out.append("""-- 1.3 Table: academic_scores (17 School Subjects + Overall Percentage)
CREATE TABLE `academic_scores` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `student_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `mathematics_score` DECIMAL(5,2) NULL,
    `science_score` DECIMAL(5,2) NULL,
    `physics_score` DECIMAL(5,2) NULL,
    `chemistry_score` DECIMAL(5,2) NULL,
    `biology_score` DECIMAL(5,2) NULL,
    `computer_science_score` DECIMAL(5,2) NULL,
    `english_score` DECIMAL(5,2) NULL,
    `malayalam_score` DECIMAL(5,2) NULL,
    `hindi_score` DECIMAL(5,2) NULL,
    `social_science_score` DECIMAL(5,2) NULL,
    `history_score` DECIMAL(5,2) NULL,
    `geography_score` DECIMAL(5,2) NULL,
    `political_science_score` DECIMAL(5,2) NULL,
    `economics_score` DECIMAL(5,2) NULL,
    `accountancy_score` DECIMAL(5,2) NULL,
    `business_studies_score` DECIMAL(5,2) NULL,
    `psychology_score` DECIMAL(5,2) NULL,
    `overall_percentage` DECIMAL(5,2) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_academic_scores_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    INDEX `idx_academic_student` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.4 question_sections
    out.append("""-- 1.4 Table: question_sections
CREATE TABLE `question_sections` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NULL,
    `display_order` INT NOT NULL DEFAULT 0,
    `is_active` BOOLEAN DEFAULT TRUE,
    INDEX `idx_sections_order` (`display_order`),
    INDEX `idx_sections_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.5 questions
    out.append("""-- 1.5 Table: questions
CREATE TABLE `questions` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `question_code` VARCHAR(50) NOT NULL UNIQUE,
    `question_text` TEXT NOT NULL,
    `section_id` INT NOT NULL,
    `question_type` ENUM('rating_scale', 'mcq', 'likert_5', 'likert_7') NOT NULL DEFAULT 'mcq',
    `class_min` TINYINT UNSIGNED NOT NULL DEFAULT 7,
    `class_max` TINYINT UNSIGNED NOT NULL DEFAULT 12,
    `difficulty` ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'medium',
    `skill_category` VARCHAR(100) NULL,
    `stream_specific` VARCHAR(50) NULL,
    `is_required` BOOLEAN DEFAULT TRUE,
    `display_order` INT NOT NULL DEFAULT 0,
    `explanation` TEXT NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_questions_section` FOREIGN KEY (`section_id`) REFERENCES `question_sections` (`id`) ON DELETE RESTRICT,
    INDEX `idx_questions_code` (`question_code`),
    INDEX `idx_questions_class` (`class_min`, `class_max`),
    INDEX `idx_questions_section` (`section_id`),
    INDEX `idx_questions_skill` (`skill_category`),
    INDEX `idx_questions_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.6 question_options
    out.append("""-- 1.6 Table: question_options
CREATE TABLE `question_options` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `question_id` BIGINT UNSIGNED NOT NULL,
    `option_text` VARCHAR(500) NOT NULL,
    `option_value` VARCHAR(100) NULL,
    `score` DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    `is_correct` BOOLEAN NULL,
    `display_order` INT NOT NULL DEFAULT 0,
    CONSTRAINT `fk_options_question` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
    INDEX `idx_options_question` (`question_id`),
    INDEX `idx_options_order` (`display_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.7 assessment_sessions
    out.append("""-- 1.7 Table: assessment_sessions
CREATE TABLE `assessment_sessions` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `student_id` BIGINT UNSIGNED NOT NULL,
    `status` ENUM('in_progress', 'completed', 'expired') NOT NULL DEFAULT 'in_progress',
    `started_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `completed_at` TIMESTAMP NULL,
    `current_question` INT DEFAULT 1,
    `completion_percentage` DECIMAL(5,2) DEFAULT 0.00,
    `selected_question_ids` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_sessions_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    INDEX `idx_sessions_student` (`student_id`),
    INDEX `idx_sessions_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.8 student_answers
    out.append("""-- 1.8 Table: student_answers
CREATE TABLE `student_answers` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `assessment_id` BIGINT UNSIGNED NOT NULL,
    `question_id` BIGINT UNSIGNED NOT NULL,
    `selected_option_id` BIGINT UNSIGNED NULL,
    `selected_option` TEXT NULL,
    `answer_text` TEXT NULL,
    `numeric_value` DECIMAL(8,3) NULL,
    `time_taken_seconds` INT NULL,
    `answered_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_answers_session` FOREIGN KEY (`assessment_id`) REFERENCES `assessment_sessions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_answers_question` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_answers_option` FOREIGN KEY (`selected_option_id`) REFERENCES `question_options` (`id`) ON DELETE CASCADE,
    INDEX `idx_answers_session` (`assessment_id`),
    INDEX `idx_answers_question` (`question_id`),
    UNIQUE KEY `uq_session_question` (`assessment_id`, `question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.9 assessment_scores
    out.append("""-- 1.9 Table: assessment_scores
CREATE TABLE `assessment_scores` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `assessment_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `mathematical_ability` DECIMAL(5,2) NULL,
    `logical_reasoning` DECIMAL(5,2) NULL,
    `scientific_reasoning` DECIMAL(5,2) NULL,
    `problem_solving` DECIMAL(5,2) NULL,
    `analytical_ability` DECIMAL(5,2) NULL,
    `communication` DECIMAL(5,2) NULL,
    `creativity` DECIMAL(5,2) NULL,
    `digital_ability` DECIMAL(5,2) NULL,
    `learning_ability` DECIMAL(5,2) NULL,
    `memory` DECIMAL(5,2) NULL,
    `observation` DECIMAL(5,2) NULL,
    `spatial_ability` DECIMAL(5,2) NULL,
    `practical_ability` DECIMAL(5,2) NULL,
    `teamwork` DECIMAL(5,2) NULL,
    `leadership` DECIMAL(5,2) NULL,
    `technology_interest` DECIMAL(5,2) NULL,
    `science_interest` DECIMAL(5,2) NULL,
    `healthcare_interest` DECIMAL(5,2) NULL,
    `business_interest` DECIMAL(5,2) NULL,
    `creative_interest` DECIMAL(5,2) NULL,
    `research_interest` DECIMAL(5,2) NULL,
    `social_interest` DECIMAL(5,2) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_scores_session` FOREIGN KEY (`assessment_id`) REFERENCES `assessment_sessions` (`id`) ON DELETE CASCADE,
    INDEX `idx_scores_session` (`assessment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.10 career_domains
    out.append("""-- 1.10 Table: career_domains
CREATE TABLE `career_domains` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `domain_name` VARCHAR(150) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `icon` VARCHAR(100) DEFAULT 'bi-briefcase',
    `display_order` INT NOT NULL DEFAULT 0,
    `is_active` BOOLEAN DEFAULT TRUE,
    INDEX `idx_domains_name` (`domain_name`),
    INDEX `idx_domains_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.11 career_subdomains
    out.append("""-- 1.11 Table: career_subdomains
CREATE TABLE `career_subdomains` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `domain_id` INT NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,
    CONSTRAINT `fk_subdomains_domain` FOREIGN KEY (`domain_id`) REFERENCES `career_domains` (`id`) ON DELETE RESTRICT,
    INDEX `idx_subdomains_name` (`name`),
    INDEX `idx_subdomains_domain` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.12 career_clusters
    out.append("""-- 1.12 Table: career_clusters
CREATE TABLE `career_clusters` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `subdomain_id` INT NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,
    CONSTRAINT `fk_clusters_subdomain` FOREIGN KEY (`subdomain_id`) REFERENCES `career_subdomains` (`id`) ON DELETE SET NULL,
    INDEX `idx_clusters_name` (`name`),
    INDEX `idx_clusters_subdomain` (`subdomain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.13 careers (16 Columns - Cleaned Normalized Master)
    out.append("""-- 1.13 Table: careers (16 Columns Master Entity)
CREATE TABLE `careers` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_code` VARCHAR(50) NOT NULL UNIQUE,
    `career_name` VARCHAR(200) NOT NULL,
    `domain_id` INT NOT NULL,
    `subdomain_id` INT NULL,
    `cluster_id` INT NULL,
    `description` TEXT NULL,
    `minimum_education` VARCHAR(150) NULL,
    `typical_education` VARCHAR(150) NULL,
    `work_environment` VARCHAR(200) NULL,
    `work_style` VARCHAR(200) NULL,
    `entry_level_role` VARCHAR(200) NULL,
    `advanced_role` VARCHAR(200) NULL,
    `related_careers` TEXT NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_careers_domain` FOREIGN KEY (`domain_id`) REFERENCES `career_domains` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_careers_subdomain` FOREIGN KEY (`subdomain_id`) REFERENCES `career_subdomains` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_careers_cluster` FOREIGN KEY (`cluster_id`) REFERENCES `career_clusters` (`id`) ON DELETE SET NULL,
    INDEX `idx_careers_name` (`career_name`),
    INDEX `idx_careers_code` (`career_code`),
    INDEX `idx_careers_domain` (`domain_id`),
    INDEX `idx_careers_cluster` (`cluster_id`),
    INDEX `idx_careers_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.14 career_skills
    out.append("""-- 1.14 Table: career_skills
CREATE TABLE `career_skills` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `skill_name` VARCHAR(150) NOT NULL,
    `importance_level` TINYINT UNSIGNED NOT NULL DEFAULT 4,
    `importance_label` VARCHAR(30) DEFAULT 'High',
    CONSTRAINT `fk_skills_career` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`) ON DELETE CASCADE,
    INDEX `idx_skills_career` (`career_id`),
    INDEX `idx_skills_name` (`skill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.15 career_subjects
    out.append("""-- 1.15 Table: career_subjects
CREATE TABLE `career_subjects` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `subject_name` VARCHAR(150) NOT NULL,
    `importance_level` TINYINT UNSIGNED NOT NULL DEFAULT 4,
    `importance_label` VARCHAR(30) DEFAULT 'High',
    CONSTRAINT `fk_subjects_career` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`) ON DELETE CASCADE,
    INDEX `idx_subjects_career` (`career_id`),
    INDEX `idx_subjects_name` (`subject_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.16 career_education
    out.append("""-- 1.16 Table: career_education
CREATE TABLE `career_education` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `education_level` VARCHAR(150) NOT NULL,
    `degree_name` VARCHAR(200) NOT NULL,
    `description` TEXT NULL,
    `sequence_order` INT NOT NULL DEFAULT 1,
    CONSTRAINT `fk_education_career` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`) ON DELETE CASCADE,
    INDEX `idx_education_career` (`career_id`),
    INDEX `idx_education_order` (`sequence_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.17 career_pathways
    out.append("""-- 1.17 Table: career_pathways
CREATE TABLE `career_pathways` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `stage_number` INT NOT NULL DEFAULT 1,
    `stage_name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,
    CONSTRAINT `fk_pathways_career` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`) ON DELETE CASCADE,
    INDEX `idx_pathways_career` (`career_id`),
    INDEX `idx_pathways_stage` (`stage_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 1.18 career_recommendations
    out.append("""-- 1.18 Table: career_recommendations
CREATE TABLE `career_recommendations` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `assessment_id` BIGINT UNSIGNED NOT NULL,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `rank_position` INT NOT NULL DEFAULT 1,
    `score` DECIMAL(8,5) NULL,
    `recommendation_reason` TEXT NULL,
    `strengths` TEXT NULL,
    `skill_gaps` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_recs_session` FOREIGN KEY (`assessment_id`) REFERENCES `assessment_sessions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_recs_career` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`) ON DELETE CASCADE,
    INDEX `idx_recs_session` (`assessment_id`),
    INDEX `idx_recs_rank` (`rank_position`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # 4. SEED DATA SECTION
    out.append("-- ============================================================")
    out.append("-- 2. INITIAL SEED DATA INSERTIONS")
    out.append("-- ============================================================\n")

    # 4.1 Users & Students
    out.append("""-- 2.1 Demo Users (admin: Admin@123, rahul: Password@123)
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `updated_at`) VALUES 
(1, 'admin', 'admin@pathfinder.edu', 'scrypt:32768:8:1$7N03XgIu$c87d4683d73507cba57a3e8ecda97e7428807d9f7823b123864da5e6563604f5e7149a4f494877e80a031a0eb3f1737e44a42b9e67d264ef5f838a1656f7efaa', 'admin', '2026-08-29 09:00:00', '2026-08-29 09:00:00'),
(2, 'rahul_sharma_10', 'rahul.sharma@example.com', 'scrypt:32768:8:1$7N03XgIu$c87d4683d73507cba57a3e8ecda97e7428807d9f7823b123864da5e6563604f5e7149a4f494877e80a031a0eb3f1737e44a42b9e67d264ef5f838a1656f7efaa', 'student', '2026-08-29 09:00:00', '2026-08-29 09:00:00');

-- 2.2 Demo Student Record
INSERT INTO `students` (`id`, `user_id`, `student_code`, `first_name`, `last_name`, `age`, `gender`, `class_level`, `board`, `medium`, `stream`, `created_at`, `updated_at`) VALUES 
(1, 2, 'STU-10-0001', 'Rahul', 'Sharma', 15, 'Male', 10, 'CBSE', 'English', 'General', '2026-08-29 09:00:00', '2026-08-29 09:00:00');

-- 2.3 Demo Academic Scores across 17 Subjects
INSERT INTO `academic_scores` (`id`, `student_id`, `mathematics_score`, `science_score`, `physics_score`, `chemistry_score`, `biology_score`, `computer_science_score`, `english_score`, `malayalam_score`, `hindi_score`, `social_science_score`, `history_score`, `geography_score`, `political_science_score`, `economics_score`, `accountancy_score`, `business_studies_score`, `psychology_score`, `overall_percentage`, `created_at`) VALUES 
(1, 1, 88.00, 85.00, NULL, NULL, NULL, 92.00, 80.00, NULL, 78.00, 84.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 84.50, '2026-08-29 09:00:00');
""")

    # 4.2 Sections, Questions & Options
    # Extract from raw_setup or raw_questions
    print("Extracting question sections, questions and options...")
    raw_lines = raw_setup.split('\n')
    
    current_table = None
    for line in raw_lines:
        line_s = line.strip()
        if not line_s.startswith("INSERT INTO"):
            continue
        
        # Check target table
        if "`question_sections`" in line_s or "question_sections" in line_s:
            out.append(line_s)
        elif "`questions`" in line_s or "questions (" in line_s:
            out.append(line_s)
        elif "`question_options`" in line_s or "question_options (" in line_s:
            out.append(line_s)
        elif "`career_domains`" in line_s:
            out.append(line_s)
        elif "`career_subdomains`" in line_s:
            out.append(line_s)
        elif "`career_clusters`" in line_s:
            out.append(line_s)
        elif "`careers`" in line_s:
            # Transform careers line from 18 cols to 16 cols
            # Pattern: INSERT INTO `careers` (...) VALUES (...);
            m = re.match(r'INSERT INTO `careers` \((.*?)\) VALUES \((.*?)\);', line_s)
            if m:
                cols_str, vals_str = m.group(1), m.group(2)
                # Parse values safely
                reader = csv.reader(io.StringIO(vals_str), delimiter=',', quotechar="'", skipinitialspace=True)
                vals = next(reader)
                if len(vals) == 19:
                    # 19 values: id, code, name, dom, sub, clu, desc, min_edu, typ_edu, pref_sub(9), work_env, work_style, pathway(12), entry, adv, rel, is_active, created, updated
                    new_vals = [v for i, v in enumerate(vals) if i not in (9, 12)]
                    # Reconstruct SQL string
                    escaped_vals = []
                    for v in new_vals:
                        if v.isdigit() or (v.replace('.', '', 1).isdigit() and '.' in v):
                            escaped_vals.append(v)
                        elif v.upper() in ('TRUE', 'FALSE', 'NULL'):
                            escaped_vals.append(v)
                        else:
                            clean_v = v.replace("'", "\\'")
                            escaped_vals.append(f"'{clean_v}'")
                    
                    cleaned_line = f"INSERT INTO `careers` (`id`, `career_code`, `career_name`, `domain_id`, `subdomain_id`, `cluster_id`, `description`, `minimum_education`, `typical_education`, `work_environment`, `work_style`, `entry_level_role`, `advanced_role`, `related_careers`, `is_active`, `created_at`, `updated_at`) VALUES ({', '.join(escaped_vals)});"
                    out.append(cleaned_line)
                else:
                    out.append(line_s)
            else:
                out.append(line_s)
        elif "`career_skills`" in line_s:
            out.append(line_s)
        elif "`career_subjects`" in line_s:
            out.append(line_s)
        elif "`career_education`" in line_s:
            out.append(line_s)
        elif "`career_pathways`" in line_s:
            out.append(line_s)

    out.append("\n-- ------------------------------------------------------------")
    out.append("-- Verification Summary Query")
    out.append("-- ------------------------------------------------------------")
    out.append("SELECT 'Database Setup Completed Successfully!' AS status,")
    out.append("       (SELECT COUNT(*) FROM `career_domains`) AS total_domains,")
    out.append("       (SELECT COUNT(*) FROM `career_subdomains`) AS total_subdomains,")
    out.append("       (SELECT COUNT(*) FROM `career_clusters`) AS total_clusters,")
    out.append("       (SELECT COUNT(*) FROM `careers`) AS total_careers,")
    out.append("       (SELECT COUNT(*) FROM `questions`) AS total_questions,")
    out.append("       (SELECT COUNT(*) FROM `question_options`) AS total_options;")

    final_content = '\n'.join(out) + '\n'

    # Save to both database/setup.sql and setup.sql (root)
    paths = [
        BASE_DIR / "database" / "setup.sql",
        BASE_DIR / "setup.sql"
    ]
    for p in paths:
        p.write_text(final_content, encoding='utf-8')
        print(f"Written {len(out)} lines to: {p.resolve()} ({p.stat().st_size:,} bytes)")

if __name__ == '__main__':
    build_unified_sql()

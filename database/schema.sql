-- ============================================================
-- Career Recommendation System - MySQL Workbench Database Schema
-- Database Server: MySQL 8.x
-- Tool: MySQL Workbench Compatible
-- Database Name: career_recommendation_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS `career_recommendation_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `career_recommendation_db`;

-- Drop existing tables in reverse dependency order to prevent foreign key errors
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `learning_resources`;
DROP TABLE IF EXISTS `career_recommendations`;
DROP TABLE IF EXISTS `career_pathways`;
DROP TABLE IF EXISTS `career_education`;
DROP TABLE IF EXISTS `career_subjects`;
DROP TABLE IF EXISTS `career_skills`;
DROP TABLE IF EXISTS `careers`;
DROP TABLE IF EXISTS `career_clusters`;
DROP TABLE IF EXISTS `career_subdomains`;
DROP TABLE IF EXISTS `career_domains`;
DROP TABLE IF EXISTS `assessment_scores`;
DROP TABLE IF EXISTS `student_answers`;
DROP TABLE IF EXISTS `assessment_sessions`;
DROP TABLE IF EXISTS `question_options`;
DROP TABLE IF EXISTS `questions`;
DROP TABLE IF EXISTS `question_sections`;
DROP TABLE IF EXISTS `academic_scores`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `users`;
SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- 1. Table: users
-- ------------------------------------------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 2. Table: students
-- ------------------------------------------------------------
CREATE TABLE `students` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `student_code` VARCHAR(50) NOT NULL UNIQUE,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NULL,
    `age` TINYINT UNSIGNED NULL,
    `gender` VARCHAR(30) NULL,
    `class_level` TINYINT UNSIGNED NOT NULL,
    `board` VARCHAR(100) NULL,
    `medium` VARCHAR(50) NULL,
    `academic_year` VARCHAR(20) NULL,
    `stream` VARCHAR(100) NULL DEFAULT 'General',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT `fk_students_user`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`id`)
        ON DELETE CASCADE,

    CONSTRAINT `chk_student_class`
        CHECK (`class_level` BETWEEN 7 AND 12),

    INDEX `idx_students_user_id` (`user_id`),
    INDEX `idx_students_class` (`class_level`),
    INDEX `idx_students_stream` (`stream`),
    INDEX `idx_students_board` (`board`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 3. Table: academic_scores
-- ------------------------------------------------------------
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

    CONSTRAINT `fk_academic_student`
        FOREIGN KEY (`student_id`)
        REFERENCES `students` (`id`)
        ON DELETE CASCADE,

    INDEX `idx_academic_student` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 4. Table: question_sections
-- ------------------------------------------------------------
CREATE TABLE `question_sections` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `display_order` INT NOT NULL DEFAULT 1,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX `idx_sections_order` (`display_order`),
    INDEX `idx_sections_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 5. Table: questions
-- ------------------------------------------------------------
CREATE TABLE `questions` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `question_code` VARCHAR(50) NOT NULL UNIQUE,
    `question_text` TEXT NOT NULL,
    `section_id` INT UNSIGNED NOT NULL,
    `question_type` ENUM(
        'MCQ',
        'MULTI_SELECT',
        'RATING',
        'SCENARIO',
        'RANKING'
    ) NOT NULL DEFAULT 'MCQ',
    `class_min` TINYINT UNSIGNED NOT NULL DEFAULT 7,
    `class_max` TINYINT UNSIGNED NOT NULL DEFAULT 12,
    `difficulty` ENUM('Easy', 'Medium', 'Hard') DEFAULT 'Medium',
    `skill_category` VARCHAR(100) NULL,
    `stream_specific` VARCHAR(50) DEFAULT 'All',
    `is_required` BOOLEAN DEFAULT TRUE,
    `display_order` INT DEFAULT 0,
    `explanation` TEXT NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_questions_section`
        FOREIGN KEY (`section_id`)
        REFERENCES `question_sections` (`id`)
        ON DELETE RESTRICT,

    CONSTRAINT `chk_question_class`
        CHECK (
            `class_min` BETWEEN 7 AND 12
            AND `class_max` BETWEEN 7 AND 12
            AND `class_min` <= `class_max`
        ),

    INDEX `idx_questions_section` (`section_id`),
    INDEX `idx_questions_class_min` (`class_min`),
    INDEX `idx_questions_class_max` (`class_max`),
    INDEX `idx_questions_skill` (`skill_category`),
    INDEX `idx_questions_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 6. Table: question_options
-- ------------------------------------------------------------
CREATE TABLE `question_options` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `question_id` BIGINT UNSIGNED NOT NULL,
    `option_text` VARCHAR(500) NOT NULL,
    `option_value` VARCHAR(100) NULL,
    `score` DECIMAL(6,2) DEFAULT 0.00,
    `is_correct` BOOLEAN DEFAULT FALSE,
    `display_order` INT DEFAULT 0,

    CONSTRAINT `fk_options_question`
        FOREIGN KEY (`question_id`)
        REFERENCES `questions` (`id`)
        ON DELETE CASCADE,

    INDEX `idx_options_question_id` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 7. Table: assessment_sessions
-- ------------------------------------------------------------
CREATE TABLE `assessment_sessions` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `student_id` BIGINT UNSIGNED NOT NULL,
    `status` ENUM(
        'not_started',
        'in_progress',
        'completed',
        'abandoned'
    ) DEFAULT 'not_started',
    `started_at` DATETIME NULL,
    `completed_at` DATETIME NULL,
    `current_question` INT DEFAULT 0,
    `completion_percentage` DECIMAL(5,2) DEFAULT 0.00,
    `selected_question_ids` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_assessment_student`
        FOREIGN KEY (`student_id`)
        REFERENCES `students` (`id`)
        ON DELETE CASCADE,

    INDEX `idx_assessment_student_id` (`student_id`),
    INDEX `idx_assessment_status` (`status`),
    INDEX `idx_assessment_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 8. Table: student_answers
-- ------------------------------------------------------------
CREATE TABLE `student_answers` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `assessment_id` BIGINT UNSIGNED NOT NULL,
    `question_id` BIGINT UNSIGNED NOT NULL,
    `selected_option_id` BIGINT UNSIGNED NULL,
    `selected_option` TEXT NULL,
    `answer_text` TEXT NULL,
    `numeric_value` DECIMAL(10,2) NULL,
    `time_taken_seconds` INT UNSIGNED NULL DEFAULT 0,
    `answered_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_answers_assessment`
        FOREIGN KEY (`assessment_id`)
        REFERENCES `assessment_sessions` (`id`)
        ON DELETE CASCADE,

    CONSTRAINT `fk_answers_question`
        FOREIGN KEY (`question_id`)
        REFERENCES `questions` (`id`)
        ON DELETE RESTRICT,

    CONSTRAINT `fk_answers_option`
        FOREIGN KEY (`selected_option_id`)
        REFERENCES `question_options` (`id`)
        ON DELETE SET NULL,

    CONSTRAINT `uq_assessment_question`
        UNIQUE (`assessment_id`, `question_id`),

    INDEX `idx_answers_assessment` (`assessment_id`),
    INDEX `idx_answers_question` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 9. Table: assessment_scores
-- ------------------------------------------------------------
CREATE TABLE `assessment_scores` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `assessment_id` BIGINT UNSIGNED NOT NULL UNIQUE,

    `mathematical_ability` DECIMAL(6,2) DEFAULT 0.00,
    `logical_reasoning` DECIMAL(6,2) DEFAULT 0.00,
    `scientific_reasoning` DECIMAL(6,2) DEFAULT 0.00,
    `problem_solving` DECIMAL(6,2) DEFAULT 0.00,
    `analytical_ability` DECIMAL(6,2) DEFAULT 0.00,
    `communication` DECIMAL(6,2) DEFAULT 0.00,
    `creativity` DECIMAL(6,2) DEFAULT 0.00,
    `digital_ability` DECIMAL(6,2) DEFAULT 0.00,
    `learning_ability` DECIMAL(6,2) DEFAULT 0.00,
    `memory` DECIMAL(6,2) DEFAULT 0.00,
    `observation` DECIMAL(6,2) DEFAULT 0.00,
    `spatial_ability` DECIMAL(6,2) DEFAULT 0.00,
    `practical_ability` DECIMAL(6,2) DEFAULT 0.00,
    `teamwork` DECIMAL(6,2) DEFAULT 0.00,
    `leadership` DECIMAL(6,2) DEFAULT 0.00,

    `technology_interest` DECIMAL(6,2) DEFAULT 0.00,
    `science_interest` DECIMAL(6,2) DEFAULT 0.00,
    `healthcare_interest` DECIMAL(6,2) DEFAULT 0.00,
    `business_interest` DECIMAL(6,2) DEFAULT 0.00,
    `creative_interest` DECIMAL(6,2) DEFAULT 0.00,
    `research_interest` DECIMAL(6,2) DEFAULT 0.00,
    `social_interest` DECIMAL(6,2) DEFAULT 0.00,

    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_scores_assessment`
        FOREIGN KEY (`assessment_id`)
        REFERENCES `assessment_sessions` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 10. Table: career_domains
-- ------------------------------------------------------------
CREATE TABLE `career_domains` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `domain_name` VARCHAR(150) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `icon` VARCHAR(100) DEFAULT 'bi-briefcase',
    `display_order` INT DEFAULT 0,
    `is_active` BOOLEAN DEFAULT TRUE,
    INDEX `idx_domains_order` (`display_order`),
    INDEX `idx_domains_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 11. Table: career_subdomains
-- ------------------------------------------------------------
CREATE TABLE `career_subdomains` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `domain_id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,

    CONSTRAINT `fk_subdomain_domain`
        FOREIGN KEY (`domain_id`)
        REFERENCES `career_domains` (`id`)
        ON DELETE CASCADE,

    UNIQUE KEY `uq_domain_subdomain` (`domain_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 12. Table: career_clusters
-- ------------------------------------------------------------
CREATE TABLE `career_clusters` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `subdomain_id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,

    CONSTRAINT `fk_cluster_subdomain`
        FOREIGN KEY (`subdomain_id`)
        REFERENCES `career_subdomains` (`id`)
        ON DELETE CASCADE,

    UNIQUE KEY `uq_subdomain_cluster` (`subdomain_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 13. Table: careers
-- ------------------------------------------------------------
CREATE TABLE `careers` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_code` VARCHAR(50) NOT NULL UNIQUE,
    `career_name` VARCHAR(200) NOT NULL,
    `domain_id` INT UNSIGNED NOT NULL,
    `subdomain_id` INT UNSIGNED NULL,
    `cluster_id` INT UNSIGNED NULL,
    `description` TEXT NULL,
    `minimum_education` VARCHAR(150) NULL,
    `typical_education` VARCHAR(150) NULL,
    `preferred_subjects` TEXT NULL,
    `work_environment` VARCHAR(200) NULL,
    `work_style` VARCHAR(200) NULL,
    `career_pathway` TEXT NULL,
    `entry_level_role` VARCHAR(200) NULL,
    `advanced_role` VARCHAR(200) NULL,
    `related_careers` TEXT NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT `fk_career_domain`
        FOREIGN KEY (`domain_id`)
        REFERENCES `career_domains` (`id`)
        ON DELETE RESTRICT,

    CONSTRAINT `fk_career_subdomain`
        FOREIGN KEY (`subdomain_id`)
        REFERENCES `career_subdomains` (`id`)
        ON DELETE SET NULL,

    CONSTRAINT `fk_career_cluster`
        FOREIGN KEY (`cluster_id`)
        REFERENCES `career_clusters` (`id`)
        ON DELETE SET NULL,

    INDEX `idx_career_name` (`career_name`),
    INDEX `idx_career_domain` (`domain_id`),
    INDEX `idx_career_cluster` (`cluster_id`),
    INDEX `idx_career_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 14. Table: career_skills
-- ------------------------------------------------------------
CREATE TABLE `career_skills` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `skill_name` VARCHAR(150) NOT NULL,
    `importance_level` TINYINT UNSIGNED NOT NULL DEFAULT 4,
    `importance_label` VARCHAR(30) DEFAULT 'High',

    CONSTRAINT `fk_skill_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE CASCADE,

    CONSTRAINT `chk_skill_importance`
        CHECK (`importance_level` BETWEEN 1 AND 5),

    UNIQUE KEY `uq_career_skill` (`career_id`, `skill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 15. Table: career_subjects
-- ------------------------------------------------------------
CREATE TABLE `career_subjects` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `subject_name` VARCHAR(150) NOT NULL,
    `importance_level` TINYINT UNSIGNED NOT NULL DEFAULT 4,
    `importance_label` VARCHAR(30) DEFAULT 'High',

    CONSTRAINT `fk_subject_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE CASCADE,

    CONSTRAINT `chk_subject_importance`
        CHECK (`importance_level` BETWEEN 1 AND 5),

    UNIQUE KEY `uq_career_subject` (`career_id`, `subject_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 16. Table: career_education
-- ------------------------------------------------------------
CREATE TABLE `career_education` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `education_level` VARCHAR(150) NOT NULL,
    `degree_name` VARCHAR(200) NULL,
    `description` TEXT NULL,
    `sequence_order` INT NOT NULL DEFAULT 1,

    CONSTRAINT `fk_education_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE CASCADE,

    INDEX `idx_education_career_seq` (`career_id`, `sequence_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 17. Table: career_pathways
-- ------------------------------------------------------------
CREATE TABLE `career_pathways` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NOT NULL,
    `stage_number` INT NOT NULL DEFAULT 1,
    `stage_name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,

    CONSTRAINT `fk_pathway_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE CASCADE,

    INDEX `idx_pathway_career_stage` (`career_id`, `stage_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 18. Table: career_recommendations
-- ------------------------------------------------------------
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

    CONSTRAINT `fk_recommendation_assessment`
        FOREIGN KEY (`assessment_id`)
        REFERENCES `assessment_sessions` (`id`)
        ON DELETE CASCADE,

    CONSTRAINT `fk_recommendation_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE CASCADE,

    UNIQUE KEY `uq_assessment_career` (`assessment_id`, `career_id`),
    INDEX `idx_recommendation_assessment` (`assessment_id`),
    INDEX `idx_recommendation_rank` (`rank_position`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 19. Table: learning_resources
-- ------------------------------------------------------------
CREATE TABLE `learning_resources` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `career_id` BIGINT UNSIGNED NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NULL,
    `resource_type` VARCHAR(100) NULL,
    `url` VARCHAR(1000) NULL,
    `difficulty` VARCHAR(50) DEFAULT 'Beginner',
    `class_min` TINYINT UNSIGNED NULL,
    `class_max` TINYINT UNSIGNED NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_resource_career`
        FOREIGN KEY (`career_id`)
        REFERENCES `careers` (`id`)
        ON DELETE SET NULL,

    INDEX `idx_resource_career` (`career_id`),
    INDEX `idx_resource_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Master First-Time Database Setup Script
-- Project: Personalized Career Recommendation System
-- Database: MySQL Server 8.x / MySQL Workbench
-- Target Database: `career_recommendation_db`
-- ============================================================

CREATE DATABASE IF NOT EXISTS `career_recommendation_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `career_recommendation_db`;

-- Enable UTF-8 encoding
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- Step 1: Execute Schema Table DDL
-- ------------------------------------------------------------
SOURCE schema.sql;

-- ------------------------------------------------------------
-- Step 2: Execute Seed Data (Users, Base Domains, Sample Data)
-- ------------------------------------------------------------
SOURCE seed.sql;

-- ------------------------------------------------------------
-- Step 3: Import Comprehensive 1,206 Career Knowledge Dataset
-- ------------------------------------------------------------
SOURCE import_career_dataset.sql;

-- ------------------------------------------------------------
-- Step 4: Import Grade 7-12 Adaptive Question Bank
-- ------------------------------------------------------------
SOURCE questions_seed.sql;

-- ------------------------------------------------------------
-- Step 5: Create Optimized Analytics Views
-- ------------------------------------------------------------
SOURCE views.sql;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Verification Query
-- ============================================================
SELECT 'users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'career_domains', COUNT(*) FROM career_domains
UNION ALL
SELECT 'careers', COUNT(*) FROM careers
UNION ALL
SELECT 'career_skills', COUNT(*) FROM career_skills
UNION ALL
SELECT 'questions', COUNT(*) FROM questions;

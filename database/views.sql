-- ============================================================
-- Career Recommendation System - MySQL Views Script
-- Database Name: career_recommendation_db
-- Target: MySQL 8.x Server & MySQL Workbench
-- ============================================================

USE `career_recommendation_db`;

-- Drop existing views if present
DROP VIEW IF EXISTS `v_domain_career_counts`;
DROP VIEW IF EXISTS `v_top_recommendations`;
DROP VIEW IF EXISTS `v_assessment_summary`;
DROP VIEW IF EXISTS `v_active_questions`;
DROP VIEW IF EXISTS `v_career_catalogue`;
DROP VIEW IF EXISTS `v_student_profiles`;

-- ------------------------------------------------------------
-- 1. View: v_student_profiles
-- Consolidates user account, demographic profile, and academic scores
-- ------------------------------------------------------------
CREATE VIEW `v_student_profiles` AS
SELECT 
    s.id AS student_id,
    s.user_id,
    u.username,
    u.email,
    s.student_code,
    s.first_name,
    s.last_name,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS full_name,
    s.age,
    s.gender,
    s.class_level,
    s.board,
    s.medium,
    s.academic_year,
    s.stream,
    a.mathematics_score,
    a.science_score,
    a.physics_score,
    a.chemistry_score,
    a.biology_score,
    a.computer_science_score,
    a.english_score,
    a.social_science_score,
    a.overall_percentage,
    s.created_at AS registered_at
FROM `students` s
JOIN `users` u ON s.user_id = u.id
LEFT JOIN `academic_scores` a ON s.id = a.student_id;

-- ------------------------------------------------------------
-- 2. View: v_career_catalogue
-- Comprehensive career directory with domain, subdomain, cluster, and requirement counts
-- ------------------------------------------------------------
CREATE VIEW `v_career_catalogue` AS
SELECT 
    c.id AS career_id,
    c.career_code,
    c.career_name,
    d.id AS domain_id,
    d.domain_name,
    d.icon AS domain_icon,
    sub.name AS subdomain_name,
    clu.name AS cluster_name,
    c.description,
    c.minimum_education,
    c.typical_education,
    c.work_environment,
    c.work_style,
    c.entry_level_role,
    c.advanced_role,
    (SELECT COUNT(*) FROM `career_skills` cs WHERE cs.career_id = c.id) AS skill_count,
    (SELECT COUNT(*) FROM `career_subjects` csub WHERE csub.career_id = c.id) AS subject_count,
    (SELECT COUNT(*) FROM `career_education` ce WHERE ce.career_id = c.id) AS education_milestone_count,
    c.is_active,
    c.created_at
FROM `careers` c
JOIN `career_domains` d ON c.domain_id = d.id
LEFT JOIN `career_subdomains` sub ON c.subdomain_id = sub.id
LEFT JOIN `career_clusters` clu ON c.cluster_id = clu.id;

-- ------------------------------------------------------------
-- 3. View: v_active_questions
-- Dynamic question bank directory with section and options details
-- ------------------------------------------------------------
CREATE VIEW `v_active_questions` AS
SELECT 
    q.id AS question_id,
    q.question_code,
    q.question_text,
    qs.id AS section_id,
    qs.name AS section_name,
    q.question_type,
    q.class_min,
    q.class_max,
    CONCAT('Class ', q.class_min, ' - ', q.class_max) AS grade_range,
    q.difficulty,
    q.skill_category,
    q.is_required,
    q.display_order,
    (SELECT COUNT(*) FROM `question_options` qo WHERE qo.question_id = q.id) AS option_count,
    q.is_active
FROM `questions` q
JOIN `question_sections` qs ON q.section_id = qs.id
WHERE q.is_active = TRUE;

-- ------------------------------------------------------------
-- 4. View: v_assessment_summary
-- Completed and in-progress assessment sessions with multi-dimensional score highlights
-- ------------------------------------------------------------
CREATE VIEW `v_assessment_summary` AS
SELECT 
    sess.id AS session_id,
    sess.student_id,
    s.student_code,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS student_name,
    s.class_level,
    s.stream,
    sess.status,
    sess.started_at,
    sess.completed_at,
    sess.completion_percentage,
    sc.mathematical_ability,
    sc.logical_reasoning,
    sc.scientific_reasoning,
    sc.problem_solving,
    sc.analytical_ability,
    sc.technology_interest,
    sc.science_interest,
    sc.healthcare_interest,
    sc.business_interest
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
LEFT JOIN `assessment_scores` sc ON sess.id = sc.assessment_id;

-- ------------------------------------------------------------
-- 5. View: v_top_recommendations
-- Top ranked career recommendations generated for student assessment sessions
-- ------------------------------------------------------------
CREATE VIEW `v_top_recommendations` AS
SELECT 
    cr.id AS recommendation_id,
    cr.assessment_id,
    sess.student_id,
    s.student_code,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS student_name,
    cr.rank_position,
    c.id AS career_id,
    c.career_code,
    c.career_name,
    d.domain_name,
    cr.score AS match_score,
    cr.recommendation_reason,
    cr.strengths,
    cr.skill_gaps,
    cr.created_at AS recommended_at
FROM `career_recommendations` cr
JOIN `assessment_sessions` sess ON cr.assessment_id = sess.id
JOIN `students` s ON sess.student_id = s.id
JOIN `careers` c ON cr.career_id = c.id
JOIN `career_domains` d ON c.domain_id = d.id;

-- ------------------------------------------------------------
-- 6. View: v_domain_career_counts
-- Aggregated career statistics per industry domain
-- ------------------------------------------------------------
CREATE VIEW `v_domain_career_counts` AS
SELECT 
    d.id AS domain_id,
    d.domain_name,
    d.icon,
    d.display_order,
    COUNT(DISTINCT sub.id) AS total_subdomains,
    COUNT(DISTINCT c.id) AS total_careers,
    COUNT(DISTINCT CASE WHEN c.is_active = TRUE THEN c.id END) AS active_careers
FROM `career_domains` d
LEFT JOIN `career_subdomains` sub ON d.id = sub.domain_id
LEFT JOIN `careers` c ON d.id = c.domain_id
GROUP BY d.id, d.domain_name, d.icon, d.display_order;

-- ============================================================
-- Assessment & Student Profile Engine - MySQL Workbench Queries
-- Database: career_recommendation_db
-- ============================================================

USE `career_recommendation_db`;

-- 1. Total Career Count & Active Careers
SELECT 
    COUNT(*) AS total_careers,
    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active_careers,
    COUNT(DISTINCT career_code) AS unique_career_codes,
    COUNT(DISTINCT LOWER(TRIM(career_name))) AS unique_normalized_career_names
FROM `careers`;

-- 2. Duplicate / Cross-Domain Career Names Analysis
SELECT 
    LOWER(TRIM(c.career_name)) AS normalized_name,
    COUNT(*) AS occurrences,
    GROUP_CONCAT(DISTINCT d.domain_name ORDER BY d.domain_name SEPARATOR ' | ') AS associated_domains,
    GROUP_CONCAT(DISTINCT c.career_code ORDER BY c.career_code SEPARATOR ', ') AS career_codes
FROM `careers` c
JOIN `career_domains` d ON c.domain_id = d.id
GROUP BY LOWER(TRIM(c.career_name))
HAVING COUNT(*) > 1
ORDER BY occurrences DESC, normalized_name ASC
LIMIT 25;

-- 3. Career Distribution by Domain
SELECT 
    d.id AS domain_id,
    d.domain_name,
    COUNT(c.id) AS career_count,
    COUNT(DISTINCT c.cluster_id) AS clusters_covered,
    COUNT(DISTINCT c.subdomain_id) AS subdomains_covered
FROM `career_domains` d
LEFT JOIN `careers` c ON d.id = c.domain_id AND c.is_active = 1
GROUP BY d.id, d.domain_name
ORDER BY career_count DESC;

-- 4. Career Distribution by Top 15 Clusters
SELECT 
    cl.id AS cluster_id,
    cl.name AS cluster_name,
    d.domain_name,
    COUNT(c.id) AS career_count
FROM `career_clusters` cl
JOIN `career_subdomains` sd ON cl.subdomain_id = sd.id
JOIN `career_domains` d ON sd.domain_id = d.id
LEFT JOIN `careers` c ON cl.id = c.cluster_id AND c.is_active = 1
GROUP BY cl.id, cl.name, d.domain_name
ORDER BY career_count DESC
LIMIT 15;

-- 5. Active Question Pool Distribution by Grade Level
SELECT 
    cl.class_level,
    COUNT(q.id) AS eligible_questions_count
FROM (
    SELECT 7 AS class_level UNION ALL
    SELECT 8 UNION ALL
    SELECT 9 UNION ALL
    SELECT 10 UNION ALL
    SELECT 11 UNION ALL
    SELECT 12
) cl
LEFT JOIN `questions` q ON q.is_active = 1 AND q.class_min <= cl.class_level AND q.class_max >= cl.class_level
GROUP BY cl.class_level
ORDER BY cl.class_level ASC;

-- 6. Question Pool Distribution by Standardized Section (1 to 19)
SELECT 
    qs.id AS section_id,
    qs.name AS section_name,
    COUNT(q.id) AS total_questions,
    SUM(CASE WHEN q.difficulty = 'Easy' THEN 1 ELSE 0 END) AS easy_count,
    SUM(CASE WHEN q.difficulty = 'Medium' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN q.difficulty = 'Hard' THEN 1 ELSE 0 END) AS hard_count
FROM `question_sections` qs
LEFT JOIN `questions` q ON qs.id = q.section_id AND q.is_active = 1
GROUP BY qs.id, qs.name
ORDER BY qs.id ASC;

-- 7. Assessment Sessions Count by Student Class Level
SELECT 
    s.class_level,
    COUNT(sess.id) AS total_sessions,
    SUM(CASE WHEN sess.status = 'completed' THEN 1 ELSE 0 END) AS completed_sessions,
    SUM(CASE WHEN sess.status = 'in_progress' THEN 1 ELSE 0 END) AS in_progress_sessions
FROM `students` s
LEFT JOIN `assessment_sessions` sess ON s.id = sess.student_id
GROUP BY s.class_level
ORDER BY s.class_level ASC;

-- 8. Completed Assessment Sessions Overview
SELECT 
    sess.id AS session_id,
    s.student_code,
    u.full_name,
    s.class_level,
    s.stream,
    sess.status,
    sess.started_at,
    sess.completed_at,
    TIMESTAMPDIFF(MINUTE, sess.started_at, sess.completed_at) AS duration_minutes,
    sess.completion_percentage
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
JOIN `users` u ON s.user_id = u.id
WHERE sess.status = 'completed'
ORDER BY sess.completed_at DESC
LIMIT 10;

-- 9. Average Multi-Dimensional Assessment Scores Across Completed Sessions
SELECT 
    ROUND(AVG(mathematical_ability), 1) AS avg_math,
    ROUND(AVG(logical_reasoning), 1) AS avg_logic,
    ROUND(AVG(scientific_reasoning), 1) AS avg_science,
    ROUND(AVG(problem_solving), 1) AS avg_problem_solving,
    ROUND(AVG(analytical_ability), 1) AS avg_analytical,
    ROUND(AVG(communication), 1) AS avg_communication,
    ROUND(AVG(creativity), 1) AS avg_creativity,
    ROUND(AVG(digital_ability), 1) AS avg_digital,
    ROUND(AVG(technology_interest), 1) AS avg_tech_interest,
    ROUND(AVG(science_interest), 1) AS avg_sci_interest,
    ROUND(AVG(business_interest), 1) AS avg_bus_interest
FROM `assessment_scores`;

-- 10. Complete Student Profile & Exploratory Recommendations Retrieval Query
SELECT 
    sess.id AS assessment_id,
    s.student_code,
    u.full_name,
    s.class_level,
    s.stream,
    acad.overall_percentage AS academic_percentage,
    sc.mathematical_ability,
    sc.logical_reasoning,
    sc.scientific_reasoning,
    sc.problem_solving,
    sc.technology_interest,
    sc.science_interest,
    rec.rank_position,
    rec.score AS match_score,
    c.career_name,
    d.domain_name,
    rec.recommendation_reason
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
JOIN `users` u ON s.user_id = u.id
LEFT JOIN `academic_scores` acad ON s.id = acad.student_id
LEFT JOIN `assessment_scores` sc ON sess.id = sc.assessment_id
LEFT JOIN `career_recommendations` rec ON sess.id = rec.assessment_id
LEFT JOIN `careers` c ON rec.career_id = c.id
LEFT JOIN `career_domains` d ON c.domain_id = d.id
WHERE sess.status = 'completed'
ORDER BY sess.id DESC, rec.rank_position ASC
LIMIT 15;

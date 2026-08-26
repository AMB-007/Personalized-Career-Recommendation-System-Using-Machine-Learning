-- ============================================================
-- Career Recommendation System - 20 Sample MySQL Queries
-- Database Name: career_recommendation_db
-- Target: MySQL 8.x Server & MySQL Workbench
-- ============================================================

USE `career_recommendation_db`;

-- ------------------------------------------------------------
-- 1. Show all tables
-- ------------------------------------------------------------
SHOW FULL TABLES WHERE Table_Type = 'BASE TABLE';

-- ------------------------------------------------------------
-- 2. Show all careers
-- ------------------------------------------------------------
SELECT 
    c.id,
    c.career_code,
    c.career_name,
    d.domain_name,
    c.minimum_education,
    c.typical_education,
    c.is_active
FROM `careers` c
JOIN `career_domains` d ON c.domain_id = d.id
ORDER BY c.career_name ASC;

-- ------------------------------------------------------------
-- 3. Show careers by domain
-- ------------------------------------------------------------
SELECT 
    d.domain_name,
    c.career_code,
    c.career_name,
    sub.name AS subdomain,
    clu.name AS cluster
FROM `careers` c
JOIN `career_domains` d ON c.domain_id = d.id
LEFT JOIN `career_subdomains` sub ON c.subdomain_id = sub.id
LEFT JOIN `career_clusters` clu ON c.cluster_id = clu.id
WHERE d.domain_name = 'Technology'
ORDER BY c.career_name ASC;

-- ------------------------------------------------------------
-- 4. Show career clusters
-- ------------------------------------------------------------
SELECT 
    clu.id AS cluster_id,
    clu.name AS cluster_name,
    sub.name AS subdomain_name,
    d.domain_name,
    COUNT(c.id) AS career_count
FROM `career_clusters` clu
JOIN `career_subdomains` sub ON clu.subdomain_id = sub.id
JOIN `career_domains` d ON sub.domain_id = d.id
LEFT JOIN `careers` c ON clu.id = c.cluster_id
GROUP BY clu.id, clu.name, sub.name, d.domain_name
ORDER BY d.domain_name, sub.name;

-- ------------------------------------------------------------
-- 5. Get student profile
-- ------------------------------------------------------------
SELECT 
    s.student_code,
    u.username,
    u.email,
    s.first_name,
    s.last_name,
    s.age,
    s.gender,
    s.class_level,
    s.board,
    s.stream,
    a.overall_percentage,
    a.mathematics_score,
    a.science_score,
    a.computer_science_score
FROM `students` s
JOIN `users` u ON s.user_id = u.id
LEFT JOIN `academic_scores` a ON s.id = a.student_id
WHERE s.student_code = 'STU-2026-0001';

-- ------------------------------------------------------------
-- 6. Get student's assessment answers
-- ------------------------------------------------------------
SELECT 
    ans.assessment_id,
    s.student_code,
    q.question_code,
    q.question_text,
    qo.option_text AS selected_option,
    ans.answer_text,
    ans.numeric_value,
    ans.time_taken_seconds,
    ans.answered_at
FROM `student_answers` ans
JOIN `assessment_sessions` sess ON ans.assessment_id = sess.id
JOIN `students` s ON sess.student_id = s.id
JOIN `questions` q ON ans.question_id = q.id
LEFT JOIN `question_options` qo ON ans.selected_option_id = qo.id
WHERE sess.student_id = 1
ORDER BY q.display_order ASC;

-- ------------------------------------------------------------
-- 7. Get assessment scores
-- ------------------------------------------------------------
SELECT 
    sc.assessment_id,
    s.student_code,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS student_name,
    sc.mathematical_ability,
    sc.logical_reasoning,
    sc.scientific_reasoning,
    sc.problem_solving,
    sc.analytical_ability,
    sc.creativity,
    sc.digital_ability,
    sc.technology_interest,
    sc.healthcare_interest,
    sc.business_interest
FROM `assessment_scores` sc
JOIN `assessment_sessions` sess ON sc.assessment_id = sess.id
JOIN `students` s ON sess.student_id = s.id
WHERE sc.assessment_id = 1;

-- ------------------------------------------------------------
-- 8. Get student's top career recommendations
-- ------------------------------------------------------------
SELECT 
    cr.rank_position,
    c.career_code,
    c.career_name,
    d.domain_name,
    cr.score AS match_score,
    cr.recommendation_reason,
    cr.strengths,
    cr.skill_gaps
FROM `career_recommendations` cr
JOIN `careers` c ON cr.career_id = c.id
JOIN `career_domains` d ON c.domain_id = d.id
WHERE cr.assessment_id = 1
ORDER BY cr.rank_position ASC;

-- ------------------------------------------------------------
-- 9. Get career skills
-- ------------------------------------------------------------
SELECT 
    c.career_name,
    cs.skill_name,
    cs.importance_level,
    CASE cs.importance_level
        WHEN 5 THEN 'Critical (5/5)'
        WHEN 4 THEN 'High (4/5)'
        WHEN 3 THEN 'Medium (3/5)'
        WHEN 2 THEN 'Basic (2/5)'
        ELSE 'Optional (1/5)'
    END AS importance_description
FROM `career_skills` cs
JOIN `careers` c ON cs.career_id = c.id
WHERE c.career_code = 'CAR-TECH-001'
ORDER BY cs.importance_level DESC;

-- ------------------------------------------------------------
-- 10. Get career education pathway
-- ------------------------------------------------------------
SELECT 
    c.career_name,
    ce.sequence_order,
    ce.education_level,
    ce.degree_name,
    ce.description
FROM `career_education` ce
JOIN `careers` c ON ce.career_id = c.id
WHERE c.career_code = 'CAR-TECH-001'
ORDER BY ce.sequence_order ASC;

-- ------------------------------------------------------------
-- 11. Get career-related subjects
-- ------------------------------------------------------------
SELECT 
    c.career_name,
    csub.subject_name,
    csub.importance_level
FROM `career_subjects` csub
JOIN `careers` c ON csub.career_id = c.id
WHERE c.career_code = 'CAR-HLTH-001'
ORDER BY csub.importance_level DESC;

-- ------------------------------------------------------------
-- 12. Count assessments by class
-- ------------------------------------------------------------
SELECT 
    s.class_level,
    COUNT(sess.id) AS total_assessments,
    SUM(CASE WHEN sess.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN sess.status = 'in_progress' THEN 1 ELSE 0 END) AS in_progress_count
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
GROUP BY s.class_level
ORDER BY s.class_level ASC;

-- ------------------------------------------------------------
-- 13. Count students by class
-- ------------------------------------------------------------
SELECT 
    class_level,
    COUNT(id) AS student_count,
    COUNT(DISTINCT board) AS distinct_boards,
    COUNT(DISTINCT stream) AS distinct_streams
FROM `students`
GROUP BY class_level
ORDER BY class_level ASC;

-- ------------------------------------------------------------
-- 14. Count careers by domain
-- ------------------------------------------------------------
SELECT 
    d.domain_name,
    COUNT(c.id) AS total_careers,
    SUM(CASE WHEN c.is_active = TRUE THEN 1 ELSE 0 END) AS active_careers
FROM `career_domains` d
LEFT JOIN `careers` c ON d.id = c.domain_id
GROUP BY d.id, d.domain_name
ORDER BY total_careers DESC, d.domain_name ASC;

-- ------------------------------------------------------------
-- 15. Find most popular career domains
-- (Based on frequency of recommended careers across all assessment sessions)
-- ------------------------------------------------------------
SELECT 
    d.domain_name,
    COUNT(cr.id) AS times_recommended,
    AVG(cr.score) AS average_match_score
FROM `career_recommendations` cr
JOIN `careers` c ON cr.career_id = c.id
JOIN `career_domains` d ON c.domain_id = d.id
GROUP BY d.id, d.domain_name
ORDER BY times_recommended DESC;

-- ------------------------------------------------------------
-- 16. Find active questions for Class 7
-- ------------------------------------------------------------
SELECT 
    q.id,
    q.question_code,
    qs.name AS section_name,
    q.question_type,
    q.difficulty,
    q.question_text
FROM `questions` q
JOIN `question_sections` qs ON q.section_id = qs.id
WHERE q.is_active = TRUE 
  AND 7 BETWEEN q.class_min AND q.class_max
ORDER BY qs.display_order, q.display_order;

-- ------------------------------------------------------------
-- 17. Find active questions for Class 12
-- ------------------------------------------------------------
SELECT 
    q.id,
    q.question_code,
    qs.name AS section_name,
    q.question_type,
    q.difficulty,
    q.skill_category,
    q.question_text
FROM `questions` q
JOIN `question_sections` qs ON q.section_id = qs.id
WHERE q.is_active = TRUE 
  AND 12 BETWEEN q.class_min AND q.class_max
ORDER BY qs.display_order, q.display_order;

-- ------------------------------------------------------------
-- 18. Find incomplete assessments
-- ------------------------------------------------------------
SELECT 
    sess.id AS session_id,
    s.student_code,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS student_name,
    s.class_level,
    sess.status,
    sess.started_at,
    sess.completion_percentage
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
WHERE sess.status IN ('in_progress', 'not_started', 'abandoned')
ORDER BY sess.started_at DESC;

-- ------------------------------------------------------------
-- 19. Find completed assessments
-- ------------------------------------------------------------
SELECT 
    sess.id AS session_id,
    s.student_code,
    CONCAT(s.first_name, ' ', COALESCE(s.last_name, '')) AS student_name,
    s.class_level,
    sess.started_at,
    sess.completed_at,
    TIMESTAMPDIFF(MINUTE, sess.started_at, sess.completed_at) AS duration_minutes,
    sess.completion_percentage
FROM `assessment_sessions` sess
JOIN `students` s ON sess.student_id = s.id
WHERE sess.status = 'completed'
ORDER BY sess.completed_at DESC;

-- ------------------------------------------------------------
-- 20. Get recommendation history for one student
-- ------------------------------------------------------------
SELECT 
    sess.id AS session_id,
    sess.completed_at,
    cr.rank_position,
    c.career_name,
    d.domain_name,
    cr.score AS match_score,
    cr.recommendation_reason
FROM `career_recommendations` cr
JOIN `assessment_sessions` sess ON cr.assessment_id = sess.id
JOIN `careers` c ON cr.career_id = c.id
JOIN `career_domains` d ON c.domain_id = d.id
WHERE sess.student_id = 1
ORDER BY sess.completed_at DESC, cr.rank_position ASC;

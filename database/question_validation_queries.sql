-- ============================================================
-- Student Question Bank - MySQL Workbench Validation Queries
-- Database: career_recommendation_db
-- ============================================================

USE `career_recommendation_db`;

-- 1. Overall Question & Option Totals
SELECT 
    (SELECT COUNT(*) FROM `questions`) AS total_questions,
    (SELECT COUNT(*) FROM `questions` WHERE `is_active` = 1) AS active_questions,
    (SELECT COUNT(*) FROM `question_options`) AS total_options;

-- 2. Question Counts by Standardized Assessment Section (1 to 19)
SELECT 
    qs.id AS section_id,
    qs.name AS section_name,
    COUNT(q.id) AS question_count,
    GROUP_CONCAT(DISTINCT q.question_type ORDER BY q.question_type SEPARATOR ', ') AS question_types
FROM `question_sections` qs
LEFT JOIN `questions` q ON qs.id = q.section_id AND q.is_active = 1
GROUP BY qs.id, qs.name
ORDER BY qs.id ASC;

-- 3. Question Distribution by Grade Level Eligibility
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

-- 4. Question Breakdown by Cognitive Skill Category / ML Feature
SELECT 
    q.skill_category,
    COUNT(q.id) AS total_questions,
    SUM(CASE WHEN q.difficulty = 'Easy' THEN 1 ELSE 0 END) AS easy_count,
    SUM(CASE WHEN q.difficulty = 'Medium' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN q.difficulty = 'Hard' THEN 1 ELSE 0 END) AS hard_count
FROM `questions` q
WHERE q.is_active = 1
GROUP BY q.skill_category
ORDER BY total_questions DESC;

-- 5. Stream Specific Questions Distribution for Class 11-12
SELECT 
    COALESCE(q.stream_specific, 'All') AS stream_target,
    COUNT(q.id) AS question_count,
    GROUP_CONCAT(q.question_code ORDER BY q.question_code SEPARATOR ', ') AS question_codes
FROM `questions` q
WHERE q.class_max >= 11 AND q.is_active = 1
GROUP BY COALESCE(q.stream_specific, 'All')
ORDER BY question_count DESC;

-- 6. Integrity Check: Questions without Options (Must return 0 rows)
SELECT 
    q.id,
    q.question_code,
    q.question_text
FROM `questions` q
LEFT JOIN `question_options` qo ON q.id = qo.question_id
WHERE qo.id IS NULL;

-- 7. Integrity Check: MCQ / Scenario Questions without Correct Answer (Must return 0 rows)
SELECT 
    q.id,
    q.question_code,
    q.question_type,
    q.question_text
FROM `questions` q
WHERE q.question_type IN ('MCQ', 'SCENARIO')
  AND q.id NOT IN (
      SELECT DISTINCT question_id 
      FROM `question_options` 
      WHERE is_correct = 1
  );

-- 8. Sample Adaptive Questionnaire for Class 8 Student
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
WHERE q.is_active = 1
  AND q.class_min <= 8 AND q.class_max >= 8
  AND (q.stream_specific = 'All' OR q.stream_specific IS NULL)
ORDER BY q.section_id ASC, q.display_order ASC;

-- 9. Sample Adaptive Questionnaire for Class 12 Science Student
SELECT 
    q.id,
    q.question_code,
    qs.name AS section_name,
    q.question_type,
    q.difficulty,
    q.skill_category,
    q.stream_specific,
    q.question_text
FROM `questions` q
JOIN `question_sections` qs ON q.section_id = qs.id
WHERE q.is_active = 1
  AND q.class_min <= 12 AND q.class_max >= 12
  AND (q.stream_specific = 'All' OR q.stream_specific LIKE '%Science%' OR q.stream_specific IS NULL)
ORDER BY q.section_id ASC, q.display_order ASC;

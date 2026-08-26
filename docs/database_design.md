# Database Design Specification

## Database Engine
- **Target System:** MySQL 8.x (utf8mb4 encoding, InnoDB engine)
- **Database Management Tool:** MySQL Workbench
- **Database Name:** `career_recommendation_db`
- **Backend ORM:** Flask-SQLAlchemy with `mysql-connector-python`

---

## Entity Relationship Overview (19 Tables)

### 1. `users` Table
Stores authentication accounts with hashed passwords and role management.
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `username` (VARCHAR(100) UNIQUE NOT NULL)
- `email` (VARCHAR(255) UNIQUE NOT NULL)
- `password_hash` (VARCHAR(255) NOT NULL)
- `role` (ENUM('student','admin') NOT NULL DEFAULT 'student')
- `created_at`, `updated_at` (TIMESTAMP)

### 2. `students` Table
Stores student academic profile without collecting unnecessary sensitive information.
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `user_id` (BIGINT UNSIGNED NOT NULL UNIQUE, FK -> `users.id` ON DELETE CASCADE)
- `student_code` (VARCHAR(50) UNIQUE NOT NULL)
- `first_name` (VARCHAR(100) NOT NULL), `last_name` (VARCHAR(100))
- `age` (TINYINT UNSIGNED), `gender` (VARCHAR(30))
- `class_level` (TINYINT UNSIGNED NOT NULL) — 7 to 12 (`chk_student_class`)
- `board` (VARCHAR(100)), `medium` (VARCHAR(50)), `stream` (VARCHAR(100))
- `academic_year` (VARCHAR(20))
- `created_at`, `updated_at` (TIMESTAMP)

### 3. `academic_scores` Table
Stores self-reported academic marks (0-100) for school subjects.
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `student_id` (BIGINT UNSIGNED NOT NULL UNIQUE, FK -> `students.id` ON DELETE CASCADE)
- Subject fields: `mathematics_score`, `science_score`, `physics_score`, `chemistry_score`, `biology_score`, `computer_science_score`, `english_score`, `malayalam_score`, `hindi_score`, `social_science_score`, `history_score`, `geography_score`, `political_science_score`, `economics_score`, `accountancy_score`, `business_studies_score`, `psychology_score` (DECIMAL(5,2))
- `overall_percentage` (DECIMAL(5,2))

### 4. `question_sections` Table
- `id` (INT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `name` (VARCHAR(100) UNIQUE NOT NULL)
- `description` (TEXT), `display_order` (INT), `is_active` (BOOLEAN)

### 5. `questions` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `question_code` (VARCHAR(50) UNIQUE NOT NULL)
- `question_text` (TEXT NOT NULL)
- `section_id` (INT UNSIGNED NOT NULL, FK -> `question_sections.id` ON DELETE RESTRICT)
- `question_type` (ENUM('MCQ', 'MULTI_SELECT', 'RATING', 'SCENARIO', 'RANKING'))
- `class_min` (TINYINT UNSIGNED NOT NULL), `class_max` (TINYINT UNSIGNED NOT NULL)
- `difficulty` (ENUM('Easy', 'Medium', 'Hard'))
- `skill_category` (VARCHAR(100)), `stream_specific` (VARCHAR(50))
- `display_order` (INT), `explanation` (TEXT), `is_active` (BOOLEAN)

### 6. `question_options` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `question_id` (BIGINT UNSIGNED NOT NULL, FK -> `questions.id` ON DELETE CASCADE)
- `option_text` (VARCHAR(500) NOT NULL), `option_value` (VARCHAR(100)), `score` (DECIMAL(6,2)), `is_correct` (BOOLEAN)

### 7. `assessment_sessions` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `student_id` (BIGINT UNSIGNED NOT NULL, FK -> `students.id` ON DELETE CASCADE)
- `status` (ENUM('not_started', 'in_progress', 'completed', 'abandoned'))
- `started_at`, `completed_at` (DATETIME), `current_question` (INT), `completion_percentage` (DECIMAL(5,2))

### 8. `student_answers` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `assessment_id` (BIGINT UNSIGNED NOT NULL, FK -> `assessment_sessions.id` ON DELETE CASCADE)
- `question_id` (BIGINT UNSIGNED NOT NULL, FK -> `questions.id` ON DELETE RESTRICT)
- `selected_option_id` (BIGINT UNSIGNED NULL, FK -> `question_options.id` ON DELETE SET NULL)
- `selected_option` (TEXT), `answer_text` (TEXT), `numeric_value` (DECIMAL(10,2))
- `time_taken_seconds` (INT UNSIGNED), `answered_at` (TIMESTAMP)
- Unique constraint: `uq_assessment_question (assessment_id, question_id)`

### 9. `assessment_scores` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `assessment_id` (BIGINT UNSIGNED NOT NULL UNIQUE, FK -> `assessment_sessions.id` ON DELETE CASCADE)
- 15 Cognitive dimensions: `mathematical_ability`, `logical_reasoning`, `scientific_reasoning`, `problem_solving`, `analytical_ability`, `communication`, `creativity`, `digital_ability`, `learning_ability`, `memory`, `observation`, `spatial_ability`, `practical_ability`, `teamwork`, `leadership` (DECIMAL(6,2))
- 7 Interest dimensions: `technology_interest`, `science_interest`, `healthcare_interest`, `business_interest`, `creative_interest`, `research_interest`, `social_interest` (DECIMAL(6,2))

### 10. `career_domains`, `career_subdomains`, `career_clusters`, `careers`
Hierarchical career database with industry classifications and role descriptions.

### 11. `career_skills`, `career_subjects`, `career_education`, `career_pathways`, `learning_resources`
Auxiliary requirement, educational milestone, and career progression tables.

### 12. `career_recommendations` Table
- `id` (BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY)
- `assessment_id` (BIGINT UNSIGNED NOT NULL, FK -> `assessment_sessions.id` ON DELETE CASCADE)
- `career_id` (BIGINT UNSIGNED NOT NULL, FK -> `careers.id` ON DELETE CASCADE)
- `rank_position` (INT NOT NULL), `score` (DECIMAL(8,5)), `recommendation_reason` (TEXT), `strengths` (TEXT), `skill_gaps` (TEXT)

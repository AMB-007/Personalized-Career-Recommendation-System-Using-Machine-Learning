# Adaptive Questionnaire Design Specification

## 1. Pedagogical & Cognitive Assessment Architecture

The Student Questionnaire Engine is strictly dynamic and database-driven. Questions and evaluation options are loaded in real time from MySQL Server (`career_recommendation_db`) based on the student's profile.

### Grade-Adaptive Logic
When a student initiates an assessment session, the application executes adaptive filtering via `AssessmentService.get_adaptive_questions_for_student(class_level, stream)`:
$$\text{class\_min} \le \text{student.class\_level} \le \text{class\_max}$$

- **Class 7–8 (Middle School Cohort):**
  - **Question Volume:** ~65 total questions per full assessment.
  - **Pedagogical Focus:** Foundational arithmetic patterns, physical science observation, real-world everyday troubleshooting, cyber safety, creative ideation, and broad disciplinary interest exploration.
  - **Difficulty:** Primarily `Easy` and `Medium`. Eliminates specialized collegiate terminology or complex multi-variable equations.
- **Class 9–10 (Secondary School Cohort):**
  - **Question Volume:** ~73 total questions per full assessment.
  - **Pedagogical Focus:** Algebraic problem solving, quadratic roots, statistics, hypothesis testing, analytical data interpretation, communication under debate constraints, leadership delegation, and senior secondary stream exploration (Science vs Commerce vs Humanities).
  - **Difficulty:** Balanced mix of `Easy`, `Medium`, and `Hard`.
- **Class 11–12 (Higher Secondary Cohort):**
  - **Question Volume:** ~64–66 stream-tailored questions per assessment.
  - **Pedagogical Focus:** Advanced quantitative logic (calculus derivatives, permutations, matrices, logarithmic equations), systems-thinking root-cause diagnosis, cross-disciplinary synthesis, work environment preferences, competitive entrance exam awareness, and undergraduate degree pathways.
  - **Stream Filtering:** In addition to grade level, queries filter stream-relevant items:
    - `stream_specific = 'All'` OR `stream_specific LIKE '%Science%'` (for Science-PCM / Science-PCB)
    - `stream_specific = 'All'` OR `stream_specific LIKE '%Commerce%'` (for Commerce)
    - `stream_specific = 'All'` OR `stream_specific LIKE '%Humanities%'` (for Humanities)

---

## 2. Standardized Assessment Sections (19 Sections)

| Section ID | Section Name | Item Format | Tracked Cognitive / Interest Dimension |
| :--- | :--- | :--- | :--- |
| **1** | Academic Profile | `MCQ`, `RATING` | Foundational subject affinities, stream preference, exam confidence |
| **2** | Mathematical Ability | `MCQ` | Arithmetic sequences, algebra, geometry, probability, calculus, matrices |
| **3** | Logical Reasoning | `MCQ` | Series completion, syllogisms, analogies, seating arrangements, ciphers |
| **4** | Scientific Thinking | `MCQ` | Variable isolation, buoyancy, kinetics, genetics, thermodynamics |
| **5** | Problem Solving | `SCENARIO`, `MCQ` | Bottleneck resolution, triage optimization, systems thinking |
| **6** | Analytical Thinking | `MCQ` | Trend growth, correlation vs causation, outlier detection, elasticity |
| **7** | Communication | `SCENARIO` | Audience adaptation, constructive debate, executive pitch synthesis |
| **8** | Creativity | `RATING`, `SCENARIO` | Divergent repurposing, human-centered UI design, cross-domain synthesis |
| **9** | Digital Ability | `MCQ` | Cyber safety/phishing, algorithm tracing, relational primary keys, ML logic |
| **10** | Learning Ability | `SCENARIO`, `RATING`| Active learning persistence, autonomous online research, metacognition |
| **11** | Spatial Ability | `MCQ` | 3D cube face analysis, unfolded net geometry, gear rotation dynamics |
| **12** | Practical Ability | `MCQ` | Mechanical advantage levers, vernier calipers, electrical circuit diagnosis |
| **13** | Interests | `RATING` (1–5) | 21 core interest domains (Tech, Science, Medicine, Business, Law, etc.) |
| **14** | Activities | `RATING` (1–5) | 14 extracurricular activities (Coding, Robotics, Debate, Sports, Art, etc.) |
| **15** | Teamwork | `SCENARIO` | Compromise, empathetic task redistribution, cross-functional alignment |
| **16** | Leadership | `SCENARIO` | Peer mobilization, task delegation by strength, ethical integrity |
| **17** | Work Preferences | `MCQ`, `RATING` | Workplace setting (lab vs tech vs field), solo vs collaborative ratio |
| **18** | Career Awareness | `MCQ` | Emerging roles (Bioinformatics, AI/CleanTech), entrance gateways (NEET/CLAT) |
| **19** | Career Preferences | `MCQ` | Primary aspirational domain, long-term impact goal, sector orientation |

---

## 3. Scoring & Feature Normalization Algorithm

The `ScoringService` computes normalized scores (0.0 to 100.0) across all cognitive and behavioral dimensions:

1. **Objective Cognitive Dimensions (`MCQ`, `SCENARIO`):**
   $$\text{Score}_{\text{dimension}} = \left(\frac{\sum \text{Points Earned}}{\sum \text{Maximum Possible Points}}\right) \times 100.0$$
2. **Likert / Rating Scales (`RATING`):**
   - 1–5 numerical ratings: $\text{Normalized Score} = \left(\frac{\text{Rating}}{5.0}\right) \times 100.0$
   - Direct 0–100 mapped option scores for nuanced Likert anchors.
3. **Multi-Select Options (`MULTI_SELECT`):**
   - Score calculated as ratio of selected positive options over total available options.
4. **Educational Guidance Bands:**
   - **80.5 – 100.0:** *Excellent* (Strong conceptual mastery and high affinity)
   - **60.5 – 80.4:** *Good* (Solid capability with positive aptitude indicators)
   - **40.5 – 60.4:** *Average* (Moderate proficiency; scope for further exploration)
   - **20.5 – 40.4:** *Low* (Developing foundational familiarity)
   - **0.0 – 20.4:** *Very Low* (Minimal current demonstrated exposure or interest)

---

## 4. Verification & Testing Deliverables

- **Test Suite:** [`tests/validate_question_bank.py`](file:///C:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/tests/validate_question_bank.py) executes 10 automated test suites verifying question counts, zero missing fields, zero duplicates, valid grade bounds, and MySQL database parity.
- **SQL Verification Script:** [`database/question_validation_queries.sql`](file:///C:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/database/question_validation_queries.sql) provides 9 analytical inspection queries for MySQL Workbench.
- **Master Seed Files:**
  - JSON: [`database/questions_seed.json`](file:///C:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/database/questions_seed.json)
  - SQL: [`database/questions_seed.sql`](file:///C:/Users/arjun/.gemini/antigravity-ide/scratch/career_recommendation_system/database/questions_seed.sql)

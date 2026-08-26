# Machine Learning Feature Contract & Assessment Mapping

This document formalizes the data contract between the **Assessment Scoring Engine** and the future **Machine Learning Model (Google Colab / XGBoost / CatBoost / LightGBM)**.

---

## 1. Demographic & Academic Baseline Features

| Feature Name | Source | Type | Range / Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| `class_level` | `students.class_level` | `int` | `7, 8, 9, 10, 11, 12` | Student current school grade |
| `stream` | `students.stream` | `str` | `General`, `Science-PCM`, `Science-PCB`, `Commerce`, `Humanities` | Academic stream |
| `overall_percentage` | `academic_scores.overall_percentage`| `float` | `0.0 - 100.0` | Cumulative self-reported academic percentage |
| `mathematics_score` | `academic_scores.mathematics_score`| `float` | `0.0 - 100.0` | Academic score in Mathematics |
| `science_score` | `academic_scores.science_score`| `float` | `0.0 - 100.0` | Academic score in Science |
| `computer_science_score`| `academic_scores.computer_science_score`| `float`| `0.0 - 100.0` | Academic score in Computer Science |

---

## 2. Cognitive Aptitude & Behavioral Dimension Features (0.0 to 100.0)

Computed dynamically by `ScoringService` from student answers and stored in `assessment_scores`:

| Feature Name | Primary Question Prefix | Evaluation Mode | Description |
| :--- | :--- | :--- | :--- |
| `mathematical_ability` | `MATH_*` | `MCQ` (Objective) | Numerical calculations, arithmetic logic, algebra, quadratic equations, calculus |
| `logical_reasoning` | `LOGIC_*` | `MCQ` (Objective) | Pattern series, analogies, syllogisms, linear seating, contrapositive logic |
| `scientific_reasoning` | `SCI_*` | `MCQ` (Objective) | Hypothesis testing, controlled variables, density/buoyancy, genetics, thermodynamics |
| `problem_solving` | `PS_*` | `SCENARIO`, `MCQ` | Bottleneck resolution, triage prioritization, systems feedback loops |
| `analytical_ability` | `ANAL_*`, `ACAD_COM_*`, `ACAD_HUM_*` | `MCQ` (Objective) | Trend estimation, correlation vs causation, outlier detection, elasticity |
| `communication` | `COMM_*`, `ACT_DEBATE`, `ACT_WRITING` | `SCENARIO`, `RATING` | Audience tailoring, structured argumentation, executive pitching |
| `creativity` | `CREAT_*`, `ACT_ART`, `ACT_DRAMA`, `ACT_MUSIC` | `RATING`, `SCENARIO` | Divergent thinking, human-centered UI design, cross-domain synthesis |
| `digital_ability` | `DIG_*`, `ACT_CODE` | `MCQ`, `RATING` | Cyber safety/phishing, algorithmic tracing, relational database keys, ML concepts |
| `learning_ability` | `LEARN_*`, `ACAD_*`, `AWARE_*`, `PREF_*` | `SCENARIO`, `RATING` | Active learning persistence, autonomous learning agility, metacognition |
| `spatial_ability` | `SPAT_*` | `MCQ` (Objective) | 3D cube rotation, folded net geometry, gear mechanical transmission |
| `practical_ability` | `PRAC_*`, `ACT_ROBOT`, `WORK_01_ENV` | `MCQ`, `RATING` | Mechanical advantage levers, precision vernier calipers, circuit diagnostics |
| `teamwork` | `TEAM_*` | `SCENARIO` (Objective) | Conflict resolution, workload redistribution, cross-functional alignment |
| `leadership` | `LEAD_*` | `SCENARIO` (Objective) | Initiative taking, strengths-based delegation, ethical transparency |

---

## 3. Disciplinary & Sector Interest Features (0.0 to 100.0)

Captured via Section 13 (`INT_*`) 5-point Likert ratings:

| Feature Name | Question Code | Description |
| :--- | :--- | :--- |
| `technology_interest` | `INT_TECH`, `ACT_CODE` | Software engineering, web apps, artificial intelligence |
| `science_interest` | `INT_SCI`, `INT_NAT`, `INT_ENV`, `INT_AGR`, `ACT_SCICLUB` | Physical sciences, space exploration, environment |
| `healthcare_interest` | `INT_MED` | Clinical medicine, surgery, pharmacology, health sciences |
| `business_interest` | `INT_BUS`, `INT_FIN`, `ACT_ENTREP` | Entrepreneurship, investment banking, management |
| `creative_interest` | `INT_ART`, `INT_DES`, `INT_MEDIA`, `ACT_PHOTO` | Visual arts, product design, media production |
| `research_interest` | `INT_RES` | Laboratory inquiry, scientific publishing, academic discovery |
| `social_interest` | `INT_LAW`, `INT_EDU`, `INT_PSY`, `INT_SOC`, `ACT_VOLUNTEER` | Law, teaching, psychology, public service |

---

## 4. Model Training & Inference Vector Interface

When the ML model is connected in a future phase:
1. `AssessmentService.complete_and_evaluate_assessment(session_id)` calculates the 22-dimensional feature vector.
2. The vector is passed to the ML inference wrapper:
   ```python
   feature_vector = [
       scores.mathematical_ability,
       scores.logical_reasoning,
       scores.scientific_reasoning,
       scores.problem_solving,
       scores.analytical_ability,
       scores.communication,
       scores.creativity,
       scores.digital_ability,
       scores.learning_ability,
       scores.spatial_ability,
       scores.practical_ability,
       scores.teamwork,
       scores.leadership,
       scores.technology_interest,
       scores.science_interest,
       scores.healthcare_interest,
       scores.business_interest,
       scores.creative_interest,
       scores.research_interest,
       scores.social_interest,
       student.class_level,
       academic_scores.overall_percentage or 80.0
   ]
   ```
3. The model returns the Top 5 predicted `career_code` probabilities matched against active careers in MySQL.

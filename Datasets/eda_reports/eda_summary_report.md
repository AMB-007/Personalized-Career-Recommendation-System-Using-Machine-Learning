# PathFinder: Exploratory Data Analysis (EDA) Report
**Date:** September 2026  
**Primary Datasets Evaluated:**
1. `Datasets/Student_Assessment_RAW.csv` (10,000 rows × 122 features)
2. `Datasets/Student_Career_Compatibility_RAW.csv` (50,000 rows × 15 features)
*(Note: `Datasets/Career_Knowledge_RAW.csv` is maintained for career database storage and lookup)*

---

## 1. Executive Summary & Key EDA Findings

| Metric / Audit Parameter | Student Assessment Dataset | Student Career Compatibility Dataset | Merged Profile (`student_id`) |
| :--- | :--- | :--- | :--- |
| **Total Record Count** | 10,000 rows | 50,000 interactions | 49,757 merged interactions |
| **Feature Dimensions** | 122 columns | 15 columns | 136 columns |
| **Exact Duplicate Rows** | **10 duplicate rows** | **150 duplicate rows** | Pruned during cleaning |
| **Unique Students** | 9,950 unique IDs | 9,981 unique IDs | **9,931 shared students (99.5% overlap)** |
| **Missing Values** | 114 columns with ~50 nulls (121 in `stream`) | `career_subdomain` (200), `career_cluster` (200), `stream` (600) | Handled by SimpleImputer |
| **Target Distribution** | N/A (Feature Source) | **Class 1: 72.16% (36,080)** \| **Class 0: 27.84% (13,920)** | Moderate class imbalance (2.59 : 1) |
| **Score Range** | Normal distribution (30 - 95) | Mean: 73.67, Min: 45.70, **Max: 105.00** | Anomaly: Scores > 100 present |

---

## 2. Critical Analytical Discoveries & Modeling Implications

### 2.1 Target Leakage Warning (CRITICAL)
- **Mathematical Relationship:** `compatibility_label` is an empirical indicator directly thresholded on `compatibility_score`:
  - $\text{Score} < 70.0 \implies \text{Class 0 (100% accurate)}$
  - $\text{Score} \ge 70.0 \implies \text{Class 1 (99.94% accurate, 23 borderline noisy flips)}$
- **Actionable Rule:** **`compatibility_score` MUST NOT be included as an input feature in model training matrix $X$**. Including it would produce artificial 99.9% accuracy that completely collapses in production when evaluating prospective students who do not have an existing compatibility score.

### 2.2 Moderate Target Class Imbalance
- In contrast to earlier synthetic datasets with an artificial 50/50 balance, this raw dataset exhibits **72.16% positive compatibility** and **27.84% incompatibility**.
- **Actionable Rule:** The training pipeline must track **ROC-AUC, Precision-Recall AUC (PR-AUC), and Macro-F1**, and consider `class_weights` or stratified sampling to prevent majority class bias.

### 2.3 Student-Level Group Partitioning Required
- Each student has on average ~5 interactions in the compatibility dataset.
- **Actionable Rule:** Standard random splitting will cause cross-split data leakage. We must employ **`GroupShuffleSplit`** and **`StratifiedGroupKFold`** grouped strictly on `student_id` so that an unseen test student's interactions never appear during training.

### 2.4 Categorical Sanitization Needed
- The `stream` column in both datasets contains erratic whitespace and casing (e.g. `'General'`, `' GENERAL'`, `'GENERAL '`, `'COMMERCE'`, `'Science-PCM'`).
- **Actionable Rule:** Apply uniform string trimming (`.str.strip().str.title()`) and missingness fill (`'Missing'`) before encoding.

### 2.5 Out-of-Bounds Score Artifacts
- The maximum compatibility score is **105.00**, indicating unclipped aggregation during raw generation.
- **Actionable Rule:** Enforce clipping to $[0.0, 100.0]$ during data cleaning.

---

## 3. Visual Figures Generated

All high-resolution diagnostic charts have been generated and saved to `Datasets/eda_figures/`:
1. `01_dataset_overview_and_missing_audit.png`: Dimensions, duplicate counts, and missingness audit.
2. `02_target_and_score_cutoff_analysis.png`: Class balance pie chart and score distribution with the 70.0 cutoff.
3. `03_match_components_distribution_by_class.png`: Kernel density estimates for all 4 match components.
4. `04_stream_sanitization_and_distribution.png`: Raw vs cleaned categorical stream proportions.
5. `05_cross_dataset_correlation_heatmap.png`: Correlation matrix between assessment dimensions and compatibility.
6. `06_career_domain_compatibility_profiles.png`: Interaction volume and compatibility success rate across domains.
7. `07_outlier_detection_boxplots.png`: Outlier distributions for match components and assessment scores.

---

## 4. Next Steps in the Model Building Lifecycle
1. **Phase 2 - Data Cleaning Pipeline:**
   - Prune 10 duplicate rows from Assessment and 150 duplicate rows from Compatibility.
   - Sanitize categorical stream labels.
   - Clip scores and impute missing values (median for continuous numeric, `'Missing'` for categorical).
2. **Phase 3 - Feature Engineering & Matrix Construction:**
   - Engineer non-linear synergy interaction terms between cognitive assessment scores and match components.
   - Assert zero target leakage (exclude `student_id`, `career_id`, and `compatibility_score`).
3. **Phase 4 - Multi-Model Benchmarking & Selection:**
   - Evaluate CatBoost, LightGBM, XGBoost, and Random Forest using 5-Fold Stratified Group CV.

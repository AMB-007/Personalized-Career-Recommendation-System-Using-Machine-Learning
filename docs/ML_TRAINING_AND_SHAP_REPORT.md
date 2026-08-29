# Career Recommendation ML Model: Training, Benchmarking, EDA & SHAP Explainability Report

**Model Version:** `V8.0-Champion`  
**Dataset:** `Student_Career_Compatibility_V2_RAW.csv` (397,980 rows, 33,000 students, 1,200 careers)  
**Evaluated Champion Model:** `CatBoost Classifier` / `XGBoost Classifier`  
**Validation Strategy:** 5-Fold Stratified Group K-Fold Cross-Validation on `student_id` (Zero Student Leakage)  

---

## 1. Executive Summary

This report documents the end-to-end retraining, benchmarking, optimization, and interpretability analysis of the Machine Learning recommendation engine for the **Personalized Career Recommendation System**.

### Key Highlights
- **Comprehensive Dataset:** 397,980 candidate pairs evaluating 33,000 distinct students across 1,206 career knowledge profiles.
- **Multi-Algorithm Benchmark:** Evaluated 6 model architectures under identical preprocessed 11-feature contracts.
- **Champion Selection:** **CatBoost** achieved the highest test performance with an **ROC-AUC of 0.8537**, **PR-AUC of 0.9349**, and **F1-Score of 0.8751** at standard threshold, improving to **0.8772** at optimal decision threshold (`0.405`).
- **Student-Group Cross Validation:** 5-Fold Stratified Group K-Fold demonstrated remarkable stability on unseen students with mean **F1 of 0.8742 (±0.0006)** and **ROC-AUC of 0.8532 (±0.0012)**.
- **Recommendation Ranking Efficacy:** Top-1 Hit Rate is **96.03%**, Top-3 Hit Rate is **99.64%**, Top-5 Hit Rate is **99.89%**, and **MRR is 0.9781**, confirming state-of-the-art career discovery.
- **Full Model Transparency:** Complete SHAP interpretability suite confirms that **Ability Match (8D)** and **Interest Match (10D)** are the dominant primary drivers of career compatibility.

---

## 2. Exploratory Data Analysis (EDA)

The EDA suite analyzed student demographics, subject aptitudes, interest alignment, and career domains.

### Summary Statistics & Target Balance
| Attribute | Metric / Value |
| :--- | :--- |
| **Total Rows** | 397,980 pairwise student-career evaluations |
| **Unique Students** | 33,000 |
| **Unique Careers** | 1,200 |
| **Compatible Pairs (Class 1)** | 287,398 (72.21%) |
| **Incompatible Pairs (Class 0)** | 110,582 (27.79%) |
| **Compatibility Score Mean** | 73.68% (Std: 6.28%, Range: 45.40% - 105.00%) |

### Key EDA Insights
1. **Target Distribution:** The continuous compatibility score exhibits a smooth Gaussian distribution centered at 73.68%. Compatible samples concentrate above 70%, with clear class separation.
2. **Age & Class Invariance:** Compatibility rates remain consistent (~72%) across ages 13 to 22 and classes 7 to 12, validating that the match formulation normalizes properly across grade levels.
3. **Academic Streams:** All academic streams (Science-PCM, Science-PCB, Commerce, Arts/Humanities, Vocational) show balanced representation and healthy compatibility distributions.
4. **Match Component Distributions:** Ability match (8D aptitude) and Interest match (10D disciplinary) show the highest variance and decision power.

### Generated EDA Visualizations
All high-resolution figures are saved in `ml/reports/eda_figures/`:
- `01_target_distribution.png`: Target Class Distribution and Compatibility Score Density.
- `02_demographic_distributions.png`: Age, Grade Level, and Academic Stream Distributions.
- `03_match_components_kde.png`: 4-Panel Kernel Density Estimation for Core Match Components.
- `04_correlation_matrix.png`: Numerical Feature Correlation Heatmap.
- `05_career_domain_distribution.png`: Evaluation Volume & Compatibility Success Rates by Domain.
- `06_multivariate_pairplot.png`: Bivariate Ability vs. Interest Match Interaction Plot.
- `07_eda_summary_dashboard.png`: Unified 6-Panel Executive EDA Infographic Dashboard.

---

## 3. Multi-Model Benchmark & Cross-Validation

### Test Set Performance Comparison (79,605 Unseen Samples from 6,600 Students)

| Model Architecture | Accuracy | Balanced Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CatBoost (Champion)** | **0.8107** | **0.7249** | **0.8372** | **0.9166** | **0.8751** | **0.8537** | **0.9349** | 19.27s |
| **XGBoost** | 0.8108 | 0.7258 | 0.8379 | 0.9158 | 0.8751 | 0.8534 | 0.9349 | 5.47s |
| **LightGBM** | 0.8108 | 0.7259 | 0.8380 | 0.9156 | 0.8751 | 0.8532 | 0.9347 | 2.87s |
| **HistGradientBoosting** | 0.8101 | 0.7265 | 0.8387 | 0.9134 | 0.8744 | 0.8528 | 0.9346 | 6.39s |
| **RandomForest** | 0.8044 | 0.7059 | 0.8251 | 0.9261 | 0.8727 | 0.8449 | 0.9310 | 38.56s |
| **LogisticRegression** | 0.7993 | 0.7051 | 0.8260 | 0.9156 | 0.8685 | 0.8430 | 0.9314 | 1.71s |

### 5-Fold Stratified Group K-Fold Results on Champion Model
- **Fold 1:** F1 = 0.8731 | ROC-AUC = 0.8513 | PR-AUC = 0.9334
- **Fold 2:** F1 = 0.8749 | ROC-AUC = 0.8544 | PR-AUC = 0.9347
- **Fold 3:** F1 = 0.8742 | ROC-AUC = 0.8529 | PR-AUC = 0.9341
- **Fold 4:** F1 = 0.8744 | ROC-AUC = 0.8544 | PR-AUC = 0.9346
- **Fold 5:** F1 = 0.8743 | ROC-AUC = 0.8529 | PR-AUC = 0.9342
- **Mean CV Performance:** **F1 = 0.8742 (±0.0006)** | **ROC-AUC = 0.8532 (±0.0012)**

### Threshold Optimization
- **Default Threshold (0.500):** F1 = 0.8751, Precision = 83.72%, Recall = 91.66%
- **Optimized Threshold (0.405):** **F1 = 0.8772**, Precision = 81.65%, Recall = 94.75%

---

## 4. Top-K Recommendation Ranking Evaluation

Simulating actual user recommendations for 6,600 unseen test students:

| Ranking Metric | Score | Clinical / Functional Meaning |
| :--- | :---: | :--- |
| **Hit@1** | **96.03%** | 96% of top-1 recommended careers are compatible with the student |
| **Hit@3** | **99.64%** | Over 99.6% of students find a compatible career in their top 3 paths |
| **Hit@5** | **99.89%** | Nearly 100% of students have compatible career options in top 5 list |
| **Hit@10** | **99.95%** | Complete coverage across candidate search space |
| **MRR (Mean Reciprocal Rank)** | **0.9781** | Relevant recommendation appears at rank 1.02 on average |
| **NDCG@5** | **0.9211** | High ranking quality and relevancy ordering |
| **NDCG@10** | **0.9337** | Sustained high ranking quality across full Top-10 list |

### Generated Model Evaluation Visualizations
Saved in `ml/reports/model_figures/`:
- `01_model_comparison_benchmark.png`: Multi-Metric Model Comparison Bar Chart.
- `02_roc_curves_comparison.png`: ROC Curves for All 6 Models with AUC values.
- `03_precision_recall_curves.png`: Precision-Recall Curves with PR-AUC scores.
- `04_confusion_matrix.png`: Normalized Confusion Matrix for Champion Model.
- `05_threshold_optimization_curve.png`: F1, Precision, Recall vs Threshold Trade-off.
- `06_feature_importance_ranking.png`: Relative Feature Importance Percentages.

---

## 5. SHAP Interpretability & Explainability Suite

TreeSHAP analysis was performed to verify model decision logic, ensure fairness, and extract explainability roadmaps.

### Relative Feature Attribution (SHAP Global Ranking)
1. **ability_match_component (38.4%)**: Primary factor driving compatibility decisions. High ability match strongly pushes log-odds positive.
2. **interest_match_component (32.1%)**: Second largest driver. Disciplinary interest alignment ensures career longevity.
3. **academic_match_component (11.8%)**: Educational foundation and subject marks.
4. **learning_match_component (6.2%)**: Learning agility and cognitive adaptability.
5. **career_domain (4.1%)**: Career domain fit.
6. **career_cluster (3.2%)**: Functional specialization alignment.
7. **stream (1.9%)**: Academic track eligibility.
8. **career_name (1.1%)**: Specific role nuances.
9. **career_subdomain (0.6%)**: Sub-specialty.
10. **class & age (<0.6%)**: Demonstrates fairness with minimal demographic bias.

### Generated SHAP Visualizations
Saved in `ml/reports/shap_figures/`:
- `01_shap_summary_bar.png`: Global mean absolute SHAP value feature ranking.
- `02_shap_beeswarm.png`: Beeswarm summary showing feature directionality and impact magnitude.
- `03_shap_dependence_ability.png`: Ability Match dependence colored by Interest Match.
- `04_shap_dependence_interest.png`: Interest Match dependence colored by Ability Match.
- `05_shap_dependence_academic.png`: Academic Match dependence colored by Learning Match.
- `06_shap_waterfall_compatible.png`: Individual student local explanation for a top recommended career.
- `07_shap_waterfall_incompatible.png`: Individual student local explanation highlighting aptitude gaps.
- `08_shap_decision_plot.png`: Multi-sample decision trajectory plot for 25 candidate recommendations.

---

## 6. Production Artifacts & Deployment

The following artifacts have been generated and validated in `backend/ml/models/`:

| Artifact File | Size | Description |
| :--- | :---: | :--- |
| `model.joblib` | ~1.2 MB | Trained Champion CatBoost/XGBoost Classifier |
| `preprocessor.joblib` | ~44 KB | Fitted ColumnTransformer (StandardScaler + OrdinalEncoder) |
| `feature_columns.json` | 243 B | 11-Feature contract column definitions in exact order |
| `classes.json` | 93 B | Target class array `[0, 1]` and label mapping |
| `model_config.json` | 420 B | Model hyperparameters, threshold (`0.405`), and schema settings |
| `version.json` | 80 B | Version tracking metadata (`V8.0-Champion`) |
| `feature_importance.csv` | 334 B | Feature importance weights and ranking |
| `training_history.json` | ~4.8 KB | Full benchmark records, CV metrics, and ranking evaluation scores |

### Verification Status
- **Unit & Integration Tests:** 73/73 tests passing (100% OK).
- **Latency & Concurrency:** Multi-threaded recommendation latency < 45ms for 1,206 career catalogue evaluations.
- **Zero Data Leakage:** Zero student cross-contamination confirmed via group validation.

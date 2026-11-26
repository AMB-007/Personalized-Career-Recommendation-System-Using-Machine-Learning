# End-to-End Integration & Verification Report

**Project:** Personalized Career Recommendation System for Class 7–12 Students  
**Model:** XGBoost Career Compatibility & Ranking Engine (`V19.0-XGBoost-SMOTE-91pct`)  
**Date:** 2026-11-26  
**Status:** **25/25 ML & E2E TESTS VERIFIED**

---

## 1. Environment & Runtime

- **Operating System:** Windows (PowerShell Shell)
- **Python Version:** 3.11.9
- **Framework:** Flask 3.x, Flask-SQLAlchemy 3.1+, Flask-Login 0.6+
- **Machine Learning Packages:** XGBoost 3.2.0, LightGBM 4.7.0, Scikit-Learn 1.9.1, imbalanced-learn 0.14.2, Joblib 1.6.0, Pandas, NumPy, SHAP 0.51.0
- **Database Engine:** MySQL Server 8.x (with isolated SQLite test runner)

---

## 2. Canonical Production Model Version

- **Canonical Version:** `V19.0-XGBoost-SMOTE-91pct` (Authoritative from `version.json` and `model_config.json`)
- **Algorithm:** `XGBoost` (`xgboost.sklearn.XGBClassifier`)
- **Test Classification Accuracy:** `91.35%` (9,873 unseen test pairs, 80/20 student-grouped split)
- **5-Fold Stratified Group CV Accuracy:** `90.86% (± 0.44%)` (`96.97%` ROC-AUC)
- **Top-1 Recommendation Accuracy (Hit@1):** `99.43%`
- **Target Label:** Real `compatibility_label` (`0` = Not Compatible, `1` = Compatible)

---

## 3. Model Artifact Integrity Verification (SHA-256)

All production artifacts in `backend/ml/models/` and `backend/ml/data/` are verified against recorded SHA-256 hashes in `tests/reports/model_artifact_integrity.json`:

| Artifact File | Size (Bytes) | SHA-256 Checksum | Status |
| :--- | :--- | :--- | :--- |
| `model.joblib` | 2,467,796 | `7bd2c6f9e469cdc3f1786a0412e79a7dbf64d251b3f7436cd22d3600b56b9bd4` | **VERIFIED** |
| `preprocessor.joblib` | 9,592 | `d13c5921bf5507ddbe95abb9e333101c64f1873c19746af27a9634c6c3d271b2` | **VERIFIED** |
| `classes.json` | 4,326 | `7e82040df7e282d3f41d2bc1902d0aeff3902b189bd572de9f6f6ec11f207b1b` | **VERIFIED** |
| `model_config.json` | 985 | `53219d79e7c2bd015abde6d0780419abfaf8ed04d1ee009ad71df1c2359c0b62` | **VERIFIED** |
| `model_metadata.json` | 3,770 | `52b69e588d4a0ddb0ff66a8b9393e12ea2f3511075660e4d95386d6e056c4ecd` | **VERIFIED** |
| `version.json` | 207 | `a4b2f0bfe67fce2a981fd8836a07823cae99ca038501c18ba958c35c383063d0` | **VERIFIED** |
| `training_history.json` | 3,086 | `0f1f427e2c72ff040d7134c87b39001c3dbd41484fc47354caa66b13fac017d3` | **VERIFIED** |
| `career_knowledge_requirements.csv` | 121,292 | `c20948d0c7309e041177be9410b463b2bed950c8c311fdd883fa8088c9438f4b` | **VERIFIED** |

---

## 4. Feature Contract & Selection Summary

- **Emitted Candidate Schema (`get_feature_columns()`):** 22 fields (`age`, `class`, 12 base/derived numerical metrics, 5 engineered interaction features, and 3 nominal categories `stream`, `career_domain`, `career_name`).
- **Trained Preprocessor Selected Features (`20`):**
  - 17 Numerical (`ability_match_component`, `interest_match_component`, `academic_match_component`, `learning_match_component`, `composite_alignment_index`, `ability_interest_synergy`, `ability_interest_gap`, `min_core_match`, `max_core_match`, `harmonic_core_match`, `geometric_core_synergy`, `holistic_synergy`, `academic_learning_avg`, `component_mean_4d`, `component_std_4d`, `alignment_to_gap_ratio`, `weighted_synergy_index`)
  - 3 Nominal Categoricals (`stream`, `career_domain`, `career_name`)
- **Dropped/Pruned Columns:** `student_id`, `career_id`, `career_subdomain`, `career_cluster`, `age`, `class`, `ability_to_interest_ratio`.

---

## 5. Career Knowledge Catalogue & Performance Benchmarks

- **Total Careers in Catalogue:** `158` (100% alignment with dataset career names)
- **Measured Latency (`tests/reports/inference_performance.json`):**
  - **Feature Building (158 candidates):** `100.84 ms`
  - **XGBoost Inference (158 pairs):** `85.01 ms`
  - **Full End-to-End Recommendation Pipeline:** `229.36 ms`
  - **Multi-Thread Concurrency (5 & 10 concurrent requests):** `PASS`

---

## 6. Model Evaluation Summary

| Metric Type | Metric Name | Value |
| :--- | :--- | :--- |
| **Recommendation Ranking (Untouched Test Students)** | **Hit@1 (Top 1 Accuracy)** | **99.43%** |
| | **Hit@3** | **99.95%** |
| | **Hit@5** | **100.00%** |
| | **Hit@10** | **100.00%** |
| | **Mean Reciprocal Rank (MRR)** | **0.9970** |
| | **NDCG@5** | **0.9905** |
| **Binary Compatibility Classification (N_test = 9,873)** | **Test Accuracy** | **91.35%** |
| | **Balanced Accuracy** | **89.87%** |
| | **Decisive Accuracy (\|P - 0.5\| >= 0.25)** | **95.83%** |
| | **Precision** | **95.01%** |
| | **Recall** | **93.06%** |
| | **F1-Score** | **0.9403** |
| | **ROC-AUC** | **97.03%** |
| | **PR-AUC** | **98.91%** |

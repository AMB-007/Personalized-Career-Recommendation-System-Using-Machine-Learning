# REST API Examples: Personalized Career Recommendation System

This document contains real examples of API requests and responses from the Personalized Career Recommendation System powered by the **V7.2 XGBoost ML Model**.

---

## 1. System Health Check

### Request
```http
GET /api/health HTTP/1.1
Host: localhost:5000
Accept: application/json
```

### Response
```json
{
  "success": true,
  "message": null,
  "data": {
    "status": "healthy",
    "model_loaded": true,
    "preprocessor_loaded": true,
    "career_catalogue_loaded": true,
    "database": true,
    "algorithm": "XGBoost",
    "model_version": "V7.2"
  },
  "meta": null
}
```

---

## 2. Model Metadata & Verified Performance Metrics

### Request
```http
GET /api/model/info HTTP/1.1
Host: localhost:5000
Accept: application/json
```

### Response
```json
{
  "success": true,
  "message": null,
  "data": {
    "status": "loaded",
    "algorithm": "XGBoost",
    "model_version": "V7.2",
    "feature_count": 11,
    "features": [
      "age",
      "class",
      "ability_match_component",
      "interest_match_component",
      "academic_match_component",
      "learning_match_component",
      "career_name",
      "career_domain",
      "career_subdomain",
      "career_cluster",
      "stream"
    ],
    "threshold": 0.495,
    "created_at": "2026-08-26T04:01:10.307761Z",
    "classification_metrics": {
      "accuracy": 0.8099,
      "balanced_accuracy": 0.7171,
      "precision": 0.8321,
      "recall": 0.9240,
      "f1_score": 0.8756,
      "roc_auc": 0.8525,
      "pr_auc": 0.9348
    },
    "recommendation_metrics": {
      "hit_at_1": 0.9618,
      "hit_at_3": 0.9968,
      "hit_at_5": 0.9988,
      "hit_at_10": 0.9994,
      "mrr": 0.9798,
      "ndcg_at_5": 0.9212
    }
  },
  "meta": null
}
```

---

## 3. Direct ML Compatibility Prediction

### Request
```http
POST /api/predictions HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "features": [
    {
      "age": 17,
      "class": 12,
      "ability_match_component": 79.6,
      "interest_match_component": 60.23,
      "academic_match_component": 90.9,
      "learning_match_component": 54.7,
      "career_name": "Cloud Systems Architect",
      "career_domain": "Technology",
      "career_subdomain": "Cloud Infrastructure",
      "career_cluster": "Cluster 14",
      "stream": "Science-PCM"
    }
  ]
}
```

### Response
```json
{
  "success": true,
  "message": "Predictions generated successfully.",
  "data": {
    "model": "XGBoost",
    "version": "V7.2",
    "threshold": 0.495,
    "count": 1,
    "probabilities": [
      0.978214
    ],
    "predictions": [
      1
    ]
  },
  "meta": null
}
```

---

## 4. Personalized Career Recommendation (Standalone Profile)

### Request
```http
POST /api/recommendations HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "student_id": "STU001",
  "age": 17,
  "class_level": 12,
  "stream": "Science-PCM",
  "academic_percentage": 92.5,
  "top_k": 5,
  "scores": {
    "mathematical_ability": 94.0,
    "logical_reasoning": 96.0,
    "scientific_reasoning": 91.0,
    "problem_solving": 90.0,
    "analytical_ability": 92.0,
    "communication": 78.0,
    "creativity": 75.0,
    "digital_ability": 95.0,
    "learning_ability": 90.0,
    "technology_interest": 98.0,
    "engineering_interest": 95.0,
    "healthcare_interest": 30.0,
    "business_interest": 50.0,
    "finance_interest": 60.0,
    "arts_interest": 25.0,
    "design_interest": 70.0,
    "research_interest": 85.0,
    "environment_interest": 40.0,
    "agriculture_interest": 20.0
  }
}
```

### Response
```json
{
  "success": true,
  "message": "Recommendations generated successfully.",
  "data": {
    "model": "XGBoost Career Compatibility Model",
    "model_version": "V7.2",
    "student_id": "STU001",
    "total_evaluated_careers": 1206,
    "top_1": {
      "rank": 1,
      "career_id": "CAR01130",
      "career_name": "Software & AI Solutions Architect",
      "career_domain": "Technology",
      "career_subdomain": "Artificial Intelligence",
      "career_cluster": "Enterprise Systems",
      "compatibility_score": 99.83,
      "probability": 0.998315,
      "is_compatible": 1,
      "minimum_education_level": "Undergraduate",
      "ability_match_score": 91.45,
      "interest_match_score": 88.2,
      "recommendation_reason": "XGBoost Compatibility Score: 99.83% alignment across Technology aptitude benchmarks (91.45%) and disciplinary interests (88.2%).",
      "strengths": "Strong compatibility in Technology core aptitudes and Enterprise Systems functional track.",
      "skill_gaps": "Prepare for Undergraduate requirements and master essential competencies for Software & AI Solutions Architect."
    },
    "top_3": [ ... ],
    "top_5": [ ... ],
    "top_10": [ ... ],
    "recommendations": [ ... ]
  },
  "meta": null
}
```

---

## 5. Assessment Session Recommendation Generation

### Request
```http
POST /api/recommendations HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Cookie: session=...

{
  "session_id": 1,
  "top_k": 5
}
```

### Response
```json
{
  "success": true,
  "message": "Recommendations generated successfully.",
  "data": {
    "model": "XGBoost",
    "model_version": "V7.2",
    "assessment_id": 1,
    "student_id": "STU000001",
    "recommendations": [
      {
        "id": 1,
        "assessment_id": 1,
        "career_id": 2,
        "rank_position": 1,
        "score": 90.0,
        "recommendation_reason": "Exploratory Career Match (XGBoost ML): 90.0% alignment across Technology aptitude benchmarks (65.62%) and disciplinary interests (78.6%).",
        "strengths": "High aptitude synergy with Technology core competencies and career requirements.",
        "skill_gaps": "Focus on Bachelor's in CS prerequisites and specialized skill development for Cloud Software Architect."
      }
    ]
  },
  "meta": null
}
```

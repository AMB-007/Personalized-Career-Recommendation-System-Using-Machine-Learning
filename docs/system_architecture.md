# System Architecture Documentation

## Overview
The **Personalized Career Recommendation Platform** is an enterprise-grade academic major project designed for students in Classes 7 to 12.

```
                              ┌────────────────────────────────────────┐
                              │            Web Browser Client          │
                              │   HTML5, CSS3, JavaScript, Chart.js    │
                              └───────────────────┬────────────────────┘
                                                  │ HTTP (REST + Forms)
                                                  ▼
                              ┌────────────────────────────────────────┐
                              │           Flask Application Core       │
                              │  - Auth & Role-Based Access Control    │
                              │  - Application Factory & Config        │
                              └───────┬──────────────┬──────────────┬──┘
                                      │              │              │
                    ┌─────────────────┘              │              └─────────────────┐
                    ▼                                ▼                                ▼
      ┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
      │  Assessment Engine Layer  │    │   Scoring Service Layer   │    │   Career Knowledge Base   │
      │  - Grade Adaptive Loading │    │  - Normalization (0-100)  │    │  - Domain Hierarchy       │
      │  - Multi-format Stepper   │    │  - Cognitive Dimensions   │    │  - 5-Step Roadmaps        │
      │  - Autosave Controller    │    │  - Interest Aggregations  │    │  - Skill & Subject Matrix │
      └─────────────┬─────────────┘    └─────────────┬─────────────┘    └─────────────┬─────────────┘
                    │                                │                                │
                    └────────────────────────┬───────┴────────────────────────────────┘
                                             │
                                             ▼
                              ┌────────────────────────────────────────┐
                              │      Recommendation Service Layer      │
                              │  - Consumes ml/model_interface.py      │
                              │  - Baseline Heuristic Match Engine     │
                              │  - Pluggable ML Model Loader           │
                              └───────────────────┬────────────────────┘
                                                  │
                                                  ▼
                              ┌────────────────────────────────────────┐
                              │         Relational Database            │
                              │    MySQL (schema.sql & seed.sql) /     │
                              │       Flask-SQLAlchemy Entities        │
                              └────────────────────────────────────────┘
```

## Architectural Layers

1. **Presentation Layer (Frontend):**
   - Built with Semantic HTML5, Vanilla CSS Design System, Bootstrap 5 components, and Vanilla JavaScript.
   - Dynamic Chart.js visualizations for spider/radar cognitive plots and interest bar graphs.
   - Fully responsive for Desktop, Laptop, Tablet, and Mobile viewports.

2. **Application & Routing Layer (Flask Blueprints):**
   - `auth_bp`: Registration, login, logout, password hashing, session management.
   - `student_bp`: Dashboard, student profile, academic marks updates.
   - `assessment_bp`: Adaptive questionnaire delivery, answer persistence, submission, and scoring.
   - `career_bp`: Career explorer, domain queries, career detail profiles, education roadmaps.
   - `admin_bp`: Role-protected question bank and career management CRUD.

3. **Domain Services Layer:**
   - `AssessmentService`: Controls lifecycle of sessions and class filtering (`class_min <= student_class <= class_max`).
   - `ScoringService`: Normalizes multi-dimensional raw points to 0–100 scales and assigns educational guidance bands.
   - `CareerService`: Multi-filter search engine for careers, prerequisites, and milestone roadmaps.
   - `RecommendationService`: Invokes the ML model interface and persists Top-K recommendation rankings.

4. **Data Persistence Layer:**
   - 17 structured relational entities managed via Flask-SQLAlchemy with complete MySQL DDL (`database/schema.sql`).

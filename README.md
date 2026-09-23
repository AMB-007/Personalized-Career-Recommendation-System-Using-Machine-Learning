# PathFinder — Personalized Career Recommendation System

A machine learning–powered web application that recommends the most suitable careers to students based on their aptitude, interests, and academic profile. Students complete a short adaptive assessment, and the system ranks compatible careers using a trained LightGBM classifier.

---

## What This Project Does

- Students register, fill their academic profile (Class 7–12, stream, subject marks), and take an adaptive assessment (~50 questions).
- Their answers are scored across 22 dimensions, forming a 17-feature numerical vector.
- A trained ML model predicts a **compatibility score** for each of 158 careers and returns a **personalised Top-5 career list** with match percentages.
- Admins can manage careers, view assessments, and monitor system metrics from a dedicated dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11+, Flask 3.x |
| **Database** | MySQL 8.x via SQLAlchemy |
| **ML Engine** | LightGBM (champion), XGBoost, Random Forest |
| **ML Toolkit** | scikit-learn, SHAP, pandas, numpy |
| **Frontend** | Jinja2 templates, Vanilla CSS, JavaScript |
| **Auth** | Flask-Login, Flask-Bcrypt |
| **Notebook** | Jupyter (`model_training/model_90plus.ipynb`) |

### ML Model Performance

| Model | Accuracy | F1-Score | ROC-AUC | Train Time |
|---|---|---|---|---|
| **LightGBM** *(Champion)* | **91.59%** | **0.9417** | **97.13%** | 21.4s |
| XGBoost | 91.35% | 0.9401 | 97.16% | 20.7s |
| Random Forest | 90.74% | 0.9341 | 97.01% | 172.7s |

---

## Project Structure

```
├── backend/
│   ├── app.py                  # Flask app factory
│   ├── config.py               # Environment configs
│   ├── ml/
│   │   ├── models/             # Trained model artifacts (.joblib)
│   │   ├── feature_builder.py  # 17-feature vector construction
│   │   ├── prediction_service.py
│   │   └── recommendation_service.py
│   ├── models/                 # SQLAlchemy ORM models
│   ├── routes/                 # Flask Blueprints
│   └── services/               # Business logic layer
├── database/
│   ├── setup.sql               # MySQL schema (6 tables)
│   └── seed.py                 # Seeds questions & careers
├── frontend/
│   ├── templates/              # Jinja2 HTML templates
│   └── static/                 # CSS, JS, icons
├── model_training/
│   ├── model_90plus.ipynb      # Full EDA → training → evaluation notebook
│   └── model.joblib            # Exported champion model
├── Datasets/
│   └── Student Career Recommendation Dataset.csv
├── figures/                    # All 14 EDA & model evaluation figures
├── scripts/                    # Utility scripts (career sync, DB export)
├── tests/                      # 20+ unit & integration tests
├── requirements.txt
└── run.py                      # App entry point
```

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- MySQL 8.x running locally
- Git

### 1. Clone the repository
```bash
git clone https://github.com/AMB-007/Personalized-Career-Recommendation-System-Using-Machine-Learning.git
cd Personalized-Career-Recommendation-System-Using-Machine-Learning
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Create a `.env` file in the project root:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_recommendation_db
DATABASE_URL=mysql+mysqlconnector://root:your_mysql_password@localhost:3306/career_recommendation_db
```

### 4. Set up the database
```bash
# Create schema in MySQL
mysql -u root -p < database/setup.sql

# Seed questions and career data
python database/seed.py
```

### 5. Run the application
```bash
python run.py
```

Open your browser at **http://127.0.0.1:5000**

---

## ML Notebook

The complete machine learning pipeline is documented in [`model_training/model_90plus.ipynb`](model_training/model_90plus.ipynb), covering:

1. Dataset ingestion & EDA (14 visualisation figures)
2. Label engineering with weighted z-score composite
3. Preprocessing pipeline (StandardScaler + OHE)
4. Multi-model training & benchmark (LightGBM vs XGBoost vs Random Forest)
5. Champion model evaluation (Confusion matrix, ROC, PR curves)
6. SHAP feature importance analysis

To retrain from scratch:
```bash
python scripts/run_model_training.py
```

---

## UML Architecture Diagrams

| Diagram | Preview |
|---|:---:|
| Use Case Diagram | ![](figures/use_case_diagram.png) |
| Activity Diagram | ![](figures/activity_diagram.png) |
| Sequence Diagram | ![](figures/sequence_diagram.png) |
| Class Diagram | ![](figures/class_diagram.png) |

---

## Running Tests

```bash
python -m unittest discover tests/
```

---

## License

This project is developed as an academic final-year project.

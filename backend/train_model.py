"""
train_model.py — Retrain XGBoost model from the cleaned CSV dataset
Saves: xgboost_model.pkl, label_encoder.pkl, feature_columns.pkl
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'model', 'career_recommendation_dataset_cleaned.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')

print("Loading dataset...")
df = pd.read_csv(CSV_PATH)
print(f"Dataset shape: {df.shape}")

# ── Target column ──────────────────────────────────────────────────────────
TARGET = 'Recommended_Career'

# ── Drop non-feature columns ───────────────────────────────────────────────
DROP_COLS = [
    'Student_ID', TARGET,
    # computed score columns (derived, not input)
    'Academic_Performance_Score', 'Total_Technical_Skill_Score',
    'Soft_Skill_Score', 'Digital_Literacy_Score', 'Domain_Skill_Score',
    'STEM_Strength_Score', 'Business_Aptitude_Score', 'Creativity_Score',
    'Leadership_Score', 'Career_Readiness_Score',
    # subject-studied boolean flags (redundant with grade cols)
    'Mathematics_Studied', 'Science_Studied', 'English_Studied',
    'Social_Science_Studied', 'Second_Language_Studied', 'Physics_Studied',
    'Chemistry_Studied', 'Biology_Studied', 'Computer_Science_Studied',
    'Accountancy_Studied', 'Business_Studies_Studied', 'Economics_Studied',
    'Statistics_Studied', 'History_Studied', 'Political_Science_Studied',
    'Geography_Studied', 'Psychology_Studied',
]

feature_cols = [c for c in df.columns if c not in DROP_COLS]
X = df[feature_cols].copy()
y = df[TARGET].copy()

print(f"Feature count: {len(feature_cols)}")
print(f"Career classes: {y.nunique()}")

# ── Encode categorical features ────────────────────────────────────────────
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"Categorical columns to encode: {len(cat_cols)}")

cat_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    X[col] = X[col].fillna('Unknown')
    X[col] = le.fit_transform(X[col].astype(str))
    cat_encoders[col] = le

# Fill any remaining NaNs
X = X.fillna(0)

# ── Encode target ──────────────────────────────────────────────────────────
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"Classes: {list(label_encoder.classes_)}")

# ── Train/test split ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# ── Train XGBoost ──────────────────────────────────────────────────────────
print("\nTraining XGBoost model...")
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='mlogloss',
    random_state=42,
    n_jobs=-1,
    verbosity=1
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=50
)

# ── Evaluate ───────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc * 100:.2f}%")

# ── Save model artifacts ───────────────────────────────────────────────────
os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, 'xgboost_model.pkl'), 'wb') as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, 'label_encoder.pkl'), 'wb') as f:
    pickle.dump(label_encoder, f)

with open(os.path.join(MODEL_DIR, 'feature_columns.pkl'), 'wb') as f:
    pickle.dump({
        'feature_cols': feature_cols,
        'cat_cols': cat_cols,
        'cat_encoders': cat_encoders,
    }, f)

print("\nModel saved to model/")
print("   xgboost_model.pkl")
print("   label_encoder.pkl")
print("   feature_columns.pkl")
print(f"\nFeature columns ({len(feature_cols)}):")
print(feature_cols)

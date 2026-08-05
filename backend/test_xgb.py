import xgboost as xgb
base = "d:/Career_Recommendation_System/backend/models/"
try:
    model = xgb.XGBClassifier()
    model.load_model(base + "career_model.pkl")
    print("XGBClassifier loaded successfully via load_model")
except Exception as e:
    print("XGBClassifier load_model error:", e)

try:
    booster = xgb.Booster()
    booster.load_model(base + "career_model.pkl")
    print("Booster loaded successfully via load_model")
except Exception as e:
    print("Booster load_model error:", e)

import joblib
base = "d:/Career_Recommendation_System/backend/models/"
try:
    model = joblib.load(base + "career_model.pkl")
    print("Loaded with joblib successfully")
    print("Model type:", type(model))
except Exception as e:
    print("joblib load error:", e)

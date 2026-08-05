import pickle
import pandas as pd
import numpy as np
import xgboost as xgb

base = "d:/Career_Recommendation_System/backend/models/"
try:
    model = pickle.load(open(base + "career_model.pkl", "rb"))
    le = pickle.load(open(base + "label_encoder.pkl", "rb"))
    print("Models loaded successfully")
    print("Model type:", type(model))
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()

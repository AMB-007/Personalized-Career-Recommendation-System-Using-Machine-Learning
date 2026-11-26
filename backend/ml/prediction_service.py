"""
Prediction Service Module.
Executes batch model inference with consistent feature engineering and thresholding.
"""

from typing import Any, Dict, Union, List
import numpy as np
import pandas as pd
from backend.ml.feature_engineering import (
    add_engineered_features,
    clean_categorical_series,
    clean_numeric_series,
    clean_stream_value,
)
from backend.ml.model_loader import (
    ModelLoader,
    get_model,
    get_preprocessor,
    get_model_config,
)

# Align Career Knowledge Catalogue domain labels with training domain taxonomy
DOMAIN_ALIAS_MAP = {
    'information technology': 'Technology',
    'healthcare & life sciences': 'Healthcare',
    'healthcare & engineering': 'Healthcare',
    'arts & creative design': 'Arts & Design',
    'finance & commerce': 'Finance',
    'business & management': 'Business',
    'governance & public policy': 'Government & Public Service',
    'defense & security': 'Defence & Security',
    'education & training': 'Education',
    'law & legal services': 'Law',
    'science & research': 'Research',
    'sports & fitness': 'Sports',
    'trades & technical services': 'Skilled Trades',
    'aviation & aerospace': 'Aviation',
    'architecture & planning': 'Architecture & Construction',
    'agriculture & life sciences': 'Agriculture',
    'energy & environment': 'Energy',
    'hospitality & culinary arts': 'Hospitality & Tourism',
}


class PredictionService:
    """Manages feature transformation and model predictions."""

    REQUIRED_BASE_COLS = [
        'age', 'class', 'ability_match_component', 'interest_match_component',
        'academic_match_component', 'learning_match_component', 'career_name'
    ]

    @classmethod
    def _normalize_domain(cls, val: Any) -> Any:
        if pd.isna(val):
            return np.nan
        raw = str(val).strip()
        mapped = DOMAIN_ALIAS_MAP.get(raw.lower())
        return mapped if mapped else raw.title()

    @classmethod
    def predict_compatibility(cls, features_data: Union[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transforms input feature matrix and predicts compatibility probabilities.
        """
        if isinstance(features_data, list):
            if not features_data:
                raise ValueError("Input features list cannot be empty.")
            df = pd.DataFrame(features_data)
        elif isinstance(features_data, dict):
            df = pd.DataFrame([features_data])
        elif isinstance(features_data, pd.DataFrame):
            if features_data.empty:
                raise ValueError("Input features DataFrame cannot be empty.")
            df = features_data.copy()
        else:
            raise ValueError("Unsupported features format. Expected DataFrame or list of dicts.")

        missing = [col for col in cls.REQUIRED_BASE_COLS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required feature columns: {missing}")

        # Sanitize base numeric component columns
        for col in ['ability_match_component', 'interest_match_component', 'academic_match_component', 'learning_match_component']:
            df[col] = clean_numeric_series(df[col]).clip(lower=0.0, upper=100.0)

        # Compute derived and engineered features consistently with training
        df = add_engineered_features(df, include_candidates=False)

        # Normalize nominal categorical columns consistently with training
        if 'stream' in df.columns:
            df['stream'] = df['stream'].apply(clean_stream_value)
        else:
            df['stream'] = np.nan

        if 'career_domain' in df.columns:
            df['career_domain'] = clean_categorical_series(df['career_domain']).apply(cls._normalize_domain)
        else:
            df['career_domain'] = np.nan

        df['career_name'] = clean_categorical_series(df['career_name'])

        model = get_model()
        preprocessor = get_preprocessor()
        config = get_model_config()

        X_proc = preprocessor.transform(df)
        probs = model.predict_proba(X_proc)[:, 1]

        threshold = float(config.get('threshold', 0.5))
        predictions = [1 if float(p) >= threshold else 0 for p in probs]

        return {
            'probabilities': [round(float(p), 4) for p in probs],
            'predictions': predictions,
            'threshold': threshold,
            'version': ModelLoader.get_model_version().get('version', 'V19.0-XGBoost-SMOTE'),
            'count': len(probs)
        }

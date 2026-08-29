"""
Production ML Prediction Service Module.
Executes preprocessing and XGBoost compatibility model inference.
Strictly decoupled from database operations.
"""

from typing import Dict, List, Any, Union
import numpy as np
import pandas as pd
from backend.ml.model_loader import (
    get_model,
    get_preprocessor,
    get_feature_columns,
    get_model_config,
    get_model_version,
    ModelArtifactError
)


class PredictionService:
    """Coordinates preprocessing and model scoring for career compatibility vectors."""

    @classmethod
    def predict_compatibility(
        cls,
        feature_df: Union[pd.DataFrame, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Executes end-to-end ML inference on prepared candidate feature rows:
        1. Validates required feature columns.
        2. Applies preprocessor.joblib (imputation + scaling + encoding).
        3. Runs model.joblib (XGBoost Classifier).
        4. Applies decision threshold.
        5. Returns structured compatibility probabilities and predictions.
        """
        if isinstance(feature_df, list):
            feature_df = pd.DataFrame(feature_df)

        if not isinstance(feature_df, pd.DataFrame) or feature_df.empty:
            raise ValueError("Feature input must be a non-empty DataFrame or list of dicts.")

        # Graceful auto-computation of engineered alignment features if base features provided
        if 'composite_alignment_index' not in feature_df.columns and 'ability_match_component' in feature_df.columns:
            a_val = feature_df['ability_match_component'].fillna(50.0).astype(float)
            i_val = feature_df['interest_match_component'].fillna(50.0).astype(float)
            ac_val = feature_df['academic_match_component'].fillna(80.0).astype(float)
            l_val = feature_df['learning_match_component'].fillna(50.0).astype(float)
            feature_df['composite_alignment_index'] = np.round(
                0.17 * (0.4447 * a_val + 0.3136 * i_val + 0.0997 * ac_val + 0.1007 * l_val + 3.784) +
                0.83 * (0.45 * a_val + 0.35 * i_val + 0.10 * ac_val + 0.10 * l_val),
                2
            )
            feature_df['ability_interest_synergy'] = np.round((a_val * i_val) / 100.0, 2)
            feature_df['ability_interest_gap'] = np.round(np.abs(a_val - i_val), 2)
            feature_df['min_core_match'] = np.minimum(a_val, i_val)
            feature_df['max_core_match'] = np.maximum(a_val, i_val)
            feature_df['harmonic_core_match'] = np.round(2.0 * (a_val * i_val) / (a_val + i_val + 1e-5), 2)

        required_features = get_feature_columns()
        missing_cols = [c for c in required_features if c not in feature_df.columns]
        if missing_cols:
            raise ValueError(f"Feature schema violation: Missing required columns: {missing_cols}")

        # Ensure correct column ordering
        x_in = feature_df[required_features].copy()

        # 1. Transform using trained preprocessor (NEVER fit on inference data)
        preprocessor = get_preprocessor()
        try:
            x_trans = np.asarray(preprocessor.transform(x_in), dtype=np.float32)
        except Exception as e:
            raise RuntimeError(f"Preprocessing transformation failed: {str(e)}") from e

        # 2. Score with trained XGBoost model
        model = get_model()
        config = get_model_config()
        version_info = get_model_version()
        threshold = float(config.get('threshold', 0.495))

        try:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(x_trans)[:, 1]
            else:
                raw_pred = model.predict(x_trans)
                proba = raw_pred.astype(float)

            proba_list = [round(float(p), 6) for p in proba]
            pred_list = [int(p >= threshold) for p in proba]

            return {
                "model": config.get("model", "XGBoost"),
                "version": version_info.get("version", "V7.2"),
                "threshold": threshold,
                "count": len(proba_list),
                "probabilities": proba_list,
                "predictions": pred_list
            }

        except Exception as e:
            raise RuntimeError(f"XGBoost inference execution failed: {str(e)}") from e

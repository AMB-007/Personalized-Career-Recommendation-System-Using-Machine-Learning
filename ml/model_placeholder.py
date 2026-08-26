"""
ML Model Compatibility Wrapper.
Wraps the production V7.1/V7.2 XGBoost Career Compatibility Engine in backend/ml/
while preserving backward-compatibility with the legacy CareerModelInterface.
"""

from typing import Dict, List, Any, Optional
from ml.model_interface import CareerModelInterface
from backend.ml.recommendation_service import CareerRecommendationEngine
from backend.ml.model_loader import get_feature_columns, is_model_ready


class CareerModelPlaceholder(CareerModelInterface):
    """
    Production-ready wrapper routing to backend.ml.recommendation_service.
    Maintains backward compatibility with legacy interface callers.
    """

    def __init__(self):
        self.is_loaded = is_model_ready()
        self.model_type = "XGBoost Career Compatibility Model (V7.2 Production Engine)"

    def load_model(self, model_path: Optional[str] = None) -> bool:
        """Loads the production XGBoost model."""
        self.is_loaded = is_model_ready()
        return True

    def get_feature_names(self) -> List[str]:
        """Returns the 11 feature names expected by the model contract."""
        return get_feature_columns()

    def predict(self, feature_dict: Dict[str, Any]) -> Dict[str, float]:
        """Calculates normalized compatibility probabilities for careers."""
        res = CareerRecommendationEngine.generate_recommendations(feature_dict, top_k=25)
        return {item['career_id']: item['probability'] for item in res['recommendations']}

    def predict_top_k(self, feature_dict: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
        """
        Evaluates student profile and returns Top K ranked career paths.
        """
        res = CareerRecommendationEngine.generate_recommendations(feature_dict, top_k=k)
        top_results = []
        for item in res['recommendations']:
            top_results.append({
                "rank": item['rank'],
                "career_code": item['career_id'],
                "career_name": item['career_name'],
                "score": item['compatibility_score'],
                "reason": item['recommendation_reason']
            })
        return top_results

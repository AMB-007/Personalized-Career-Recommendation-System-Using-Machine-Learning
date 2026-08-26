"""
ML Model Interface Specification.
Defines the standard contract for career prediction models (XGBoost, CatBoost, LightGBM).
Ensures that integrating a real ML model later requires zero changes to the frontend or routes.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple


class CareerModelInterface(ABC):
    """Abstract Base Class defining the Machine Learning Model interface for Career Recommendations."""

    @abstractmethod
    def load_model(self, model_path: Optional[str] = None) -> bool:
        """
        Loads the trained model weights and metadata from storage.
        Supported formats for future models:
        - XGBoost: .json / .ubj / .model
        - CatBoost: .cbm / .bin
        - LightGBM: .txt / .pkl
        """
        pass

    @abstractmethod
    def predict(self, feature_dict: Dict[str, Any]) -> Dict[str, float]:
        """
        Takes processed student feature vector and returns probability/match scores
        for all registered career target classes.
        Returns: Dict mapping career_code -> probability (0.0 to 1.0)
        """
        pass

    @abstractmethod
    def predict_top_k(self, feature_dict: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
        """
        Predicts top K recommended careers with match confidence and rationale insights.
        Returns: List of dicts containing:
        - career_code: str
        - score: float (0.0 to 100.0)
        - rank: int (1 to K)
        - reason: str (Explanatory match insights)
        """
        pass

    @abstractmethod
    def get_feature_names(self) -> List[str]:
        """Returns the ordered list of required feature names expected by the model."""
        pass

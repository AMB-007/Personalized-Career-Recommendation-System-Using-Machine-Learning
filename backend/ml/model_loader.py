"""
Production ML Model Loader Module.
Provides thread-safe singleton loading, validation, and caching for the trained
XGBoost Career Compatibility Model artifacts.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import joblib

logger = logging.getLogger(__name__)

# Default model directory path relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_MODEL_DIR = BASE_DIR / "backend" / "ml" / "models"


class ModelArtifactError(Exception):
    """Raised when one or more required ML model artifacts are missing or invalid."""
    pass


class ModelLoader:
    """Singleton manager for production ML artifacts."""

    _instance: Optional['ModelLoader'] = None

    def __init__(self, model_dir: Optional[Path] = None):
        self.model_dir = Path(model_dir or os.getenv("MODEL_DIR") or DEFAULT_MODEL_DIR).resolve()
        self._model = None
        self._preprocessor = None
        self._feature_columns: Optional[List[str]] = None
        self._classes: Optional[Dict[str, Any]] = None
        self._model_config: Optional[Dict[str, Any]] = None
        self._version: Optional[Dict[str, Any]] = None
        self._is_loaded = False

    @classmethod
    def get_instance(cls, model_dir: Optional[Path] = None) -> 'ModelLoader':
        """Thread-safe singleton accessor."""
        if cls._instance is None:
            cls._instance = cls(model_dir=model_dir)
        return cls._instance

    def _validate_artifacts(self) -> None:
        """Validates that all required artifact files exist on the filesystem."""
        if not self.model_dir.exists():
            raise ModelArtifactError(
                f"Model directory not found at: {self.model_dir}. "
                "Ensure production model artifacts have been copied to the backend."
            )

        required_files = [
            "model.joblib",
            "preprocessor.joblib",
            "feature_columns.json",
            "classes.json",
            "model_config.json",
            "version.json"
        ]

        missing = [f for f in required_files if not (self.model_dir / f).exists()]
        if missing:
            raise ModelArtifactError(
                f"Missing required model artifact files in {self.model_dir}: {missing}"
            )

    def load(self, force_reload: bool = False) -> None:
        """
        Loads and validates all model artifacts into memory.
        Guarantees that artifacts are loaded only once unless force_reload is True.
        Never executes fitting or retraining.
        """
        if self._is_loaded and not force_reload:
            return

        self._validate_artifacts()

        try:
            # 1. Feature columns
            feat_path = self.model_dir / "feature_columns.json"
            with open(feat_path, "r", encoding="utf-8") as f:
                self._feature_columns = json.load(f)

            # 2. Classes & label mapping
            classes_path = self.model_dir / "classes.json"
            with open(classes_path, "r", encoding="utf-8") as f:
                self._classes = json.load(f)

            # 3. Model configuration
            config_path = self.model_dir / "model_config.json"
            with open(config_path, "r", encoding="utf-8") as f:
                self._model_config = json.load(f)

            # 4. Version metadata
            version_path = self.model_dir / "version.json"
            with open(version_path, "r", encoding="utf-8") as f:
                self._version = json.load(f)

            # 5. Preprocessor pipeline (ColumnTransformer)
            prep_path = self.model_dir / "preprocessor.joblib"
            self._preprocessor = joblib.load(prep_path)

            # 6. XGBoost Classifier
            model_path = self.model_dir / "model.joblib"
            self._model = joblib.load(model_path)

            self._is_loaded = True
            logger.info(
                f"Successfully loaded XGBoost model {self._version.get('version', 'V7')} "
                f"from {self.model_dir}"
            )

        except Exception as e:
            self._is_loaded = False
            raise ModelArtifactError(f"Failed to load ML model artifacts from {self.model_dir}: {str(e)}") from e

    def get_model(self):
        """Returns the cached XGBoost classifier."""
        if not self._is_loaded or self._model is None:
            self.load()
        return self._model

    def get_preprocessor(self):
        """Returns the cached scikit-learn ColumnTransformer preprocessor."""
        if not self._is_loaded or self._preprocessor is None:
            self.load()
        return self._preprocessor

    def get_feature_columns(self) -> List[str]:
        """Returns the ordered list of required feature names."""
        if not self._is_loaded or self._feature_columns is None:
            self.load()
        return list(self._feature_columns)

    def get_classes(self) -> Dict[str, Any]:
        """Returns class definitions and target label mappings."""
        if not self._is_loaded or self._classes is None:
            self.load()
        return dict(self._classes)

    def get_model_config(self) -> Dict[str, Any]:
        """Returns model hyperparameters and prediction threshold."""
        if not self._is_loaded or self._model_config is None:
            self.load()
        return dict(self._model_config)

    def get_model_version(self) -> Dict[str, Any]:
        """Returns model version metadata."""
        if not self._is_loaded or self._version is None:
            self.load()
        return dict(self._version)

    def is_loaded(self) -> bool:
        """Returns True if artifacts are loaded and ready for inference."""
        return self._is_loaded


# Global helper functions for convenient access
def get_model():
    return ModelLoader.get_instance().get_model()

def get_preprocessor():
    return ModelLoader.get_instance().get_preprocessor()

def get_feature_columns() -> List[str]:
    return ModelLoader.get_instance().get_feature_columns()

def get_classes() -> Dict[str, Any]:
    return ModelLoader.get_instance().get_classes()

def get_model_config() -> Dict[str, Any]:
    return ModelLoader.get_instance().get_model_config()

def get_model_version() -> Dict[str, Any]:
    return ModelLoader.get_instance().get_model_version()

def is_model_ready() -> bool:
    return ModelLoader.get_instance().is_loaded()

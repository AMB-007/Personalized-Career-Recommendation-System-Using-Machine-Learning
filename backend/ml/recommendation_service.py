"""
Production ML Career Recommendation Service.
Evaluates student assessment profiles against the complete 1,206 Career Knowledge
catalogue using the V7.2 XGBoost Model and produces ranked Top-K recommendations.
"""

import os
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from backend.ml.feature_builder import FeatureBuilder
from backend.ml.prediction_service import PredictionService
from backend.ml.model_loader import get_model_version, get_model_config

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_CAREER_DATA_PATH = BASE_DIR / "backend" / "ml" / "data" / "career_knowledge_requirements.csv"



class CareerRecommendationEngine:
    # Load configuration for domain thresholds and interest weighting
    _config_cache = None

    @classmethod
    def _load_config(cls):
        if cls._config_cache is None:
            config_path = Path(__file__).resolve().parent / "config.yaml"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    cls._config_cache = yaml.safe_load(f) or {}
            else:
                cls._config_cache = {}
        return cls._config_cache
    """Manages full career catalogue scoring, ranking, and Top-K extraction."""

    _catalogue: Optional[pd.DataFrame] = None
    _catalogue_path: Optional[Path] = None

    @classmethod
    def get_career_catalogue(cls, data_path: Optional[Path] = None) -> pd.DataFrame:
        """Loads and caches the 1,206 career knowledge requirements dataset."""
        if cls._catalogue is not None:
            return cls._catalogue

        path = Path(data_path or os.getenv("CAREER_DATA_PATH") or DEFAULT_CAREER_DATA_PATH).resolve()
        if not path.exists():
            raise FileNotFoundError(
                f"Career knowledge requirements dataset not found at {path}. "
                "Ensure career_knowledge_requirements.csv is placed in backend/ml/data/"
            )

        df = pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]
        cls._catalogue = df
        cls._catalogue_path = path
        logger.info(f"CAREER_CATALOGUE_LOADED: {len(df)} careers from {path}")
        return cls._catalogue

    @classmethod
    def generate_recommendations(
        cls,
        student_profile: Dict[str, Any],
        top_k: int = 10,
        data_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Generates ranked career recommendations for a student:
        1. Loads complete career knowledge catalogue (1,206 careers).
        2. Constructs 11-feature contract candidate matrix (1,206 rows).
        3. Preprocesses and predicts compatibility probabilities via XGBoost.
        4. Applies prerequisite domain threshold verification from config.yaml.
        5. Ranks careers descending by compatibility score.
        6. Deduplicates on career_id for Top-K extraction.
        7. Extracts Top 1, Top 3, Top 5, Top 10 recommendations.
        """
        catalogue = cls.get_career_catalogue(data_path)
        if catalogue.empty:
            raise ValueError("Career knowledge catalogue is empty.")

        total_evaluated = len(catalogue)
        logger.debug(f"PREDICTION_STARTED: Evaluating {total_evaluated} career candidates")

        # 1. Build batch features for all catalogue careers (1,206 candidates)
        features_df = FeatureBuilder.build_batch_features(student_profile, catalogue)
        assert len(features_df) == total_evaluated, "Candidate count mismatch with catalogue"

        # 2. Run model predictions
        pred_results = PredictionService.predict_compatibility(features_df)
        probs = pred_results['probabilities']
        preds = pred_results['predictions']

        # 3. Attach scores to catalogue items
        catalogue_scored = catalogue.copy()
        catalogue_scored['probability'] = probs
        catalogue_scored['compatibility_score'] = [round(p * 100.0, 2) for p in probs]
        catalogue_scored['is_compatible'] = preds
        catalogue_scored['ability_match'] = features_df['ability_match_component'].values
        catalogue_scored['interest_match'] = features_df['interest_match_component'].values

        # 4. Domain & prerequisite threshold compliance check
        cfg = cls._load_config()
        domain_cfg = cfg.get('domain_requirements', {})
        default_cfg = cfg.get('default_requirements', {})

        def _is_compliant(row):
            domain = str(row.get('career_domain', '')).lower()
            thresholds = domain_cfg.get(domain, default_cfg)
            for field, min_val in thresholds.items():
                if row.get(field) is not None:
                    try:
                        if float(row[field]) < float(min_val):
                            return 0
                    except (ValueError, TypeError):
                        return 0
            return 1

        catalogue_scored['threshold_pass'] = catalogue_scored.apply(_is_compliant, axis=1)

        # 5. Sort descending by compliance, compatibility probability, ability & interest match
        catalogue_sorted = catalogue_scored.sort_values(
            by=['threshold_pass', 'probability', 'ability_match', 'interest_match'],
            ascending=[False, False, False, False]
        )

        # 6. Deduplicate unique careers for Top-K extraction
        catalogue_distinct = catalogue_sorted.drop_duplicates(subset=['career_id'], keep='first').reset_index(drop=True)

        version_info = get_model_version()
        k_val = min(top_k, len(catalogue_distinct))

        recommendations_list = []
        for rank in range(1, k_val + 1):
            row = catalogue_distinct.iloc[rank - 1]
            c_name = str(row.get('career_name', 'Career'))
            c_dom = str(row.get('career_domain', 'General'))
            c_sub = str(row.get('career_subdomain', 'General'))
            c_clu = str(row.get('career_cluster', 'General'))
            score = float(row['compatibility_score'])
            config = cls._load_config()
            model_name = config.get('model', 'CatBoost')
            reason = (
                f"{model_name} Compatibility Score: {score}% alignment across {c_dom} "
                f"aptitude benchmarks ({row['ability_match']}%) and disciplinary interests ({row['interest_match']}%)."
            )
            strengths_desc = (
                f"Strong compatibility in {c_dom} core aptitudes and {c_clu} functional track."
            )
            gaps_desc = (
                f"Prepare for {row.get('minimum_education_level', 'Degree')} requirements and "
                f"master essential competencies for {c_name}."
            )

            rec_item = {
                'rank': rank,
                'career_id': str(row.get('career_id', f'CAR{rank:05d}')),
                'career_name': c_name,
                'career_domain': c_dom,
                'career_subdomain': c_sub,
                'career_cluster': c_clu,
                'compatibility_score': score,
                'probability': float(row['probability']),
                'is_compatible': int(row['is_compatible']),
                'minimum_education_level': str(row.get('minimum_education_level', 'Undergraduate')),
                'ability_match_score': float(row['ability_match']),
                'interest_match_score': float(row['interest_match']),
                'recommendation_reason': reason,
                'strengths': strengths_desc,
                'skill_gaps': gaps_desc
            }
            recommendations_list.append(rec_item)

        logger.debug(f"RECOMMENDATIONS_GENERATED: Extracted Top {len(recommendations_list)} recommendations")

        config = get_model_config()
        model_name = config.get('model', 'CatBoost')
        version_name = version_info.get('version', 'V8.0-Champion')

        return {
            'model': f"{model_name} Career Compatibility Model",
            'model_version': version_name,
            'student_id': student_profile.get('student_id') or student_profile.get('student_code'),
            'total_evaluated_careers': total_evaluated,
            'top_1': recommendations_list[0] if recommendations_list else None,
            'top_3': recommendations_list[:3],
            'top_5': recommendations_list[:5],
            'top_10': recommendations_list[:10],
            'recommendations': recommendations_list
        }

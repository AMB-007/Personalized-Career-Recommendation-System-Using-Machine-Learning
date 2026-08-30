"""
Production ML Feature Builder Module.
Transforms student questionnaire responses, normalized assessment scores, and career
knowledge requirements into the exact 11-feature contract expected by the V7.2
XGBoost Career Compatibility Model.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import yaml
import numpy as np
import pandas as pd
from backend.ml.model_loader import get_feature_columns

logger = logging.getLogger(__name__)

# stray _load_config removed (now defined inside FeatureBuilder class)


# 8 Primary Cognitive & Aptitude Dimensions for Ability Matching
PRIMARY_ABILITY_PAIRS = [
    ('mathematical_ability', 'required_mathematical_ability'),
    ('logical_reasoning', 'required_logical_reasoning'),
    ('scientific_reasoning', 'required_scientific_thinking'),
    ('problem_solving', 'required_problem_solving'),
    ('analytical_ability', 'required_analytical_thinking'),
    ('communication', 'required_communication'),
    ('creativity', 'required_creativity'),
    ('digital_ability', 'required_digital_ability'),
]

# 10 Disciplinary Interest Dimensions for Interest Matching
PRIMARY_INTEREST_PAIRS = [
    ('technology_interest', 'required_technology_interest'),
    ('engineering_interest', 'required_engineering_interest'),
    ('healthcare_interest', 'required_healthcare_interest'),
    ('business_interest', 'required_business_interest'),
    ('finance_interest', 'required_finance_interest'),
    ('arts_interest', 'required_arts_interest'),
    ('design_interest', 'required_design_interest'),
    ('research_interest', 'required_research_interest'),
    ('environment_interest', 'required_environment_interest'),
    ('agriculture_interest', 'required_agriculture_interest'),
]


class FeatureBuilder:
    """Builds and validates feature vectors for XGBoost compatibility inference."""

    @classmethod
    def _load_config(cls):
        """Load ``backend/ml/config.yaml`` once per process.

        Returns an empty dict if the file is missing.
        """
        config_path = Path(__file__).resolve().parent / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    @classmethod
    def _interest_weights(cls, student_scores: Dict[str, Any]) -> Dict[str, float]:
        """Return weighting factors for each interest.

        The top N interests (by student score) receive a boost factor defined in config.
        """
        cfg = cls._load_config()
        top_n = cfg.get('top_n_interests', 3)
        boost = cfg.get('interest_boost_factor', 1.5)
        # collect interest fields
        interest_fields = [field for field, _ in PRIMARY_INTEREST_PAIRS]
        scores = {field: cls._extract_student_interest_score(student_scores, field) for field in interest_fields}
        top_fields = sorted(scores, key=scores.get, reverse=True)[:top_n]
        weights = {field: 1.0 for field in interest_fields}
        for f in top_fields:
            weights[f] = boost
        return weights

    @staticmethod
    def _extract_student_ability_score(student_scores: Dict[str, Any], field_name: str) -> float:
        """Extracts ability score with aliased fallbacks (0-100 scale)."""
        aliases = {
            'scientific_reasoning': ['scientific_reasoning', 'scientific_thinking', 'science_score'],
            'analytical_ability': ['analytical_ability', 'analytical_thinking'],
            'communication': ['communication', 'communication_ability'],
            'digital_ability': ['digital_ability', 'digital_literacy'],
            'learning_ability': ['learning_ability', 'learning_agility']
        }
        for alias in aliases.get(field_name, [field_name]):
            if alias in student_scores and student_scores[alias] is not None:
                try:
                    val = float(student_scores[alias])
                    return max(0.0, min(100.0, val))
                except (ValueError, TypeError):
                    pass
        return 50.0

    @staticmethod
    def _extract_student_interest_score(student_scores: Dict[str, Any], field_name: str) -> float:
        """Extracts interest score with aliased fallbacks (0-100 scale)."""
        aliases = {
            'engineering_interest': ['engineering_interest', 'technology_interest', 'science_interest'],
            'arts_interest': ['arts_interest', 'creative_interest'],
            'design_interest': ['design_interest', 'creative_interest'],
            'environment_interest': ['environment_interest', 'science_interest'],
            'agriculture_interest': ['agriculture_interest', 'science_interest']
        }
        for alias in aliases.get(field_name, [field_name]):
            if alias in student_scores and student_scores[alias] is not None:
                try:
                    val = float(student_scores[alias])
                    return max(0.0, min(100.0, val))
                except (ValueError, TypeError):
                    pass
        return 50.0

    @classmethod
    def calculate_ability_match(
        cls,
        student_scores: Dict[str, Any],
        career_reqs: Dict[str, Any]
    ) -> float:
        """
        Computes 8-D ability match component (0.0 to 100.0) between student scores
        and career required abilities: mean(100 - |student - required|).
        """
        diffs = []
        for stu_field, car_field in PRIMARY_ABILITY_PAIRS:
            s_val = cls._extract_student_ability_score(student_scores, stu_field)
            c_val = float(career_reqs.get(car_field, 50.0) or 50.0)
            diffs.append(max(0.0, 100.0 - abs(s_val - c_val)))
        return round(float(np.mean(diffs)), 2)

    @classmethod
    def calculate_interest_match(
        cls,
        student_scores: Dict[str, Any],
        career_reqs: Dict[str, Any]
    ) -> float:
        """
        Computes 10-D interest match component (0.0 to 100.0) between student interests
        and career required interests: mean(100 - |student - required|).
        """
        diffs = []
        weights = cls._interest_weights(student_scores)
        for stu_field, car_field in PRIMARY_INTEREST_PAIRS:
            s_val = cls._extract_student_interest_score(student_scores, stu_field)
            c_val = float(career_reqs.get(car_field, 50.0) or 50.0)
            weight = weights.get(stu_field, 1.0)
            diffs.append(weight * max(0.0, 100.0 - abs(s_val - c_val)))
        # normalize by total weight sum to keep scale 0‑100
        total_weight = sum(weights.values())
        return round(float(np.mean(diffs) / total_weight * len(weights)), 2)

    @classmethod
    def build_candidate_feature_row(
        cls,
        student_profile: Dict[str, Any],
        career_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Constructs a single candidate feature row conforming to the 11-feature contract.
        NOTE: student_id is strictly NOT included.
        """
        scores = student_profile.get('scores', {})
        if not scores and 'abilities' in student_profile:
            scores = {**student_profile.get('abilities', {}), **student_profile.get('interests', {})}
            scores = {k: (v['score'] if isinstance(v, dict) else v) for k, v in scores.items()}

        academic = student_profile.get('academic', {})
        academic_score = float(
            student_profile.get('academic_percentage') or
            academic.get('overall_percentage') or
            scores.get('academic_percentage') or
            80.0
        )
        academic_score = max(0.0, min(100.0, academic_score))

        learning_score = cls._extract_student_ability_score(scores, 'learning_ability')

        age = int(student_profile.get('age') or 16)
        age = max(10, min(30, age))

        class_level = int(student_profile.get('class_level') or student_profile.get('class') or 10)
        class_level = max(7, min(12, class_level))

        stream = str(student_profile.get('stream') or academic.get('stream') or 'General')

        ability_match = cls.calculate_ability_match(scores, career_item)
        interest_match = cls.calculate_interest_match(scores, career_item)
        comp_align = round(0.45 * ability_match + 0.35 * interest_match + 0.10 * academic_score + 0.10 * learning_score, 2)
        ab_syn = round((ability_match * interest_match) / 100.0, 2)
        ab_gap = round(abs(ability_match - interest_match), 2)
        min_core = min(ability_match, interest_match)
        max_core = max(ability_match, interest_match)
        harm_core = round(2.0 * (ability_match * interest_match) / (ability_match + interest_match + 1e-5), 2)
        geom_syn = round(float(np.sqrt(max(0.0, ability_match * interest_match))), 2)
        hol_syn = round(float((ability_match * interest_match * academic_score * learning_score) ** 0.25), 2)

        row = {
            'age': age,
            'class': class_level,
            'ability_match_component': ability_match,
            'interest_match_component': interest_match,
            'academic_match_component': academic_score,
            'learning_match_component': learning_score,
            'composite_alignment_index': comp_align,
            'ability_interest_synergy': ab_syn,
            'ability_interest_gap': ab_gap,
            'min_core_match': min_core,
            'max_core_match': max_core,
            'harmonic_core_match': harm_core,
            'geometric_core_synergy': geom_syn,
            'holistic_synergy': hol_syn,
            'career_name': str(career_item.get('career_name', 'Professional Specialist')),
            'career_domain': str(career_item.get('career_domain', 'General')),
            'career_subdomain': str(career_item.get('career_subdomain', 'General')),
            'career_cluster': str(career_item.get('career_cluster', 'General')),
            'stream': stream
        }

        return row

    @classmethod
    def build_batch_features(
        cls,
        student_profile: Dict[str, Any],
        career_catalogue: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Efficiently constructs the candidate feature matrix for all careers in the catalogue
        using vectorized NumPy operations.
        Returns a DataFrame strictly matching the model feature contract.
        """
        expected_cols = get_feature_columns()
        n = len(career_catalogue)

        scores = student_profile.get('scores', {})
        if not scores and 'abilities' in student_profile:
            scores = {**student_profile.get('abilities', {}), **student_profile.get('interests', {})}
            scores = {k: (v['score'] if isinstance(v, dict) else v) for k, v in scores.items()}

        academic = student_profile.get('academic', {})
        academic_score = float(
            student_profile.get('academic_percentage') or
            academic.get('overall_percentage') or
            scores.get('academic_percentage') or
            80.0
        )
        academic_score = max(0.0, min(100.0, academic_score))

        learning_score = cls._extract_student_ability_score(scores, 'learning_ability')

        age = int(student_profile.get('age') or 16)
        age = max(10, min(30, age))

        class_level = int(student_profile.get('class_level') or student_profile.get('class') or 10)
        class_level = max(7, min(12, class_level))

        stream = str(student_profile.get('stream') or academic.get('stream') or 'General')

        # 1. Vectorized Ability Match (8 dimensions)
        ability_diffs = []
        for stu_field, car_field in PRIMARY_ABILITY_PAIRS:
            s_val = cls._extract_student_ability_score(scores, stu_field)
            if car_field in career_catalogue.columns:
                c_vals = career_catalogue[car_field].fillna(50.0).astype(float).values
            else:
                c_vals = np.full(n, 50.0, dtype=float)
            diff = np.maximum(0.0, 100.0 - np.abs(s_val - c_vals))
            ability_diffs.append(diff)
        ability_match_array = np.mean(ability_diffs, axis=0)

        # 2. Vectorized Interest Match (10 dimensions)
        interest_diffs = []
        for stu_field, car_field in PRIMARY_INTEREST_PAIRS:
            s_val = cls._extract_student_interest_score(scores, stu_field)
            if car_field in career_catalogue.columns:
                c_vals = career_catalogue[car_field].fillna(50.0).astype(float).values
            else:
                c_vals = np.full(n, 50.0, dtype=float)
            diff = np.maximum(0.0, 100.0 - np.abs(s_val - c_vals))
            interest_diffs.append(diff)
        interest_match_array = np.mean(interest_diffs, axis=0)

        # 3. Vectorized Composite Features
        comp_align_array = np.round(0.45 * ability_match_array + 0.35 * interest_match_array + 0.10 * academic_score + 0.10 * learning_score, 2)
        ab_syn_array = np.round((ability_match_array * interest_match_array) / 100.0, 2)
        ab_gap_array = np.round(np.abs(ability_match_array - interest_match_array), 2)
        min_core_array = np.minimum(ability_match_array, interest_match_array)
        max_core_array = np.maximum(ability_match_array, interest_match_array)
        harm_core_array = np.round(2.0 * (ability_match_array * interest_match_array) / (ability_match_array + interest_match_array + 1e-5), 2)
        geom_syn_array = np.round(np.sqrt(np.maximum(0.0, ability_match_array * interest_match_array)), 2)
        hol_syn_array = np.round((ability_match_array * interest_match_array * academic_score * learning_score) ** 0.25, 2)

        # Construct DataFrame
        df = pd.DataFrame({
            'age': np.full(n, age, dtype=int),
            'class': np.full(n, class_level, dtype=int),
            'ability_match_component': np.round(ability_match_array, 2),
            'interest_match_component': np.round(interest_match_array, 2),
            'academic_match_component': np.full(n, academic_score, dtype=float),
            'learning_match_component': np.full(n, learning_score, dtype=float),
            'composite_alignment_index': comp_align_array,
            'ability_interest_synergy': ab_syn_array,
            'ability_interest_gap': ab_gap_array,
            'min_core_match': min_core_array,
            'max_core_match': max_core_array,
            'harmonic_core_match': harm_core_array,
            'geometric_core_synergy': geom_syn_array,
            'holistic_synergy': hol_syn_array,
            'career_name': career_catalogue['career_name'].astype(str).values if 'career_name' in career_catalogue.columns else np.full(n, 'Professional Specialist', dtype=object),
            'career_domain': career_catalogue['career_domain'].astype(str).values if 'career_domain' in career_catalogue.columns else np.full(n, 'General', dtype=object),
            'career_subdomain': career_catalogue['career_subdomain'].astype(str).values if 'career_subdomain' in career_catalogue.columns else np.full(n, 'General', dtype=object),
            'career_cluster': career_catalogue['career_cluster'].astype(str).values if 'career_cluster' in career_catalogue.columns else np.full(n, 'General', dtype=object),
            'stream': np.full(n, stream, dtype=object)
        })

        # Enforce exact column order from feature_columns.json
        df = df[expected_cols]

        # Validation assertions
        assert list(df.columns) == expected_cols, f"Columns mismatch: {list(df.columns)} vs {expected_cols}"
        assert 'student_id' not in df.columns, "Security violation: student_id must NOT be passed to model"
        assert 'career_id' not in df.columns, "Feature violation: career_id must NOT be passed to model"

        return df

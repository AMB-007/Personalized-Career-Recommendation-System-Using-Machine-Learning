"""
Shared Feature Engineering & Data Cleaning Utilities.
Provides a single source of truth for data sanitization, deterministic
dataset-aligned match metrics, and engineered features across both
model training and production ML serving.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd

MISSING_SENTINELS = [
    '?', '-', '--', 'unknown', 'Unknown', 'UNKNOWN',
    'nan', 'NaN', 'NAN', 'none', 'None', 'NONE',
    'n/a', 'N/A', 'na', 'NA', 'null', 'Null', 'NULL', ''
]

RAW_NUMERIC_COLUMNS = [
    'age',
    'class',
    'ability_match_component',
    'interest_match_component',
    'academic_match_component',
    'learning_match_component',
    'composite_alignment_index',
    'ability_interest_synergy',
    'ability_interest_gap',
    'min_core_match',
    'max_core_match',
    'harmonic_core_match',
    'geometric_core_synergy',
    'holistic_synergy',
]

ENGINEERED_NUMERIC_COLUMNS = [
    'academic_learning_avg',
    'component_mean_4d',
    'component_std_4d',
    'alignment_to_gap_ratio',
    'weighted_synergy_index',
]

# Selected features retained after Correlation + Tree Importance + Permutation Importance
# (age, class, and ability_to_interest_ratio were pruned during feature selection;
#  student_id, career_id, career_subdomain, career_cluster were dropped as ID/noise columns).
SELECTED_NUMERIC_FEATURES = [
    'ability_match_component',
    'interest_match_component',
    'academic_match_component',
    'learning_match_component',
    'composite_alignment_index',
    'ability_interest_synergy',
    'ability_interest_gap',
    'min_core_match',
    'max_core_match',
    'harmonic_core_match',
    'geometric_core_synergy',
    'holistic_synergy',
    'academic_learning_avg',
    'component_mean_4d',
    'component_std_4d',
    'alignment_to_gap_ratio',
    'weighted_synergy_index',
]

SELECTED_CATEGORICAL_FEATURES = [
    'stream',
    'career_domain',
    'career_name',
]

# Full candidate schema emitted by FeatureBuilder for API/test contract compatibility
API_FEATURE_COLUMNS = [
    'age',
    'class',
    *SELECTED_NUMERIC_FEATURES,
    *SELECTED_CATEGORICAL_FEATURES,
]


def clean_stream_value(val: Any) -> Any:
    """Standardizes messy stream text (typos, casing, missing tokens) to canonical streams."""
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if v in {s.lower() for s in MISSING_SENTINELS} or v in {'general', 'all'}:
        return np.nan
    if 'sci' in v or 'scei' in v:
        return 'Science'
    if 'com' in v:
        return 'Commerce'
    if 'art' in v or 'arst' in v or 'human' in v:
        return 'Arts'
    return str(val).strip().title()


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """Converts numbers stored as dirty text (%, commas, sentinel tokens) to float64."""
    s = (
        series.astype(str)
        .str.strip()
        .str.replace('%', '', regex=False)
        .str.replace(',', '.', regex=False)
    )
    s = s.replace(MISSING_SENTINELS, np.nan)
    return pd.to_numeric(s, errors='coerce')


def clean_categorical_series(series: pd.Series) -> pd.Series:
    """Cleans whitespace, casing, and missing sentinel tokens in nominal text columns."""
    s = series.astype(str).str.strip()
    s = s.replace(MISSING_SENTINELS, np.nan)
    return s.where(s.isna(), s.str.title())


def compute_core_match_metrics(
    ability: float,
    interest: float,
    academic: float,
    learning: float,
) -> Dict[str, float]:
    """
    Computes the dataset-verified alignment & synergy metrics from the 4 core components.
    Formulas match the exact definitions observed in Student Career Recommendation Dataset.csv.
    """
    ab = float(ability)
    it = float(interest)
    ac = float(academic)
    lr = float(learning)

    comp_idx = (0.45 * ab) + (0.35 * it) + (0.10 * ac) + (0.10 * lr)
    synergy = (ab * it) / 100.0
    gap = abs(ab - it)
    min_core = min(ab, it)
    max_core = max(ab, it)
    denom = ab + it
    harmonic = (2.0 * ab * it / denom) if denom > 0 else 0.0
    geom = float(np.sqrt(max(ab * it, 0.0)))
    holistic = float(np.power(max(ab * it * ac * lr, 0.0), 0.25))

    return {
        'composite_alignment_index': round(comp_idx, 2),
        'ability_interest_synergy': round(synergy, 2),
        'ability_interest_gap': round(gap, 2),
        'min_core_match': round(min_core, 2),
        'max_core_match': round(max_core, 2),
        'harmonic_core_match': round(harmonic, 2),
        'geometric_core_synergy': round(geom, 2),
        'holistic_synergy': round(holistic, 2),
    }


def compute_engineered_scalar_features(
    ability: float,
    interest: float,
    academic: float,
    learning: float,
    composite_alignment_index: float,
    ability_interest_gap: float,
    holistic_synergy: float,
) -> Dict[str, float]:
    """Computes row-wise engineered features for a single student-career candidate."""
    ab = float(ability)
    it = float(interest)
    ac = float(academic)
    lr = float(learning)
    comp_idx = float(composite_alignment_index)
    gap = float(ability_interest_gap)
    holistic = float(holistic_synergy)

    vals_4d = np.array([ab, it, ac, lr], dtype=float)
    return {
        'academic_learning_avg': round((ac + lr) / 2.0, 4),
        'component_mean_4d': round(float(np.mean(vals_4d)), 4),
        'component_std_4d': round(float(np.std(vals_4d, ddof=1)), 4),
        'alignment_to_gap_ratio': round(comp_idx / (gap + 1.0), 4),
        'weighted_synergy_index': round((comp_idx * holistic) / 100.0, 4),
    }


def add_engineered_features(df: pd.DataFrame, include_candidates: bool = False) -> pd.DataFrame:
    """
    Computes missing base alignment metrics (if any) and engineered features
    on a DataFrame in a vectorized, row-wise, zero-leakage manner.
    """
    out = df.copy()

    ab = pd.to_numeric(out['ability_match_component'], errors='coerce')
    it = pd.to_numeric(out['interest_match_component'], errors='coerce')
    ac = pd.to_numeric(out['academic_match_component'], errors='coerce')
    lr = pd.to_numeric(out['learning_match_component'], errors='coerce')

    # Fill missing base derived features only if absent from raw dataframe
    if 'composite_alignment_index' not in out.columns:
        out['composite_alignment_index'] = (0.45 * ab) + (0.35 * it) + (0.10 * ac) + (0.10 * lr)
    if 'ability_interest_synergy' not in out.columns:
        out['ability_interest_synergy'] = (ab * it) / 100.0
    if 'ability_interest_gap' not in out.columns:
        out['ability_interest_gap'] = (ab - it).abs()
    if 'min_core_match' not in out.columns:
        out['min_core_match'] = np.minimum(ab, it)
    if 'max_core_match' not in out.columns:
        out['max_core_match'] = np.maximum(ab, it)
    if 'harmonic_core_match' not in out.columns:
        denom = ab + it
        out['harmonic_core_match'] = np.where(denom > 0, (2.0 * ab * it) / denom, 0.0)
    if 'geometric_core_synergy' not in out.columns:
        out['geometric_core_synergy'] = np.sqrt(np.maximum(ab * it, 0.0))
    if 'holistic_synergy' not in out.columns:
        out['holistic_synergy'] = np.power(np.maximum(ab * it * ac * lr, 0.0), 0.25)

    # Row-wise engineered interaction features
    if 'academic_learning_avg' not in out.columns:
        out['academic_learning_avg'] = (ac + lr) / 2.0
    if 'component_mean_4d' not in out.columns:
        out['component_mean_4d'] = (ab + it + ac + lr) / 4.0
    if 'component_std_4d' not in out.columns:
        comp_matrix = pd.concat([ab, it, ac, lr], axis=1)
        out['component_std_4d'] = comp_matrix.std(axis=1)
    if 'alignment_to_gap_ratio' not in out.columns:
        out['alignment_to_gap_ratio'] = (
            pd.to_numeric(out['composite_alignment_index'], errors='coerce')
            / (pd.to_numeric(out['ability_interest_gap'], errors='coerce') + 1.0)
        )
    if 'weighted_synergy_index' not in out.columns:
        out['weighted_synergy_index'] = (
            pd.to_numeric(out['composite_alignment_index'], errors='coerce')
            * pd.to_numeric(out['holistic_synergy'], errors='coerce')
        ) / 100.0

    if include_candidates and 'ability_to_interest_ratio' not in out.columns:
        out['ability_to_interest_ratio'] = ab / np.maximum(it, 1.0)

    return out

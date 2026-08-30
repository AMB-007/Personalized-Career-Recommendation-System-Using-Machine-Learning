"""
Test script to simulate the student profile from user screenshots and analyze prediction accuracy.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.ml.recommendation_service import CareerRecommendationEngine
from backend.ml.feature_builder import FeatureBuilder

def test_prediction():
    student_profile = {
        'age': 16,
        'class_level': 11,
        'stream': 'Science',
        'scores': {
            'mathematical_ability': 25.0,
            'logical_reasoning': 30.0,
            'scientific_reasoning': 20.0,
            'problem_solving': 45.0,
            'analytical_ability': 35.0,
            'communication': 65.0,
            'creativity': 55.0,
            'digital_ability': 50.0,
            'learning_ability': 20.0,
            'technology_interest': 65.0,
            'engineering_interest': 80.0,
            'healthcare_interest': 60.0,
            'business_interest': 70.0,
            'finance_interest': 72.0,
            'arts_interest': 60.0,
            'creative_interest': 60.0,
            'research_interest': 80.0,
        }
    }

    recs = CareerRecommendationEngine.generate_recommendations(student_profile, top_k=10)
    print("=== MODEL VERSION ===")
    print(recs.get('model_version'))
    print(f"Total evaluated: {recs.get('total_careers_evaluated')}")

    print("\n=== TOP 10 RECOMMENDATIONS ===")
    for r in recs['recommendations']:
        print(f"Rank #{r['rank']:2d}: {r['career_name']:<35s} | Domain: {r['career_domain']:<15s} | Score: {r['compatibility_score']:>5.1f}% | Prob: {r['probability']:.4f} | A_match: {r.get('ability_match_component')} | I_match: {r.get('interest_match_component')}")

    # Inspect Dentist specifically in catalogue
    catalogue = CareerRecommendationEngine.get_career_catalogue()
    dentist_row = catalogue[catalogue['career_name'].str.lower().str.contains('dentist')]
    print("\n=== DENTIST REQUIREMENT PROFILE ===")
    if not dentist_row.empty:
        for idx, row in dentist_row.iterrows():
            print(dict(row))

if __name__ == '__main__':
    test_prediction()

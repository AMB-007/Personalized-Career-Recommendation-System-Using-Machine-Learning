import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ml.recommendation_service import CareerRecommendationEngine

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
print(f"Total Evaluated: {recs.get('total_careers_evaluated')}")
print(f"Model Version: {recs.get('model_version')}")
print("-" * 80)
for r in recs['recommendations']:
    print(f"Rank #{r['rank']:2d}: {r['career_name']} | Domain: {r['career_domain']} | Score: {r['compatibility_score']}% | Prob: {r['probability']:.4f} | A_match: {r.get('ability_match_component')} | I_match: {r.get('interest_match_component')}")

"""
Assessment Scoring Service.
Computes normalized multi-dimensional cognitive aptitude, interest, and work preference scores (0-100 scale).
Categorizes scores into educational guidance bands (Very Low, Low, Average, Good, Excellent).
"""

from typing import Dict, Any, List, Union
from backend.extensions import db
from backend.models.assessment import AssessmentSession, StudentAnswer, AssessmentScore
from backend.models.question import Question, QuestionOption


class ScoringService:
    """Core assessment evaluation and normalization engine."""

    # Educational guidance score bands
    SCORE_BANDS = [
        (80.5, 100.0, "Excellent", "Demonstrates strong conceptual mastery and high affinity."),
        (60.5, 80.4, "Good", "Solid capability with positive aptitude indicators."),
        (40.5, 60.4, "Average", "Moderate proficiency with scope for further exploration and skill building."),
        (20.5, 40.4, "Low", "Developing foundational familiarity; supplementary practice recommended."),
        (0.0, 20.4, "Very Low", "Minimal demonstrated exposure or current interest.")
    ]

    @classmethod
    def get_score_category(cls, score: float) -> Dict[str, str]:
        """Convert a 0-100 numerical score into an educational guidance category and description."""
        score = max(0.0, min(100.0, score))
        for min_val, max_val, label, desc in cls.SCORE_BANDS:
            if min_val <= score <= max_val:
                return {'label': label, 'description': desc, 'score': round(score, 1)}
        return {'label': 'Average', 'description': 'Moderate proficiency.', 'score': round(score, 1)}

    @classmethod
    def calculate_and_save_scores(cls, session: Union[AssessmentSession, int]) -> AssessmentScore:
        """
        Calculates all cognitive, interest, and behavioral dimensions from student answers
        and saves/updates the AssessmentScore record in the database.
        """
        if isinstance(session, int):
            session_obj = db.session.get(AssessmentSession, session)
            if not session_obj:
                raise ValueError(f"AssessmentSession {session} not found.")
            session = session_obj

        answers = StudentAnswer.query.filter_by(assessment_id=session.id).all()
        
        # Track total points scored and maximum possible points per skill category
        category_scores: Dict[str, float] = {}
        category_max: Dict[str, float] = {}

        # Default list of all tracked cognitive and interest dimensions
        tracked_dimensions = [
            'mathematical_ability', 'logical_reasoning', 'scientific_reasoning',
            'problem_solving', 'analytical_ability', 'communication',
            'creativity', 'digital_ability', 'learning_ability', 'memory',
            'observation', 'spatial_ability', 'practical_ability', 'teamwork', 'leadership',
            'technology_interest', 'science_interest', 'healthcare_interest',
            'business_interest', 'creative_interest', 'research_interest', 'social_interest'
        ]

        for dim in tracked_dimensions:
            category_scores[dim] = 0.0
            category_max[dim] = 0.0

        for ans in answers:
            q = ans.question
            if not q or not q.skill_category:
                continue

            skill = q.skill_category

            if q.question_type in ['MCQ', 'SCENARIO']:
                # Find selected option score
                selected_opt = QuestionOption.query.filter_by(question_id=q.id, option_value=ans.selected_option).first()
                pts = selected_opt.score if selected_opt else 0.0
                max_pts = 1.0  # standard MCQ max

                category_scores[skill] = category_scores.get(skill, 0.0) + pts
                category_max[skill] = category_max.get(skill, 0.0) + max_pts

            elif q.question_type == 'RATING':
                # Rating scale (1 to 5) or numeric value
                val = ans.numeric_value
                if val is None and ans.selected_option:
                    try:
                        val = float(ans.selected_option)
                    except ValueError:
                        # Check if mapped option score exists
                        selected_opt = QuestionOption.query.filter_by(question_id=q.id, option_value=ans.selected_option).first()
                        val = selected_opt.score if selected_opt else 60.0

                if val is not None:
                    # Normalize 1-5 scale to 0-100 or use direct score if 0-100
                    normalized_val = val if val > 5 else (val / 5.0) * 100.0
                    category_scores[skill] = category_scores.get(skill, 0.0) + normalized_val
                    category_max[skill] = category_max.get(skill, 0.0) + 100.0

            elif q.question_type == 'MULTI_SELECT':
                # Multi-select options
                selected_vals = (ans.selected_option or '').split(',')
                opts = QuestionOption.query.filter_by(question_id=q.id).all()
                max_pts = sum(opt.score for opt in opts if opt.score > 0) or 1.0
                pts = sum(opt.score for opt in opts if opt.option_value in selected_vals)

                category_scores[skill] = category_scores.get(skill, 0.0) + pts
                category_max[skill] = category_max.get(skill, 0.0) + max_pts

        # Calculate final normalized percentage (0 - 100) for each dimension
        normalized_results: Dict[str, float] = {}
        for dim in tracked_dimensions:
            max_p = category_max.get(dim, 0.0)
            if max_p > 0:
                score_pct = (category_scores.get(dim, 0.0) / max_p) * 100.0
            else:
                # Default baseline value for unexplored dimensions
                score_pct = 50.0
            normalized_results[dim] = max(0.0, min(100.0, round(score_pct, 1)))

        # Update or create AssessmentScore record
        score_record = AssessmentScore.query.filter_by(assessment_id=session.id).first()
        if not score_record:
            score_record = AssessmentScore(assessment_id=session.id)
            db.session.add(score_record)

        for dim, val in normalized_results.items():
            if hasattr(score_record, dim):
                setattr(score_record, dim, val)

        db.session.commit()
        return score_record

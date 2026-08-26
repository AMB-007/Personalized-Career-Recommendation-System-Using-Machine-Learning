"""
Career Recommendation Service.
Coordinates the production V7.1/V7.2 XGBoost Career Compatibility Machine Learning Engine,
evaluates multi-dimensional student profile vectors, and persists Top-K personalized career
matches with detailed educational milestones, prerequisite subjects, and roadmaps in MySQL.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from backend.extensions import db
from backend.models.assessment import AssessmentSession, AssessmentScore, StudentAnswer
from backend.models.career import Career, CareerDomain, CareerSkill, CareerSubject, CareerEducation, CareerPathway
from backend.models.recommendation import CareerRecommendation
from backend.models.student import Student, AcademicScore
from backend.ml.recommendation_service import CareerRecommendationEngine
from backend.ml.feature_builder import FeatureBuilder
from backend.ml.prediction_service import PredictionService
from backend.ml.model_loader import get_model_version, is_model_ready


class RecommendationService:
    """Service layer coordinating production XGBoost career recommendations and explanations."""

    @classmethod
    def build_student_profile_dict(
        cls,
        session: AssessmentSession,
        score_record: Optional[AssessmentScore] = None,
        academic_record: Optional[AcademicScore] = None
    ) -> Dict[str, Any]:
        """Constructs standardized student profile dictionary for ML inference."""
        student = session.student
        if score_record is None:
            score_record = AssessmentScore.query.filter_by(assessment_id=session.id).first()
        if academic_record is None and student:
            academic_record = AcademicScore.query.filter_by(student_id=student.id).order_by(AcademicScore.created_at.desc()).first()

        scores_dict = {}
        if score_record:
            raw_data = score_record.to_dict()
            scores_dict.update(raw_data.get('cognitive_scores', {}))
            scores_dict.update(raw_data.get('interest_scores', {}))

        academic_pct = float(academic_record.overall_percentage) if academic_record and academic_record.overall_percentage is not None else 80.0

        return {
            'student_id': student.student_code if student else f'STU{session.student_id:06d}',
            'age': student.age if student and student.age else 16,
            'class_level': student.class_level if student and student.class_level else 10,
            'stream': student.stream if student and student.stream else 'General',
            'academic_percentage': academic_pct,
            'scores': scores_dict
        }

    @classmethod
    def generate_recommendations_for_session(
        cls,
        session: AssessmentSession,
        top_k: int = 5
    ) -> List[CareerRecommendation]:
        """
        Generates and persists top K career recommendations for a completed assessment session
        using the production V7.1/V7.2 XGBoost Career Compatibility model.
        """
        score_record = AssessmentScore.query.filter_by(assessment_id=session.id).first()
        student = session.student
        academic_record = AcademicScore.query.filter_by(student_id=student.id).order_by(AcademicScore.created_at.desc()).first() if student else None

        active_db_careers = Career.query.filter_by(is_active=True).all()
        if not active_db_careers:
            return []

        # 1. Build standardized student profile
        student_profile = cls.build_student_profile_dict(session, score_record, academic_record)

        # 2. Score active database careers via XGBoost feature builder & prediction service
        # This guarantees 100% foreign-key integrity with the MySQL database
        db_career_rows = []
        for c in active_db_careers:
            db_career_rows.append({
                'db_id': c.id,
                'career_code': c.career_code,
                'career_name': c.career_name,
                'career_domain': c.domain.domain_name if c.domain else 'General',
                'career_subdomain': c.subdomain.name if c.subdomain else 'General',
                'career_cluster': c.cluster.name if c.cluster else 'General',
                'minimum_education_level': c.minimum_education or 'Undergraduate',
                # Map domain/skills to required abilities/interests if available
                'required_mathematical_ability': 50.0,
                'required_logical_reasoning': 50.0,
                'required_scientific_thinking': 50.0,
                'required_problem_solving': 50.0,
                'required_analytical_thinking': 50.0,
                'required_communication': 50.0,
                'required_creativity': 50.0,
                'required_digital_ability': 50.0,
                'required_technology_interest': 50.0,
                'required_engineering_interest': 50.0,
                'required_healthcare_interest': 50.0,
                'required_business_interest': 50.0,
                'required_finance_interest': 50.0,
                'required_arts_interest': 50.0,
                'required_design_interest': 50.0,
                'required_research_interest': 50.0,
                'required_environment_interest': 50.0,
                'required_agriculture_interest': 50.0,
            })

        db_career_df = pd.DataFrame(db_career_rows)

        # Also merge with full 1,206 career knowledge catalogue requirements if matched by name
        try:
            full_catalogue = CareerRecommendationEngine.get_career_catalogue()
            if not full_catalogue.empty:
                cat_by_name = {str(row['career_name']).strip().lower(): row for _, row in full_catalogue.iterrows()}
                for idx, r in db_career_df.iterrows():
                    cname = str(r['career_name']).strip().lower()
                    if cname in cat_by_name:
                        cat_row = cat_by_name[cname]
                        for k in cat_row.index:
                            if k.startswith('required_'):
                                db_career_df.at[idx, k] = float(cat_row[k])
        except Exception:
            pass

        # Build feature DataFrame for DB careers
        feat_df = FeatureBuilder.build_batch_features(student_profile, db_career_df)

        # Run XGBoost inference
        pred_res = PredictionService.predict_compatibility(feat_df)
        probs = pred_res['probabilities']

        db_career_df['probability'] = probs
        db_career_df['score'] = [round(p * 100.0, 1) for p in probs]
        db_career_df['ability_match'] = feat_df['ability_match_component'].values
        db_career_df['interest_match'] = feat_df['interest_match_component'].values

        # Sort descending by XGBoost compatibility score
        sorted_careers = db_career_df.sort_values(by=['score', 'ability_match'], ascending=[False, False]).head(top_k)

        # 3. Clear prior recommendations for idempotency
        CareerRecommendation.query.filter_by(assessment_id=session.id).delete()

        persisted_recs = []
        for rank, (_, row) in enumerate(sorted_careers.iterrows(), start=1):
            c_id = int(row['db_id'])
            c_name = row['career_name']
            c_dom = row['career_domain']
            score_val = float(row['score'])

            reason_str = (
                f"Exploratory Career Match (XGBoost ML): {score_val}% alignment across {c_dom} "
                f"aptitude benchmarks ({row['ability_match']}%) and disciplinary interests ({row['interest_match']}%)."
            )
            strengths_str = (
                f"High aptitude synergy with {c_dom} core competencies and career requirements."
            )
            gaps_str = (
                f"Focus on {row['minimum_education_level']} prerequisites and specialized skill development for {c_name}."
            )

            rec_entry = CareerRecommendation(
                assessment_id=session.id,
                career_id=c_id,
                rank_position=rank,
                score=score_val,
                recommendation_reason=reason_str,
                strengths=strengths_str,
                skill_gaps=gaps_str
            )
            db.session.add(rec_entry)
            persisted_recs.append(rec_entry)

        db.session.commit()
        return persisted_recs

    @classmethod
    def get_recommendations_for_session(cls, session_id: int) -> List[Dict[str, Any]]:
        """Retrieves structured recommendation list for a session."""
        recs = CareerRecommendation.query.filter_by(assessment_id=session_id).order_by(CareerRecommendation.rank_position.asc()).all()
        return [r.to_dict() for r in recs]

    @classmethod
    def get_detailed_career_explanations(cls, session_id: int) -> List[Dict[str, Any]]:
        """
        Fetches recommendations with rich explanatory breakdowns pulling live details
        from MySQL `career_skills`, `career_subjects`, `career_education`, and `career_pathways`.
        """
        recs = CareerRecommendation.query.filter_by(assessment_id=session_id).order_by(CareerRecommendation.rank_position.asc()).all()
        detailed_list = []

        for r in recs:
            c = r.career
            if not c:
                continue

            # Fetch skills with importance
            skills_data = [
                {'skill_name': s.skill_name, 'importance': s.importance_level, 'label': s.importance_label}
                for s in CareerSkill.query.filter_by(career_id=c.id).order_by(CareerSkill.importance_level.desc()).all()
            ]

            # Fetch subjects with importance
            subjects_data = [
                {'subject_name': sub.subject_name, 'importance': sub.importance_level, 'label': sub.importance_label}
                for sub in CareerSubject.query.filter_by(career_id=c.id).order_by(CareerSubject.importance_level.desc()).all()
            ]

            # Fetch education milestones
            edu_milestones = [
                {'level': e.education_level, 'degree': e.degree_name, 'description': e.description, 'sequence': e.sequence_order}
                for e in CareerEducation.query.filter_by(career_id=c.id).order_by(CareerEducation.sequence_order.asc()).all()
            ]

            # Fetch progression stages
            pathway_stages = [
                {'stage_number': p.stage_number, 'stage_name': p.stage_name, 'description': p.description}
                for p in CareerPathway.query.filter_by(career_id=c.id).order_by(CareerPathway.stage_number.asc()).all()
            ]

            detailed_list.append({
                'rank': r.rank_position,
                'match_score': float(r.score) if r.score is not None else 0.0,
                'career_id': c.id,
                'career_code': c.career_code,
                'career_name': c.career_name,
                'domain_name': c.domain.domain_name if c.domain else 'General',
                'subdomain_name': c.subdomain.name if c.subdomain else 'General',
                'cluster_name': c.cluster.name if c.cluster else 'General',
                'description': c.description,
                'minimum_education': c.minimum_education,
                'typical_education': c.typical_education,
                'work_environment': c.work_environment,
                'work_style': c.work_style,
                'entry_level_role': c.entry_level_role,
                'advanced_role': c.advanced_role,
                'strengths': r.strengths,
                'skill_gaps': r.skill_gaps,
                'recommendation_reason': r.recommendation_reason,
                'skills': skills_data,
                'subjects': subjects_data,
                'education_milestones': edu_milestones,
                'progression_stages': pathway_stages
            })

        return detailed_list

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from backend.extensions import db


class CareerRecommendation(db.Model):
    """Career recommendation record linked to an assessment session in MySQL."""
    __tablename__ = 'career_recommendations'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('assessment_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    rank_position = db.Column(db.Integer, nullable=False, default=1, index=True)
    score = db.Column(db.Float, nullable=True)  # Match score / probability (0.0 to 100.0)
    recommendation_reason = db.Column(db.Text, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    skill_gaps = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('assessment_id', 'career_id', name='uq_assessment_career'),
    )

    # Relationships
    career = db.relationship('Career')

    @hybrid_property
    def rank(self):
        return self.rank_position

    @rank.setter
    def rank(self, val):
        self.rank_position = val

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'career_id': self.career_id,
            'career_name': self.career.career_name if self.career else None,
            'career_code': self.career.career_code if self.career else None,
            'domain_name': self.career.domain.domain_name if self.career and self.career.domain else None,
            'domain_icon': self.career.domain.icon if self.career and self.career.domain else 'bi-briefcase',
            'description': self.career.description if self.career else None,
            'rank': self.rank_position,
            'score': round(self.score, 1) if self.score is not None else 0.0,
            'recommendation_reason': self.recommendation_reason,
            'strengths': self.strengths,
            'skill_gaps': self.skill_gaps,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<CareerRecommendation Rank {self.rank_position}: Career {self.career_id} for Session {self.assessment_id}>"

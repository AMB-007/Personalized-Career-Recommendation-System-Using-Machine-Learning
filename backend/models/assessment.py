from datetime import datetime
from backend.extensions import db


class AssessmentSession(db.Model):
    """Student assessment session state and progress in MySQL."""
    __tablename__ = 'assessment_sessions'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(
        db.Enum('not_started', 'in_progress', 'completed', 'abandoned', name='session_status_enum'),
        default='not_started',
        index=True
    )
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    current_question = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    selected_question_ids = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    answers = db.relationship('StudentAnswer', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    scores = db.relationship('AssessmentScore', backref='session', uselist=False, cascade='all, delete-orphan')
    recommendations = db.relationship('CareerRecommendation', backref='session', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'current_question': self.current_question,
            'completion_percentage': self.completion_percentage,
            'selected_question_ids': self.selected_question_ids,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<AssessmentSession {self.id} - Student {self.student_id} ({self.status})>"


class StudentAnswer(db.Model):
    """Answers submitted by students during assessment sessions in MySQL."""
    __tablename__ = 'student_answers'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('assessment_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    question_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('questions.id', ondelete='RESTRICT'), nullable=False, index=True)
    selected_option_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('question_options.id', ondelete='SET NULL'), nullable=True)
    selected_option = db.Column(db.Text, nullable=True)
    answer_text = db.Column(db.Text, nullable=True)
    numeric_value = db.Column(db.Float, nullable=True)
    time_taken_seconds = db.Column(db.Integer, default=0)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Composite Unique Constraint: one answer per question per assessment
    __table_args__ = (
        db.UniqueConstraint('assessment_id', 'question_id', name='uq_assessment_question'),
    )

    # Relationships
    question = db.relationship('Question')
    option = db.relationship('QuestionOption')

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'question_id': self.question_id,
            'selected_option_id': self.selected_option_id,
            'selected_option': self.selected_option,
            'answer_text': self.answer_text,
            'numeric_value': self.numeric_value,
            'time_taken_seconds': self.time_taken_seconds,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None
        }


class AssessmentScore(db.Model):
    """Normalized multi-dimensional assessment scores (0-100 scale) in MySQL."""
    __tablename__ = 'assessment_scores'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('assessment_sessions.id', ondelete='CASCADE'), nullable=False, unique=True)

    # Cognitive & Aptitude abilities (0-100 scale)
    mathematical_ability = db.Column(db.Float, default=0.0)
    logical_reasoning = db.Column(db.Float, default=0.0)
    scientific_reasoning = db.Column(db.Float, default=0.0)
    problem_solving = db.Column(db.Float, default=0.0)
    analytical_ability = db.Column(db.Float, default=0.0)
    communication = db.Column(db.Float, default=0.0)
    creativity = db.Column(db.Float, default=0.0)
    digital_ability = db.Column(db.Float, default=0.0)
    learning_ability = db.Column(db.Float, default=0.0)
    memory = db.Column(db.Float, default=0.0)
    observation = db.Column(db.Float, default=0.0)
    spatial_ability = db.Column(db.Float, default=0.0)
    practical_ability = db.Column(db.Float, default=0.0)
    teamwork = db.Column(db.Float, default=0.0)
    leadership = db.Column(db.Float, default=0.0)

    # Interest dimensions (0-100 scale)
    technology_interest = db.Column(db.Float, default=0.0)
    science_interest = db.Column(db.Float, default=0.0)
    healthcare_interest = db.Column(db.Float, default=0.0)
    business_interest = db.Column(db.Float, default=0.0)
    creative_interest = db.Column(db.Float, default=0.0)
    research_interest = db.Column(db.Float, default=0.0)
    social_interest = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'cognitive_scores': {
                'mathematical_ability': round(self.mathematical_ability, 1),
                'logical_reasoning': round(self.logical_reasoning, 1),
                'scientific_reasoning': round(self.scientific_reasoning, 1),
                'problem_solving': round(self.problem_solving, 1),
                'analytical_ability': round(self.analytical_ability, 1),
                'communication': round(self.communication, 1),
                'creativity': round(self.creativity, 1),
                'digital_ability': round(self.digital_ability, 1),
                'learning_ability': round(self.learning_ability, 1),
                'memory': round(self.memory, 1),
                'observation': round(self.observation, 1),
                'spatial_ability': round(self.spatial_ability, 1),
                'practical_ability': round(self.practical_ability, 1),
                'teamwork': round(self.teamwork, 1),
                'leadership': round(self.leadership, 1)
            },
            'interest_scores': {
                'technology_interest': round(self.technology_interest, 1),
                'science_interest': round(self.science_interest, 1),
                'healthcare_interest': round(self.healthcare_interest, 1),
                'business_interest': round(self.business_interest, 1),
                'creative_interest': round(self.creative_interest, 1),
                'research_interest': round(self.research_interest, 1),
                'social_interest': round(self.social_interest, 1)
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<AssessmentScore for Assessment {self.assessment_id}>"

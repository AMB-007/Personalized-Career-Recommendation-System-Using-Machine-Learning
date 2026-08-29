from datetime import datetime, timezone
from backend.extensions import db


class QuestionSection(db.Model):
    """Sections/categories of the questionnaire stored in MySQL."""
    __tablename__ = 'question_sections'

    id = db.Column(db.Integer().with_variant(db.Integer, "mysql"), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=1)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationship
    questions = db.relationship('Question', backref='section', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'question_count': self.questions.filter_by(is_active=True).count()
        }

    def __repr__(self):
        return f"<QuestionSection {self.name}>"


class Question(db.Model):
    """Dynamic question model supporting adaptive class-level filtering in MySQL."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    question_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('question_sections.id', ondelete='RESTRICT'), nullable=False, index=True)
    question_type = db.Column(
        db.Enum('MCQ', 'MULTI_SELECT', 'RATING', 'SCENARIO', 'RANKING', name='question_type_enum'),
        nullable=False,
        default='MCQ'
    )
    class_min = db.Column(db.SmallInteger, nullable=False, default=7, index=True)
    class_max = db.Column(db.SmallInteger, nullable=False, default=12, index=True)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard', name='difficulty_enum'), default='Medium')
    skill_category = db.Column(db.String(100), nullable=True, index=True)
    stream_specific = db.Column(db.String(50), nullable=True, default='All')
    is_required = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    explanation = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    options = db.relationship('QuestionOption', backref='question', lazy='joined', cascade='all, delete-orphan', order_by='QuestionOption.display_order')

    def to_dict(self, include_correct=False):
        return {
            'id': self.id,
            'question_code': self.question_code,
            'question_text': self.question_text,
            'section_id': self.section_id,
            'section_name': self.section.name if self.section else None,
            'question_type': self.question_type,
            'class_min': self.class_min,
            'class_max': self.class_max,
            'difficulty': self.difficulty,
            'skill_category': self.skill_category,
            'stream_specific': self.stream_specific,
            'is_required': self.is_required,
            'display_order': self.display_order,
            'explanation': self.explanation if include_correct else None,
            'options': [opt.to_dict(include_correct=include_correct) for opt in self.options]
        }

    def __repr__(self):
        return f"<Question {self.question_code}: {self.question_text[:30]}...>"


class QuestionOption(db.Model):
    """Options for questions stored in MySQL."""
    __tablename__ = 'question_options'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False, index=True)
    option_text = db.Column(db.String(500), nullable=False)
    option_value = db.Column(db.String(100), nullable=True)
    score = db.Column(db.Float, default=0.0)
    is_correct = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)

    def to_dict(self, include_correct=False):
        data = {
            'id': self.id,
            'question_id': self.question_id,
            'option_text': self.option_text,
            'option_value': self.option_value,
            'display_order': self.display_order
        }
        if include_correct:
            data['score'] = self.score
            data['is_correct'] = self.is_correct
        return data

    def __repr__(self):
        return f"<QuestionOption {self.id}: {self.option_text[:20]}>"

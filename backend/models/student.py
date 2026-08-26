from datetime import datetime
from backend.extensions import db


class Student(db.Model):
    """Student profile model storing academic and educational demographics in MySQL."""
    __tablename__ = 'students'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    student_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.SmallInteger, nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    class_level = db.Column(db.SmallInteger, nullable=False, index=True)  # 7 to 12
    board = db.Column(db.String(100), nullable=True, index=True)  # CBSE, ICSE, State Board, IB, Cambridge
    medium = db.Column(db.String(50), nullable=True)  # English, Malayalam, Hindi, etc.
    academic_year = db.Column(db.String(20), nullable=True)
    stream = db.Column(db.String(100), nullable=True, default='General', index=True)  # General (7-10), Science-PCM, Science-PCB, Commerce, Humanities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    academic_scores = db.relationship('AcademicScore', backref='student', uselist=False, cascade='all, delete-orphan')
    assessments = db.relationship('AssessmentSession', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}".strip()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_code': self.student_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'age': self.age,
            'gender': self.gender,
            'class_level': self.class_level,
            'board': self.board,
            'medium': self.medium,
            'academic_year': self.academic_year,
            'stream': self.stream,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Student {self.student_code} - Class {self.class_level}>"


class AcademicScore(db.Model):
    """Academic subject marks and percentages for students in MySQL."""
    __tablename__ = 'academic_scores'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, unique=True)
    mathematics_score = db.Column(db.Float, nullable=True)
    science_score = db.Column(db.Float, nullable=True)
    physics_score = db.Column(db.Float, nullable=True)
    chemistry_score = db.Column(db.Float, nullable=True)
    biology_score = db.Column(db.Float, nullable=True)
    computer_science_score = db.Column(db.Float, nullable=True)
    english_score = db.Column(db.Float, nullable=True)
    malayalam_score = db.Column(db.Float, nullable=True)
    hindi_score = db.Column(db.Float, nullable=True)
    social_science_score = db.Column(db.Float, nullable=True)
    history_score = db.Column(db.Float, nullable=True)
    geography_score = db.Column(db.Float, nullable=True)
    political_science_score = db.Column(db.Float, nullable=True)
    economics_score = db.Column(db.Float, nullable=True)
    accountancy_score = db.Column(db.Float, nullable=True)
    business_studies_score = db.Column(db.Float, nullable=True)
    psychology_score = db.Column(db.Float, nullable=True)
    overall_percentage = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'mathematics_score': self.mathematics_score,
            'science_score': self.science_score,
            'physics_score': self.physics_score,
            'chemistry_score': self.chemistry_score,
            'biology_score': self.biology_score,
            'computer_science_score': self.computer_science_score,
            'english_score': self.english_score,
            'malayalam_score': self.malayalam_score,
            'hindi_score': self.hindi_score,
            'social_science_score': self.social_science_score,
            'history_score': self.history_score,
            'geography_score': self.geography_score,
            'political_science_score': self.political_science_score,
            'economics_score': self.economics_score,
            'accountancy_score': self.accountancy_score,
            'business_studies_score': self.business_studies_score,
            'psychology_score': self.psychology_score,
            'overall_percentage': self.overall_percentage
        }

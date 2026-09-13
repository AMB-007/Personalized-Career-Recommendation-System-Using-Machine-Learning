"""
Student Profile Model for MySQL Database.
Stores student educational demographics and academic marks directly in 'students' (Table 2 of 6),
eliminating redundant 1:1 separate academic_scores table.
"""

from datetime import datetime, timezone
from backend.extensions import db


class AcademicScoreProxy:
    """Compatibility proxy for student academic subject marks stored in JSON."""
    def __init__(self, data=None, student=None):
        self._data = dict(data) if isinstance(data, dict) else {}
        self._student = student

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._data:
            return self._data[name]
        return None

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            if self._student is not None:
                self._student.academic_scores_data = dict(self._data)

    def __getitem__(self, item):
        return self._data.get(item)

    def __setitem__(self, key, value):
        self._data[key] = value
        if self._student is not None:
            self._student.academic_scores_data = dict(self._data)

    @property
    def overall_percentage(self):
        return self._data.get('overall_percentage', 75.0)

    @overall_percentage.setter
    def overall_percentage(self, val):
        self._data['overall_percentage'] = float(val) if val is not None else 75.0
        if self._student is not None:
            self._student.academic_scores_data = dict(self._data)

    def to_dict(self):
        res = {
            'id': self._student.id if self._student else 1,
            'student_id': self._student.id if self._student else 1,
            'mathematics_score': self._data.get('mathematics_score'),
            'science_score': self._data.get('science_score'),
            'physics_score': self._data.get('physics_score'),
            'chemistry_score': self._data.get('chemistry_score'),
            'biology_score': self._data.get('biology_score'),
            'computer_science_score': self._data.get('computer_science_score'),
            'english_score': self._data.get('english_score'),
            'malayalam_score': self._data.get('malayalam_score'),
            'hindi_score': self._data.get('hindi_score'),
            'social_science_score': self._data.get('social_science_score'),
            'history_score': self._data.get('history_score'),
            'geography_score': self._data.get('geography_score'),
            'political_science_score': self._data.get('political_science_score'),
            'economics_score': self._data.get('economics_score'),
            'accountancy_score': self._data.get('accountancy_score'),
            'business_studies_score': self._data.get('business_studies_score'),
            'psychology_score': self._data.get('psychology_score'),
            'overall_percentage': self.overall_percentage
        }
        return res

    def __repr__(self):
        return f"<AcademicScore overall={self.overall_percentage}%>"


class Student(db.Model):
    """Student profile model storing demographics and academic scores in MySQL (Table 2 of 6)."""
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
    stream = db.Column(db.String(100), nullable=True, default='General', index=True)
    academic_scores_data = db.Column('academic_scores', db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    assessments = db.relationship('AssessmentSession', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def academic_scores(self):
        return AcademicScoreProxy(self.academic_scores_data or {}, self)

    @academic_scores.setter
    def academic_scores(self, value):
        if isinstance(value, dict):
            self.academic_scores_data = dict(value)
        elif isinstance(value, AcademicScoreProxy):
            self.academic_scores_data = dict(value._data)
        elif isinstance(value, AcademicScore):
            self.academic_scores_data = dict(value.to_dict())
        else:
            self.academic_scores_data = {}

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
            'stream': self.stream,
            'academic_scores': self.academic_scores.to_dict(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Student {self.student_code} - Class {self.class_level}>"


class _DummyScoreColumn:
    @staticmethod
    def desc():
        return None
    @staticmethod
    def asc():
        return None


class AcademicScore:
    """Compatibility interface for academic scores without a separate database table."""
    created_at = _DummyScoreColumn()

    def __init__(self, student_id=None, **kwargs):
        self.student_id = student_id
        self._data = dict(kwargs)
        if 'overall_percentage' not in self._data:
            self._data['overall_percentage'] = kwargs.get('overall_percentage', 75.0)

        # If student exists in session, attach directly
        if student_id and db.session:
            try:
                st = db.session.get(Student, student_id)
                if st:
                    current = dict(st.academic_scores_data or {})
                    current.update(self._data)
                    st.academic_scores_data = current
            except Exception:
                pass

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        if name in ('student_id', '_data'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            if self.student_id and db.session:
                try:
                    st = db.session.get(Student, self.student_id)
                    if st:
                        current = dict(st.academic_scores_data or {})
                        current[name] = value
                        st.academic_scores_data = current
                except Exception:
                    pass

    def to_dict(self):
        d = dict(self._data)
        d['student_id'] = self.student_id
        return d

    class _Query:
        @staticmethod
        def filter_by(student_id=None, **kwargs):
            class _QueryResult:
                def __init__(self, s_id):
                    self.s_id = s_id

                def first(self):
                    if not self.s_id or not db.session:
                        return None
                    try:
                        st = db.session.get(Student, self.s_id)
                        return st.academic_scores if st else None
                    except Exception:
                        return None

                def order_by(self, *args):
                    return self
            return _QueryResult(student_id)

    query = _Query()

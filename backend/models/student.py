"""
Student Profile Compatibility Interface for MySQL Database.
Consolidated directly into 'users' (Table 1 of 5), eliminating redundant 'students' table.
Provides full backwards compatibility for Student model, AcademicScoreProxy, and AcademicScore.
"""

from backend.extensions import db
from backend.models.user import User


class AcademicScoreProxy:
    """Compatibility proxy for student academic subject marks stored in JSON on User."""
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


# Student is an alias to User (Table 1 of 5), providing complete compatibility
Student = User


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

        # If user/student exists in session, attach directly
        if student_id and db.session:
            try:
                st = db.session.get(User, student_id)
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
                    st = db.session.get(User, self.student_id)
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
                        st = db.session.get(User, self.s_id)
                        return st.academic_scores if st else None
                    except Exception:
                        return None

                def order_by(self, *args):
                    return self
            return _QueryResult(student_id)

    query = _Query()

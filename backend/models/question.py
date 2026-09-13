"""
Dynamic Question Model for MySQL Database.
Stores adaptive assessment questions and choice options directly in 'questions' (Table 3 of 6),
eliminating redundant over-normalized question_sections and question_options tables.
"""

from datetime import datetime, timezone
from sqlalchemy.orm.attributes import flag_modified
from backend.extensions import db


_DEFAULT_SECTIONS = {
    1: 'Academic Profile',
    2: 'Mathematical Ability',
    3: 'Logical Reasoning',
    4: 'Scientific Thinking',
    5: 'Problem Solving',
    6: 'Analytical Thinking',
    7: 'Communication',
    8: 'Creativity',
    9: 'Digital Ability',
    10: 'Learning Ability',
    11: 'Spatial Ability',
    12: 'Practical Ability',
    13: 'Interests',
    14: 'Activities',
    15: 'Teamwork',
    16: 'Leadership',
    17: 'Work Preferences',
    18: 'Career Awareness',
    19: 'Career Preferences'
}

_SECTION_ID_TO_NAME = dict(_DEFAULT_SECTIONS)
_SECTION_NAME_TO_ID = {name.lower(): s_id for s_id, name in _DEFAULT_SECTIONS.items()}


class SectionProxy:
    """Compatibility proxy for a question category section."""
    def __init__(self, name="General", section_id=1, display_order=1):
        self.id = section_id
        self.name = name or "General"
        self.description = f"{self.name} Assessment Section"
        self.display_order = display_order
        self.is_active = True

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, SectionProxy):
            return self.name == other.name
        return self.name == str(other)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'question_count': Question.query.filter_by(section=self.name, is_active=True).count() if db.session else 0
        }

    def __repr__(self):
        return f"<QuestionSection {self.name}>"


class OptionProxy:
    """Compatibility proxy for multiple choice options stored in JSON."""
    def __init__(self, data, question_id=None, idx=1):
        if isinstance(data, dict):
            self.id = data.get('id', idx)
            self.question_id = question_id or data.get('question_id', 1)
            self.option_text = data.get('option_text', '')
            self.option_value = data.get('option_value', '')
            self.score = float(data.get('score', 0.0))
            self.is_correct = bool(data.get('is_correct', False))
            self.display_order = int(data.get('display_order', idx))
        else:
            self.id = idx
            self.question_id = question_id or 1
            self.option_text = str(data)
            self.option_value = str(data)
            self.score = 0.0
            self.is_correct = False
            self.display_order = idx

    def to_dict(self, include_correct=False):
        d = {
            'id': self.id,
            'question_id': self.question_id,
            'option_text': self.option_text,
            'option_value': self.option_value,
            'display_order': self.display_order
        }
        if include_correct:
            d['score'] = self.score
            d['is_correct'] = self.is_correct
        return d

    def __repr__(self):
        return f"<QuestionOption {self.id}: {self.option_text[:20]}>"


class Question(db.Model):
    """Dynamic question model supporting adaptive class-level filtering in MySQL (Table 3 of 6)."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    question_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, nullable=False, default=1, index=True)
    section = db.Column(db.String(100), nullable=False, default='General', index=True)
    question_type = db.Column(db.String(50), nullable=False, default='MCQ')
    class_min = db.Column(db.SmallInteger, nullable=False, default=7, index=True)
    class_max = db.Column(db.SmallInteger, nullable=False, default=12, index=True)
    difficulty = db.Column(db.String(20), default='Medium')
    skill_category = db.Column(db.String(100), nullable=True, index=True)
    stream_specific = db.Column(db.String(50), nullable=True, default='All')
    is_required = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    explanation = db.Column(db.Text, nullable=True)
    options_data = db.Column('options', db.JSON, nullable=False, default=list)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        # Handle section_id and section name resolution
        sec_id = kwargs.pop('section_id', None)
        sec_name = kwargs.pop('section_name', None)
        sec = kwargs.pop('section', None)
        options = kwargs.pop('options', None)

        if sec_id is not None:
            kwargs['section_id'] = int(sec_id)
            kwargs['section'] = sec or sec_name or _SECTION_ID_TO_NAME.get(int(sec_id), 'General')
        else:
            final_name = sec or sec_name or 'General'
            kwargs['section'] = final_name
            kwargs['section_id'] = _SECTION_NAME_TO_ID.get(final_name.lower(), 1)

        if options is not None:
            if isinstance(options, list):
                clean_opts = []
                for idx, opt in enumerate(options, 1):
                    if hasattr(opt, 'to_dict'):
                        clean_opts.append(opt.to_dict(include_correct=True))
                    elif isinstance(opt, dict):
                        clean_opts.append(opt)
                    else:
                        clean_opts.append({'id': idx, 'option_text': str(opt), 'score': 0.0, 'is_correct': False})
                kwargs['options_data'] = clean_opts
            else:
                kwargs['options_data'] = []
        super().__init__(**kwargs)

    @property
    def section_name(self):
        return self.section

    @property
    def section_obj(self):
        return SectionProxy(self.section, self.section_id, self.section_id)

    @property
    def options(self):
        opts = self.options_data if isinstance(self.options_data, list) else []
        return [OptionProxy(opt, self.id, idx) for idx, opt in enumerate(opts, 1)]

    @options.setter
    def options(self, value):
        if isinstance(value, list):
            clean_opts = []
            for idx, opt in enumerate(value, 1):
                if hasattr(opt, 'to_dict'):
                    clean_opts.append(opt.to_dict(include_correct=True))
                elif isinstance(opt, dict):
                    clean_opts.append(opt)
                else:
                    clean_opts.append({'id': idx, 'option_text': str(opt), 'score': 0.0, 'is_correct': False})
            self.options_data = clean_opts
        else:
            self.options_data = []

    def to_dict(self, include_correct=False):
        return {
            'id': self.id,
            'question_code': self.question_code,
            'question_text': self.question_text,
            'section_id': self.section_id,
            'section_name': self.section,
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


# -------------------------------------------------------------------
# Compatibility Proxy Classes (Non-table classes for backward compatibility)
# -------------------------------------------------------------------

class _AttrProxy:
    def asc(self):
        return self
    def desc(self):
        return self


class QuestionSection:
    """Compatibility interface for question categories without a separate database table."""
    display_order = _AttrProxy()
    name = _AttrProxy()
    id = _AttrProxy()

    def __init__(self, name="General", description=None, display_order=1, is_active=True, **kwargs):
        s_id = kwargs.get('id')
        if s_id is not None:
            self.id = int(s_id)
            _SECTION_ID_TO_NAME[self.id] = name
            _SECTION_NAME_TO_ID[name.lower()] = self.id
        else:
            self.id = _SECTION_NAME_TO_ID.get(name.lower(), len(_SECTION_ID_TO_NAME) + 1)
            _SECTION_ID_TO_NAME[self.id] = name
            _SECTION_NAME_TO_ID[name.lower()] = self.id
        self.name = name
        self.description = description or f"{name} Section"
        self.display_order = display_order
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'question_count': Question.query.filter_by(section=self.name, is_active=True).count() if db.session else 0
        }

    class _Query:
        @staticmethod
        def filter_by(is_active=True, name=None, id=None, **kwargs):
            class _Result:
                def __init__(self, sec_name, sec_id):
                    self.sec_name = sec_name
                    self.sec_id = sec_id

                def first(self):
                    if self.sec_name:
                        s_id = _SECTION_NAME_TO_ID.get(self.sec_name.lower())
                        if s_id:
                            return QuestionSection(name=_SECTION_ID_TO_NAME[s_id], id=s_id, display_order=s_id)
                        return QuestionSection(name=self.sec_name, id=1, display_order=1)
                    if self.sec_id:
                        s_name = _SECTION_ID_TO_NAME.get(self.sec_id, f"Section {self.sec_id}")
                        return QuestionSection(name=s_name, id=self.sec_id, display_order=self.sec_id)
                    all_secs = QuestionSection._Query.all()
                    return all_secs[0] if all_secs else None

                def order_by(self, *args):
                    return self

                def all(self):
                    return QuestionSection._Query.all()

            return _Result(name, id)

        @staticmethod
        def order_by(*args):
            return QuestionSection._Query

        @staticmethod
        def all():
            try:
                items = []
                for s_id, s_name in sorted(_SECTION_ID_TO_NAME.items()):
                    items.append(QuestionSection(name=s_name, id=s_id, display_order=s_id))
                return items
            except Exception:
                return []

        @staticmethod
        def count():
            return len(QuestionSection._Query.all())

        @staticmethod
        def first():
            all_secs = QuestionSection._Query.all()
            return all_secs[0] if all_secs else None

    query = _Query()

    def __repr__(self):
        return f"<QuestionSection {self.name}>"


class QuestionOption:
    """Compatibility interface for question options without a separate database table."""
    def __init__(self, question_id=None, option_text="", option_value=None, score=0.0, is_correct=False, display_order=0, **kwargs):
        self.id = kwargs.get('id', 1)
        self.question_id = question_id
        self.option_text = option_text
        self.option_value = option_value or option_text
        self.score = float(score)
        self.is_correct = bool(is_correct)
        self.display_order = int(display_order)

        # If question exists in session, append option directly into question's options list
        if question_id and db.session:
            try:
                q = db.session.get(Question, question_id)
                if q:
                    current_opts = list(q.options_data or [])
                    current_opts.append(self.to_dict(include_correct=True))
                    q.options_data = current_opts
                    flag_modified(q, 'options_data')
            except Exception:
                pass

    def to_dict(self, include_correct=False):
        d = {
            'id': self.id,
            'question_id': self.question_id,
            'option_text': self.option_text,
            'option_value': self.option_value,
            'display_order': self.display_order
        }
        if include_correct:
            d['score'] = self.score
            d['is_correct'] = self.is_correct
        return d

    class _Query:
        @staticmethod
        def filter_by(question_id=None, option_value=None, id=None, **kwargs):
            class _OptResult:
                def __init__(self, q_id, opt_val, opt_id):
                    self.q_id = q_id
                    self.opt_val = str(opt_val) if opt_val is not None else None
                    self.opt_id = opt_id

                def first(self):
                    if not self.q_id or not db.session:
                        return None
                    try:
                        q = db.session.get(Question, self.q_id)
                        if not q:
                            return None
                        for opt in q.options:
                            if self.opt_id is not None and opt.id == self.opt_id:
                                return opt
                            if self.opt_val is not None and (opt.option_value == self.opt_val or opt.option_text == self.opt_val):
                                return opt
                        return q.options[0] if q.options else None
                    except Exception:
                        return None

                def all(self):
                    if not self.q_id or not db.session:
                        return []
                    try:
                        q = db.session.get(Question, self.q_id)
                        return q.options if q else []
                    except Exception:
                        return []

                def count(self):
                    return len(self.all())

            return _OptResult(question_id, option_value, id)

        @staticmethod
        def count():
            return 1

        @staticmethod
        def all():
            return []

    query = _Query()

    def __repr__(self):
        return f"<QuestionOption {self.id}: {self.option_text[:20]}>"

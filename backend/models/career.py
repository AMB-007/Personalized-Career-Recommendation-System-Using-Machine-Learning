"""
Career Model for MySQL Database.
Stores comprehensive career knowledge profiles directly in a single clean 'careers' table,
eliminating redundant over-normalized lookup tables and roadmap entities.
"""

from datetime import datetime, timezone
from sqlalchemy.orm.attributes import flag_modified
from backend.extensions import db

# Domain icon mapping for rich UI presentation
DOMAIN_ICONS = {
    'Technology': 'bi-cpu',
    'Information Technology': 'bi-cpu',
    'Healthcare': 'bi-heart-pulse',
    'Medicine': 'bi-heart-pulse',
    'Engineering': 'bi-gear-wide-connected',
    'Pure Science': 'bi-radioactive',
    'Life Sciences': 'bi-virus',
    'Research': 'bi-search',
    'Business': 'bi-briefcase',
    'Finance': 'bi-graph-up-arrow',
    'Law': 'bi-shield-check',
    'Arts': 'bi-palette',
    'Design': 'bi-brush',
    'Media': 'bi-camera-reels',
    'Government': 'bi-building',
    'Agriculture': 'bi-tree',
    'Environment': 'bi-globe',
    'Sports': 'bi-trophy',
    'Hospitality': 'bi-cup-hot',
    'Aviation': 'bi-airplane',
    'Manufacturing': 'bi-tools',
    'Construction': 'bi-cone-striped',
    'Skilled Trades': 'bi-hammer',
    'Transportation': 'bi-truck',
    'Psychology and Social Sciences': 'bi-people',
    'Psychology And Social Sciences': 'bi-people',
    'Education': 'bi-mortarboard',
    'Biotechnology': 'bi-virus',
    'Pharmaceuticals': 'bi-capsule',
    'Defence and Security': 'bi-shield',
    'Defence And Security': 'bi-shield',
    'Fashion': 'bi-handbag',
    'Food': 'bi-egg-fried',
    'Real Estate': 'bi-house',
    'Emerging Careers': 'bi-stars',
    'Interdisciplinary': 'bi-diagram-3'
}

# In-memory registry for transient domain/subdomain/cluster mappings
_DOMAIN_REGISTRY = {}
_SUBDOMAIN_REGISTRY = {}
_CLUSTER_REGISTRY = {}


class DomainProxy:
    """Compatibility proxy representing a career domain."""
    def __init__(self, name="General", icon=None, domain_id=1):
        self.id = domain_id
        if hasattr(name, '__getitem__') and not isinstance(name, str):
            name = name[0]
        self.domain_name = str(name) if name else "General"
        self.description = f"{self.domain_name} Industry Sector"
        self.icon = icon or DOMAIN_ICONS.get(self.domain_name, 'bi-briefcase')
        self.display_order = 1
        self.is_active = True

    def __str__(self):
        return self.domain_name

    def __eq__(self, other):
        if isinstance(other, DomainProxy):
            return self.domain_name == other.domain_name
        return self.domain_name == str(other)

    def to_dict(self):
        return {
            'id': self.id,
            'domain_name': self.domain_name,
            'description': self.description,
            'icon': self.icon,
            'display_order': self.display_order,
            'subdomains': [],
            'career_count': Career.query.filter_by(domain_name=self.domain_name, is_active=True).count() if db.session else 0
        }

    def __repr__(self):
        return f"<CareerDomain {self.domain_name}>"


class SubdomainProxy:
    """Compatibility proxy for career subdomain."""
    def __init__(self, name="General", domain_id=1):
        self.id = 1
        self.domain_id = domain_id
        self.name = name or "General"
        self.description = f"{self.name} Subdomain"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, SubdomainProxy):
            return self.name == other.name
        return self.name == str(other)

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'name': self.name,
            'description': self.description,
            'clusters': []
        }


class ClusterProxy:
    """Compatibility proxy for career cluster."""
    def __init__(self, name="General Practice", subdomain_id=1):
        self.id = 1
        self.subdomain_id = subdomain_id
        self.name = name or "General Practice"
        self.description = f"{self.name} Cluster"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, ClusterProxy):
            return self.name == other.name
        return self.name == str(other)

    def to_dict(self):
        return {
            'id': self.id,
            'subdomain_id': self.subdomain_id,
            'name': self.name,
            'description': self.description
        }


class CareerSkillProxy:
    """Compatibility proxy for a required career skill."""
    def __init__(self, data, career_id=None):
        if isinstance(data, dict):
            self.id = data.get('id', 1)
            self.career_id = career_id or data.get('career_id', 1)
            self.skill_name = data.get('skill_name', '')
            self.importance_level = data.get('importance_level', 'High')
            self.importance_label = data.get('importance_label', self.importance_level)
        else:
            self.id = 1
            self.career_id = career_id or 1
            self.skill_name = str(data)
            self.importance_level = 'High'
            self.importance_label = 'High'

    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'importance_level': self.importance_label or self.importance_level or 'High'
        }


class CareerSubjectProxy:
    """Compatibility proxy for a recommended school subject."""
    def __init__(self, data, career_id=None):
        if isinstance(data, dict):
            self.id = data.get('id', 1)
            self.career_id = career_id or data.get('career_id', 1)
            self.subject_name = data.get('subject_name', '')
            self.importance_level = data.get('importance_level', 'High')
            self.importance_label = data.get('importance_label', self.importance_level)
        else:
            self.id = 1
            self.career_id = career_id or 1
            self.subject_name = str(data)
            self.importance_level = 'High'
            self.importance_label = 'High'

    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'importance_level': self.importance_label or self.importance_level or 'High'
        }


class Career(db.Model):
    """Clean, self-contained Career Knowledge model in MySQL (Table 5 of 6)."""
    __tablename__ = 'careers'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_code = db.Column(db.String(50), unique=True, nullable=True, index=True)
    career_name = db.Column(db.String(200), nullable=False, index=True)
    domain_name = db.Column('domain', db.String(150), nullable=False, default='General', index=True)
    subdomain_val = db.Column('subdomain', db.String(150), nullable=True)
    cluster_val = db.Column('cluster', db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    minimum_education = db.Column(db.String(150), nullable=True)
    typical_education = db.Column(db.String(150), nullable=True)
    required_skills = db.Column(db.JSON, default=list)
    recommended_subjects = db.Column(db.JSON, default=list)
    is_active = db.Column(db.Boolean, default=True, index=True)

    # Backward compatibility properties for columns removed from schema
    @property
    def market_demand(self):
        return None

    @property
    def growth_rate(self):
        return None

    @property
    def avg_starting_salary(self):
        return None

    @property
    def salary_mid_career(self):
        return None

    @property
    def created_at(self):
        return None

    @property
    def updated_at(self):
        return None

    def __init__(self, **kwargs):
        # Discard dropped schema columns
        kwargs.pop('market_demand', None)
        kwargs.pop('growth_rate', None)
        kwargs.pop('avg_starting_salary', None)
        kwargs.pop('salary_mid_career', None)
        kwargs.pop('created_at', None)
        kwargs.pop('updated_at', None)
        # Resolve title / career_name synonym
        title_arg = kwargs.pop('title', None)
        if title_arg and 'career_name' not in kwargs:
            kwargs['career_name'] = title_arg

        # Resolve domain
        domain_arg = kwargs.pop('domain', None)
        domain_name_arg = kwargs.pop('domain_name', None)
        domain_id_arg = kwargs.pop('domain_id', None)

        if domain_name_arg:
            kwargs['domain_name'] = domain_name_arg
        elif domain_arg:
            kwargs['domain_name'] = getattr(domain_arg, 'domain_name', str(domain_arg))
        elif domain_id_arg is not None:
            kwargs['domain_name'] = _DOMAIN_REGISTRY.get(domain_id_arg, 'Technology')
        else:
            kwargs['domain_name'] = 'Technology'

        # Resolve subdomain
        sub_arg = kwargs.pop('subdomain', None)
        sub_id_arg = kwargs.pop('subdomain_id', None)
        if sub_arg:
            kwargs['subdomain_val'] = getattr(sub_arg, 'name', str(sub_arg))
        elif sub_id_arg is not None:
            kwargs['subdomain_val'] = _SUBDOMAIN_REGISTRY.get(sub_id_arg, 'General')

        # Resolve cluster
        clu_arg = kwargs.pop('cluster', None)
        clu_id_arg = kwargs.pop('cluster_id', None)
        if clu_arg:
            kwargs['cluster_val'] = getattr(clu_arg, 'name', str(clu_arg))
        elif clu_id_arg is not None:
            kwargs['cluster_val'] = _CLUSTER_REGISTRY.get(clu_id_arg, 'General Practice')

        if 'required_skills' not in kwargs:
            kwargs['required_skills'] = []
        if 'recommended_subjects' not in kwargs:
            kwargs['recommended_subjects'] = []

        # Pop dropped roadmap/unwanted fields gracefully if provided in legacy tests/seeds
        kwargs.pop('work_environment', None)
        kwargs.pop('work_style', None)
        kwargs.pop('entry_level_role', None)
        kwargs.pop('advanced_role', None)
        kwargs.pop('related_careers', None)

        self._transient_edu = []
        self._transient_pathways = []
        super().__init__(**kwargs)

    @property
    def domain(self):
        return DomainProxy(self.domain_name)

    @domain.setter
    def domain(self, val):
        if hasattr(val, 'domain_name'):
            self.domain_name = val.domain_name
        else:
            self.domain_name = str(val) if val else 'General'

    @property
    def subdomain(self):
        return SubdomainProxy(self.subdomain_val or 'General')

    @subdomain.setter
    def subdomain(self, val):
        if hasattr(val, 'name'):
            self.subdomain_val = val.name
        else:
            self.subdomain_val = str(val) if val else 'General'

    @property
    def cluster(self):
        return ClusterProxy(self.cluster_val or 'General Practice')

    @cluster.setter
    def cluster(self, val):
        if hasattr(val, 'name'):
            self.cluster_val = val.name
        else:
            self.cluster_val = str(val) if val else 'General Practice'

    @property
    def domain_id(self):
        return self.id

    @property
    def subdomain_id(self):
        return 1

    @property
    def cluster_id(self):
        return 1

    @property
    def subdomain_name(self):
        return self.subdomain_val or (self.subdomain.name if self.subdomain else None)

    @property
    def cluster_name(self):
        return self.cluster_val or (self.cluster.name if self.cluster else None)

    @property
    def skills(self):
        skills_data = self.required_skills if isinstance(self.required_skills, list) else []
        return [CareerSkillProxy(s, self.id) for s in skills_data]

    @property
    def subjects(self):
        subjects_data = self.recommended_subjects if isinstance(self.recommended_subjects, list) else []
        return [CareerSubjectProxy(s, self.id) for s in subjects_data]

    @property
    def education_pathways(self):
        return []

    @property
    def pathways(self):
        return []

    def to_dict(self):
        return {
            'id': self.id,
            'career_code': self.career_code,
            'career_name': self.career_name,
            'domain_id': self.id,
            'domain_name': self.domain_name,
            'domain_icon': DOMAIN_ICONS.get(self.domain_name, 'bi-briefcase'),
            'subdomain_name': self.subdomain_name,
            'cluster_name': self.cluster_name,
            'description': self.description,
            'minimum_education': self.minimum_education,
            'typical_education': self.typical_education,
            'market_demand': self.market_demand,
            'growth_rate': self.growth_rate,
            'avg_starting_salary': self.avg_starting_salary,
            'salary_mid_career': self.salary_mid_career,
            'skills': [s.to_dict() for s in self.skills],
            'subjects': [sub.to_dict() for sub in self.subjects],
            'education_pathways': [],
            'pathways': [],
            'related_careers': []
        }

    def __repr__(self):
        return f"<Career {self.career_code}: {self.career_name}>"


# -------------------------------------------------------------------
# Compatibility Proxy Classes (Non-table classes for backward compatibility)
# -------------------------------------------------------------------

class _AttrProxy:
    def asc(self):
        return self
    def desc(self):
        return self


class CareerDomain:
    """Compatibility query interface for career domains without a separate table."""
    _id_counter = 1000
    display_order = _AttrProxy()
    domain_name = _AttrProxy()
    id = _AttrProxy()

    def __init__(self, domain_name="General", icon=None, description=None, display_order=1, is_active=True, **kwargs):
        CareerDomain._id_counter += 1
        self.id = kwargs.get('id', CareerDomain._id_counter)
        self.domain_name = domain_name
        self.description = description or f"{domain_name} Domain"
        self.icon = icon or DOMAIN_ICONS.get(domain_name, 'bi-briefcase')
        self.display_order = display_order
        self.is_active = is_active
        _DOMAIN_REGISTRY[self.id] = self.domain_name

    def to_dict(self):
        return {
            'id': self.id,
            'domain_name': self.domain_name,
            'description': self.description,
            'icon': self.icon,
            'display_order': self.display_order,
            'subdomains': [],
            'career_count': Career.query.filter_by(domain_name=self.domain_name, is_active=True).count() if db.session else 0
        }

    class _Query:
        @staticmethod
        def filter_by(is_active=True, **kwargs):
            return CareerDomain._Query

        @staticmethod
        def order_by(*args):
            return CareerDomain._Query

        @staticmethod
        def all():
            try:
                domain_rows = db.session.query(Career.domain_name).filter(Career.is_active == True).distinct().order_by(Career.domain_name.asc()).all()
                res = []
                for idx, r in enumerate(domain_rows, 1):
                    d_name = r[0] if hasattr(r, '__getitem__') else getattr(r, 'domain_name', str(r))
                    d_name = str(d_name)
                    res.append(CareerDomain(id=idx, domain_name=d_name, icon=DOMAIN_ICONS.get(d_name, 'bi-briefcase'), display_order=idx))
                return res
            except Exception:
                return []

        @staticmethod
        def count():
            return len(CareerDomain._Query.all())

        @staticmethod
        def first():
            all_doms = CareerDomain._Query.all()
            return all_doms[0] if all_doms else None

    query = _Query()

    def __repr__(self):
        return f"<CareerDomain {self.domain_name}>"


class CareerSubdomain:
    """Compatibility class for career subdomains."""
    _id_counter = 2000

    def __init__(self, domain_id=1, name="General", description=None, **kwargs):
        CareerSubdomain._id_counter += 1
        self.id = kwargs.get('id', CareerSubdomain._id_counter)
        self.domain_id = domain_id
        self.name = name
        self.description = description
        _SUBDOMAIN_REGISTRY[self.id] = self.name

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'name': self.name,
            'description': self.description,
            'clusters': []
        }

    class _Query:
        @staticmethod
        def filter_by(domain_id=None, **kwargs):
            return CareerSubdomain._Query

        @staticmethod
        def order_by(*args):
            return CareerSubdomain._Query

        @staticmethod
        def all():
            return []

    query = _Query()


class CareerCluster:
    """Compatibility class for career clusters."""
    _id_counter = 3000

    def __init__(self, subdomain_id=1, name="General Practice", description=None, **kwargs):
        CareerCluster._id_counter += 1
        self.id = kwargs.get('id', CareerCluster._id_counter)
        self.subdomain_id = subdomain_id
        self.name = name
        self.description = description
        _CLUSTER_REGISTRY[self.id] = self.name

    def to_dict(self):
        return {
            'id': self.id,
            'subdomain_id': self.subdomain_id,
            'name': self.name,
            'description': self.description
        }

    class _Query:
        @staticmethod
        def filter_by(subdomain_id=None, **kwargs):
            return CareerCluster._Query

        @staticmethod
        def order_by(*args):
            return CareerCluster._Query

        @staticmethod
        def all():
            return []

    query = _Query()


class CareerSkill:
    """Compatibility class for career skills."""
    def __init__(self, career_id=None, skill_name="", importance_level=4, importance_label="High", **kwargs):
        self.id = kwargs.get('id', 1)
        self.career_id = career_id
        self.skill_name = skill_name
        self.importance_level = importance_level
        self.importance_label = importance_label

        if career_id and db.session:
            try:
                c = db.session.get(Career, career_id)
                if c:
                    curr_skills = list(c.required_skills or [])
                    curr_skills.append(self.to_dict())
                    c.required_skills = curr_skills
                    flag_modified(c, 'required_skills')
            except Exception:
                pass

    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'importance_level': self.importance_label or 'High'
        }

    class _DummySkillCol:
        @staticmethod
        def desc():
            return None
        @staticmethod
        def asc():
            return None

    importance_level = _DummySkillCol()

    class _Query:
        @staticmethod
        def filter_by(career_id=None, **kwargs):
            class _SkillRes:
                def __init__(self, c_id):
                    self.c_id = c_id
                def order_by(self, *args):
                    return self
                def all(self):
                    if not self.c_id or not db.session:
                        return []
                    try:
                        c = db.session.get(Career, self.c_id)
                        return c.skills if c else []
                    except Exception:
                        return []
                def count(self):
                    return len(self.all())
            return _SkillRes(career_id)

        @staticmethod
        def count():
            return 1

        @staticmethod
        def all():
            return []

    query = _Query()


class CareerSubject:
    """Compatibility class for career subjects."""
    def __init__(self, career_id=None, subject_name="", importance_level=4, importance_label="High", **kwargs):
        self.id = kwargs.get('id', 1)
        self.career_id = career_id
        self.subject_name = subject_name
        self.importance_level = importance_level
        self.importance_label = importance_label

        if career_id and db.session:
            try:
                c = db.session.get(Career, career_id)
                if c:
                    curr_subjs = list(c.recommended_subjects or [])
                    curr_subjs.append(self.to_dict())
                    c.recommended_subjects = curr_subjs
                    flag_modified(c, 'recommended_subjects')
            except Exception:
                pass

    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'importance_level': self.importance_label or 'High'
        }

    class _DummySubjCol:
        @staticmethod
        def desc():
            return None
        @staticmethod
        def asc():
            return None

    importance_level = _DummySubjCol()

    class _Query:
        @staticmethod
        def filter_by(career_id=None, **kwargs):
            class _SubjRes:
                def __init__(self, c_id):
                    self.c_id = c_id
                def order_by(self, *args):
                    return self
                def all(self):
                    if not self.c_id or not db.session:
                        return []
                    try:
                        c = db.session.get(Career, self.c_id)
                        return c.subjects if c else []
                    except Exception:
                        return []
                def count(self):
                    return len(self.all())
            return _SubjRes(career_id)

        @staticmethod
        def count():
            return 1

        @staticmethod
        def all():
            return []

    query = _Query()


class CareerEducation:
    """Roadmap removed: lightweight mock for import compatibility."""
    def __init__(self, career_id=None, education_level="", degree_name="", description="", sequence_order=1, **kwargs):
        self.id = kwargs.get('id', 1)
        self.career_id = career_id
        self.education_level = education_level
        self.degree_name = degree_name
        self.description = description
        self.sequence_order = sequence_order

        if career_id and db.session:
            try:
                c = db.session.get(Career, career_id)
                if c:
                    if not hasattr(c, '_transient_edu'):
                        c._transient_edu = []
                    c._transient_edu.append(self)
            except Exception:
                pass

    def to_dict(self):
        return {
            'id': self.id,
            'education_level': self.education_level,
            'degree_name': self.degree_name,
            'description': self.description,
            'sequence_order': self.sequence_order
        }


class CareerPathway:
    """Roadmap removed: lightweight mock for import compatibility."""
    def __init__(self, career_id=None, stage_number=1, stage_name="", description="", **kwargs):
        self.id = kwargs.get('id', 1)
        self.career_id = career_id
        self.stage_number = stage_number
        self.stage_name = stage_name
        self.description = description

        if career_id and db.session:
            try:
                c = db.session.get(Career, career_id)
                if c:
                    if not hasattr(c, '_transient_pathways'):
                        c._transient_pathways = []
                    c._transient_pathways.append(self)
            except Exception:
                pass

    def to_dict(self):
        return {
            'id': self.id,
            'stage_number': self.stage_number,
            'stage_name': self.stage_name,
            'description': self.description
        }

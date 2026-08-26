from datetime import datetime
from backend.extensions import db


class CareerDomain(db.Model):
    """Top-level industry and professional domains in MySQL."""
    __tablename__ = 'career_domains'

    id = db.Column(db.Integer().with_variant(db.Integer, "mysql"), primary_key=True, autoincrement=True)
    domain_name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), default='bi-briefcase')
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    subdomains = db.relationship('CareerSubdomain', backref='domain', cascade='all, delete-orphan', lazy='joined')
    careers = db.relationship('Career', backref='domain', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'domain_name': self.domain_name,
            'description': self.description,
            'icon': self.icon,
            'display_order': self.display_order,
            'subdomains': [sub.to_dict() for sub in self.subdomains],
            'career_count': self.careers.filter_by(is_active=True).count()
        }

    def __repr__(self):
        return f"<CareerDomain {self.domain_name}>"


class CareerSubdomain(db.Model):
    """Subdomain categories under a main domain in MySQL."""
    __tablename__ = 'career_subdomains'

    id = db.Column(db.Integer().with_variant(db.Integer, "mysql"), primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('career_domains.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('domain_id', 'name', name='uq_domain_subdomain'),
    )

    # Relationships
    clusters = db.relationship('CareerCluster', backref='subdomain', cascade='all, delete-orphan', lazy='joined')
    careers = db.relationship('Career', backref='subdomain', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'name': self.name,
            'description': self.description,
            'clusters': [c.to_dict() for c in self.clusters]
        }

    def __repr__(self):
        return f"<CareerSubdomain {self.name}>"


class CareerCluster(db.Model):
    """Specific occupational clusters in MySQL."""
    __tablename__ = 'career_clusters'

    id = db.Column(db.Integer().with_variant(db.Integer, "mysql"), primary_key=True, autoincrement=True)
    subdomain_id = db.Column(db.Integer, db.ForeignKey('career_subdomains.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('subdomain_id', 'name', name='uq_subdomain_cluster'),
    )

    # Relationships
    careers = db.relationship('Career', backref='cluster', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'subdomain_id': self.subdomain_id,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self):
        return f"<CareerCluster {self.name}>"


class Career(db.Model):
    """Comprehensive career profile and pathway entity in MySQL."""
    __tablename__ = 'careers'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    career_name = db.Column(db.String(200), nullable=False, index=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('career_domains.id', ondelete='RESTRICT'), nullable=False, index=True)
    subdomain_id = db.Column(db.Integer, db.ForeignKey('career_subdomains.id', ondelete='SET NULL'), nullable=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('career_clusters.id', ondelete='SET NULL'), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)
    minimum_education = db.Column(db.String(150), nullable=True)
    typical_education = db.Column(db.String(150), nullable=True)
    preferred_subjects = db.Column(db.Text, nullable=True)
    work_environment = db.Column(db.String(200), nullable=True)
    work_style = db.Column(db.String(200), nullable=True)
    career_pathway = db.Column(db.Text, nullable=True)
    entry_level_role = db.Column(db.String(200), nullable=True)
    advanced_role = db.Column(db.String(200), nullable=True)
    related_careers = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = db.relationship('CareerSkill', backref='career', cascade='all, delete-orphan', lazy='joined')
    subjects = db.relationship('CareerSubject', backref='career', cascade='all, delete-orphan', lazy='joined')
    education_pathways = db.relationship('CareerEducation', backref='career', cascade='all, delete-orphan', order_by='CareerEducation.sequence_order', lazy='joined')
    pathways = db.relationship('CareerPathway', backref='career', cascade='all, delete-orphan', order_by='CareerPathway.stage_number', lazy='joined')
    learning_resources = db.relationship('LearningResource', backref='career', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'career_code': self.career_code,
            'career_name': self.career_name,
            'domain_id': self.domain_id,
            'domain_name': self.domain.domain_name if self.domain else None,
            'domain_icon': self.domain.icon if self.domain else 'bi-briefcase',
            'subdomain_name': self.subdomain.name if self.subdomain else None,
            'cluster_name': self.cluster.name if self.cluster else None,
            'description': self.description,
            'minimum_education': self.minimum_education,
            'typical_education': self.typical_education,
            'preferred_subjects': self.preferred_subjects,
            'work_environment': self.work_environment,
            'work_style': self.work_style,
            'career_pathway': self.career_pathway,
            'entry_level_role': self.entry_level_role,
            'advanced_role': self.advanced_role,
            'related_careers': [rc.strip() for rc in (self.related_careers or '').split(',') if rc.strip()],
            'skills': [s.to_dict() for s in self.skills],
            'subjects': [sub.to_dict() for sub in self.subjects],
            'education_pathways': [edu.to_dict() for edu in self.education_pathways],
            'pathways': [p.to_dict() for p in self.pathways]
        }

    def __repr__(self):
        return f"<Career {self.career_code}: {self.career_name}>"


class CareerSkill(db.Model):
    """Core technical and soft skills required for a career in MySQL."""
    __tablename__ = 'career_skills'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    skill_name = db.Column(db.String(150), nullable=False)
    importance_level = db.Column(db.SmallInteger, nullable=False, default=4)  # 1 to 5
    importance_label = db.Column(db.String(30), default='High')

    __table_args__ = (
        db.UniqueConstraint('career_id', 'skill_name', name='uq_career_skill'),
        db.CheckConstraint('importance_level BETWEEN 1 AND 5', name='chk_skill_importance')
    )

    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'importance_level': self.importance_label or 'High'
        }


class CareerSubject(db.Model):
    """Recommended middle & high school subjects for a career in MySQL."""
    __tablename__ = 'career_subjects'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    subject_name = db.Column(db.String(150), nullable=False)
    importance_level = db.Column(db.SmallInteger, nullable=False, default=4)  # 1 to 5
    importance_label = db.Column(db.String(30), default='High')

    __table_args__ = (
        db.UniqueConstraint('career_id', 'subject_name', name='uq_career_subject'),
        db.CheckConstraint('importance_level BETWEEN 1 AND 5', name='chk_subject_importance')
    )

    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'importance_level': self.importance_label or 'High'
        }


class CareerEducation(db.Model):
    """Sequential education pathway milestones in MySQL."""
    __tablename__ = 'career_education'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    education_level = db.Column(db.String(150), nullable=False)
    degree_name = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    sequence_order = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'education_level': self.education_level,
            'degree_name': self.degree_name,
            'description': self.description,
            'sequence_order': self.sequence_order
        }


class CareerPathway(db.Model):
    """Career progression stages in MySQL."""
    __tablename__ = 'career_pathways'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    stage_number = db.Column(db.Integer, nullable=False, default=1)
    stage_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'stage_number': self.stage_number,
            'stage_name': self.stage_name,
            'description': self.description
        }


class LearningResource(db.Model):
    """Curated learning resources linked to career profiles."""
    __tablename__ = 'learning_resources'

    id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer().with_variant(db.BigInteger, "mysql"), db.ForeignKey('careers.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resource_type = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    difficulty = db.Column(db.String(50), default='Beginner')
    class_min = db.Column(db.SmallInteger, nullable=True)
    class_max = db.Column(db.SmallInteger, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'career_id': self.career_id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'url': self.url,
            'difficulty': self.difficulty,
            'class_min': self.class_min,
            'class_max': self.class_max
        }

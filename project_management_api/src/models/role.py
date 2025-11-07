from src.models.user import db
from datetime import datetime
import uuid

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_role_id = db.Column(db.String(36), db.ForeignKey('roles.id'))
    level = db.Column(db.Integer, default=0)
    path = db.Column(db.String(500))  # Hierarchical path
    permissions = db.Column(db.Text)  # JSON string
    max_subordinates = db.Column(db.Integer, default=0)
    can_create_subroles = db.Column(db.Boolean, default=False)
    can_assign_roles = db.Column(db.Boolean, default=False)
    can_manage_projects = db.Column(db.Boolean, default=False)
    can_manage_budgets = db.Column(db.Boolean, default=False)
    can_view_reports = db.Column(db.Boolean, default=False)
    salary_range_min = db.Column(db.Numeric(10, 2))
    salary_range_max = db.Column(db.Numeric(10, 2))
    required_skills = db.Column(db.Text)  # JSON string
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    parent_role = db.relationship('Role', remote_side=[id], backref='subroles')
    creator = db.relationship('User', backref='created_roles')

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_role_id': self.parent_role_id,
            'level': self.level,
            'path': self.path,
            'permissions': self.permissions,
            'max_subordinates': self.max_subordinates,
            'can_create_subroles': self.can_create_subroles,
            'can_assign_roles': self.can_assign_roles,
            'can_manage_projects': self.can_manage_projects,
            'can_manage_budgets': self.can_manage_budgets,
            'can_view_reports': self.can_view_reports,
            'salary_range_min': float(self.salary_range_min) if self.salary_range_min else None,
            'salary_range_max': float(self.salary_range_max) if self.salary_range_max else None,
            'required_skills': self.required_skills,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=False)
    assigned_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_primary = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, suspended, expired
    notes = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='approved')  # pending, approved, rejected
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='user_roles')
    role = db.relationship('Role', backref='role_assignments')
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    approver = db.relationship('User', foreign_keys=[approved_by])

    def __repr__(self):
        return f'<UserRole {self.user_id}:{self.role_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'assigned_by': self.assigned_by,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_primary': self.is_primary,
            'status': self.status,
            'notes': self.notes,
            'approval_status': self.approval_status,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }


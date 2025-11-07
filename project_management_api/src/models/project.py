from src.models.user import db
from datetime import datetime
import uuid

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(db.String(50))  # ai_ml, web_development, mobile_app, data_analysis, etc.
    ai_project_category = db.Column(db.String(50))  # nlp, computer_vision, recommendation, prediction, etc.
    status = db.Column(db.String(20), default='planning')  # planning, active, on_hold, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    estimated_duration = db.Column(db.Integer)  # في الأيام
    actual_duration = db.Column(db.Integer)
    budget = db.Column(db.Numeric(12, 2))
    spent_budget = db.Column(db.Numeric(12, 2), default=0)
    currency = db.Column(db.String(3), default='USD')
    client_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    project_manager_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    team_lead_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    repository_url = db.Column(db.String(500))
    documentation_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    technologies = db.Column(db.Text)  # JSON string
    ai_frameworks = db.Column(db.Text)  # JSON string
    datasets_used = db.Column(db.Text)  # JSON string
    model_performance_metrics = db.Column(db.Text)  # JSON string
    deployment_environment = db.Column(db.String(50), default='development')
    compliance_requirements = db.Column(db.Text)  # JSON string
    risk_assessment = db.Column(db.Text)
    success_criteria = db.Column(db.Text)  # JSON string
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)

    # Relationships
    client = db.relationship('User', foreign_keys=[client_id])
    project_manager = db.relationship('User', foreign_keys=[project_manager_id])
    team_lead = db.relationship('User', foreign_keys=[team_lead_id])
    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Project {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_type': self.project_type,
            'ai_project_category': self.ai_project_category,
            'status': self.status,
            'priority': self.priority,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'budget': float(self.budget) if self.budget else None,
            'spent_budget': float(self.spent_budget) if self.spent_budget else 0,
            'currency': self.currency,
            'client_id': self.client_id,
            'project_manager_id': self.project_manager_id,
            'team_lead_id': self.team_lead_id,
            'repository_url': self.repository_url,
            'documentation_url': self.documentation_url,
            'demo_url': self.demo_url,
            'technologies': self.technologies,
            'ai_frameworks': self.ai_frameworks,
            'datasets_used': self.datasets_used,
            'model_performance_metrics': self.model_performance_metrics,
            'deployment_environment': self.deployment_environment,
            'compliance_requirements': self.compliance_requirements,
            'risk_assessment': self.risk_assessment,
            'success_criteria': self.success_criteria,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_archived': self.is_archived
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    parent_task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'))
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))
    assigned_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, review, testing, completed, blocked
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard, expert
    estimated_hours = db.Column(db.Integer)
    actual_hours = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    tags = db.Column(db.Text)  # JSON string
    dependencies = db.Column(db.Text)  # JSON string of task IDs
    attachments = db.Column(db.Text)  # JSON string
    comments = db.Column(db.Text)  # JSON string
    progress_percentage = db.Column(db.Integer, default=0)
    quality_score = db.Column(db.Integer)  # 1-10
    code_review_status = db.Column(db.String(20))  # pending, approved, needs_changes
    testing_status = db.Column(db.String(20))  # not_tested, passed, failed
    ai_model_metrics = db.Column(db.Text)  # JSON string
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='tasks')
    parent_task = db.relationship('Task', remote_side=[id], backref='subtasks')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_id': self.project_id,
            'parent_task_id': self.parent_task_id,
            'assigned_to': self.assigned_to,
            'assigned_by': self.assigned_by,
            'status': self.status,
            'priority': self.priority,
            'difficulty': self.difficulty,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'tags': self.tags,
            'dependencies': self.dependencies,
            'attachments': self.attachments,
            'comments': self.comments,
            'progress_percentage': self.progress_percentage,
            'quality_score': self.quality_score,
            'code_review_status': self.code_review_status,
            'testing_status': self.testing_status,
            'ai_model_metrics': self.ai_model_metrics,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProjectTeam(db.Model):
    __tablename__ = 'project_teams'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    role_in_project = db.Column(db.String(50))  # project_manager, developer, designer, tester, etc.
    responsibilities = db.Column(db.Text)  # JSON string
    access_level = db.Column(db.String(20), default='read')  # read, write, admin
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    performance_rating = db.Column(db.Integer)  # 1-10
    contribution_percentage = db.Column(db.Integer)
    billable_rate = db.Column(db.Numeric(10, 2))

    # Relationships
    project = db.relationship('Project', backref='team_members')
    user = db.relationship('User', backref='project_memberships')

    def __repr__(self):
        return f'<ProjectTeam {self.project_id}:{self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'role_in_project': self.role_in_project,
            'responsibilities': self.responsibilities,
            'access_level': self.access_level,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'left_at': self.left_at.isoformat() if self.left_at else None,
            'is_active': self.is_active,
            'performance_rating': self.performance_rating,
            'contribution_percentage': self.contribution_percentage,
            'billable_rate': float(self.billable_rate) if self.billable_rate else None
        }


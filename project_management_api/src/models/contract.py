from src.models.user import db
from datetime import datetime
import uuid

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    contract_type = db.Column(db.String(50))  # fixed_price, hourly, milestone_based, retainer
    client_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    total_value = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3), default='USD')
    payment_terms = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, active, completed, terminated, expired
    payment_schedule = db.Column(db.Text)  # JSON string
    milestones = db.Column(db.Text)  # JSON string
    deliverables = db.Column(db.Text)  # JSON string
    terms_and_conditions = db.Column(db.Text)
    penalty_clauses = db.Column(db.Text)  # JSON string
    bonus_clauses = db.Column(db.Text)  # JSON string
    intellectual_property_terms = db.Column(db.Text)
    confidentiality_terms = db.Column(db.Text)
    termination_conditions = db.Column(db.Text)
    renewal_options = db.Column(db.Text)  # JSON string
    signed_by_client = db.Column(db.Boolean, default=False)
    signed_by_company = db.Column(db.Boolean, default=False)
    client_signature_date = db.Column(db.DateTime)
    company_signature_date = db.Column(db.DateTime)
    contract_file_url = db.Column(db.String(500))
    amendments = db.Column(db.Text)  # JSON string
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = db.relationship('User', foreign_keys=[client_id])
    project = db.relationship('Project', backref='contracts')
    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Contract {self.contract_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'contract_number': self.contract_number,
            'title': self.title,
            'description': self.description,
            'contract_type': self.contract_type,
            'client_id': self.client_id,
            'project_id': self.project_id,
            'total_value': float(self.total_value) if self.total_value else None,
            'currency': self.currency,
            'payment_terms': self.payment_terms,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'payment_schedule': self.payment_schedule,
            'milestones': self.milestones,
            'deliverables': self.deliverables,
            'terms_and_conditions': self.terms_and_conditions,
            'penalty_clauses': self.penalty_clauses,
            'bonus_clauses': self.bonus_clauses,
            'intellectual_property_terms': self.intellectual_property_terms,
            'confidentiality_terms': self.confidentiality_terms,
            'termination_conditions': self.termination_conditions,
            'renewal_options': self.renewal_options,
            'signed_by_client': self.signed_by_client,
            'signed_by_company': self.signed_by_company,
            'client_signature_date': self.client_signature_date.isoformat() if self.client_signature_date else None,
            'company_signature_date': self.company_signature_date.isoformat() if self.company_signature_date else None,
            'contract_file_url': self.contract_file_url,
            'amendments': self.amendments,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Cost(db.Model):
    __tablename__ = 'costs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    contract_id = db.Column(db.String(36), db.ForeignKey('contracts.id'))
    category = db.Column(db.String(50))  # labor, software, hardware, infrastructure, training, etc.
    subcategory = db.Column(db.String(50))
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    cost_type = db.Column(db.String(20))  # fixed, variable, recurring
    billing_type = db.Column(db.String(20))  # billable, non_billable, internal
    date_incurred = db.Column(db.DateTime, default=datetime.utcnow)
    payment_date = db.Column(db.DateTime)
    vendor = db.Column(db.String(200))
    invoice_number = db.Column(db.String(100))
    receipt_url = db.Column(db.String(500))
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, paid
    budget_allocation_id = db.Column(db.String(36), db.ForeignKey('budgets.id'))
    tax_amount = db.Column(db.Numeric(10, 2))
    tax_rate = db.Column(db.Numeric(5, 2))
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='costs')
    contract = db.relationship('Contract', backref='costs')
    approver = db.relationship('User', foreign_keys=[approved_by])
    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Cost {self.description}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'contract_id': self.contract_id,
            'category': self.category,
            'subcategory': self.subcategory,
            'description': self.description,
            'amount': float(self.amount),
            'currency': self.currency,
            'cost_type': self.cost_type,
            'billing_type': self.billing_type,
            'date_incurred': self.date_incurred.isoformat() if self.date_incurred else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'vendor': self.vendor,
            'invoice_number': self.invoice_number,
            'receipt_url': self.receipt_url,
            'approved_by': self.approved_by,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'status': self.status,
            'budget_allocation_id': self.budget_allocation_id,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'tax_rate': float(self.tax_rate) if self.tax_rate else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_budget = db.Column(db.Numeric(12, 2), nullable=False)
    allocated_budget = db.Column(db.Numeric(12, 2), default=0)
    spent_budget = db.Column(db.Numeric(12, 2), default=0)
    remaining_budget = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3), default='USD')
    budget_period = db.Column(db.String(20))  # monthly, quarterly, yearly, project_lifetime
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    categories = db.Column(db.Text)  # JSON string
    approval_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    revision_number = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='budgets')
    approver = db.relationship('User', foreign_keys=[approved_by])
    creator = db.relationship('User', foreign_keys=[created_by])
    cost_allocations = db.relationship('Cost', backref='budget_allocation')

    def __repr__(self):
        return f'<Budget {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'total_budget': float(self.total_budget),
            'allocated_budget': float(self.allocated_budget),
            'spent_budget': float(self.spent_budget),
            'remaining_budget': float(self.remaining_budget) if self.remaining_budget else None,
            'currency': self.currency,
            'budget_period': self.budget_period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'categories': self.categories,
            'approval_status': self.approval_status,
            'approved_by': self.approved_by,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'revision_number': self.revision_number,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


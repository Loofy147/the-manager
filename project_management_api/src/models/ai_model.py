from src.models.user import db
from datetime import datetime
import uuid

class AIModel(db.Model):
    __tablename__ = 'ai_models'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    model_type = db.Column(db.String(50))  # classification, regression, clustering, nlp, computer_vision, etc.
    algorithm = db.Column(db.String(100))  # random_forest, neural_network, svm, etc.
    framework = db.Column(db.String(50))  # tensorflow, pytorch, scikit-learn, etc.
    version = db.Column(db.String(20))
    training_dataset_id = db.Column(db.String(36), db.ForeignKey('datasets.id'))
    validation_dataset_id = db.Column(db.String(36), db.ForeignKey('datasets.id'))
    test_dataset_id = db.Column(db.String(36), db.ForeignKey('datasets.id'))
    hyperparameters = db.Column(db.Text)  # JSON string
    performance_metrics = db.Column(db.Text)  # JSON string
    training_duration = db.Column(db.Integer)  # في الدقائق
    model_size = db.Column(db.Integer)  # في الميجابايت
    inference_time = db.Column(db.Float)  # في الميلي ثانية
    deployment_status = db.Column(db.String(20), default='development')  # development, staging, production, retired
    model_file_url = db.Column(db.String(500))
    documentation_url = db.Column(db.String(500))
    api_endpoint = db.Column(db.String(500))
    monitoring_metrics = db.Column(db.Text)  # JSON string
    bias_assessment = db.Column(db.Text)  # JSON string
    explainability_report = db.Column(db.Text)
    compliance_status = db.Column(db.String(50))
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='ai_models')
    training_dataset = db.relationship('Dataset', foreign_keys=[training_dataset_id])
    validation_dataset = db.relationship('Dataset', foreign_keys=[validation_dataset_id])
    test_dataset = db.relationship('Dataset', foreign_keys=[test_dataset_id])
    creator = db.relationship('User', backref='created_ai_models')

    def __repr__(self):
        return f'<AIModel {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_id': self.project_id,
            'model_type': self.model_type,
            'algorithm': self.algorithm,
            'framework': self.framework,
            'version': self.version,
            'training_dataset_id': self.training_dataset_id,
            'validation_dataset_id': self.validation_dataset_id,
            'test_dataset_id': self.test_dataset_id,
            'hyperparameters': self.hyperparameters,
            'performance_metrics': self.performance_metrics,
            'training_duration': self.training_duration,
            'model_size': self.model_size,
            'inference_time': self.inference_time,
            'deployment_status': self.deployment_status,
            'model_file_url': self.model_file_url,
            'documentation_url': self.documentation_url,
            'api_endpoint': self.api_endpoint,
            'monitoring_metrics': self.monitoring_metrics,
            'bias_assessment': self.bias_assessment,
            'explainability_report': self.explainability_report,
            'compliance_status': self.compliance_status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Dataset(db.Model):
    __tablename__ = 'datasets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    dataset_type = db.Column(db.String(20))  # training, validation, test, production
    data_source = db.Column(db.String(100))  # internal, external, synthetic, web_scraping, etc.
    file_format = db.Column(db.String(20))  # csv, json, parquet, images, audio, video, etc.
    file_size = db.Column(db.Integer)  # في الميجابايت
    record_count = db.Column(db.Integer)
    feature_count = db.Column(db.Integer)
    target_variable = db.Column(db.String(100))
    data_quality_score = db.Column(db.Integer)  # 1-10
    missing_values_percentage = db.Column(db.Float)
    duplicate_records_percentage = db.Column(db.Float)
    data_schema = db.Column(db.Text)  # JSON string
    preprocessing_steps = db.Column(db.Text)  # JSON string
    data_lineage = db.Column(db.Text)  # JSON string
    privacy_level = db.Column(db.String(20))  # public, internal, confidential, restricted
    retention_period = db.Column(db.Integer)  # في الأيام
    storage_location = db.Column(db.String(500))
    access_permissions = db.Column(db.Text)  # JSON string
    last_updated = db.Column(db.DateTime)
    version = db.Column(db.String(20))
    checksum = db.Column(db.String(64))
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='datasets')
    creator = db.relationship('User', backref='created_datasets')

    def __repr__(self):
        return f'<Dataset {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_id': self.project_id,
            'dataset_type': self.dataset_type,
            'data_source': self.data_source,
            'file_format': self.file_format,
            'file_size': self.file_size,
            'record_count': self.record_count,
            'feature_count': self.feature_count,
            'target_variable': self.target_variable,
            'data_quality_score': self.data_quality_score,
            'missing_values_percentage': self.missing_values_percentage,
            'duplicate_records_percentage': self.duplicate_records_percentage,
            'data_schema': self.data_schema,
            'preprocessing_steps': self.preprocessing_steps,
            'data_lineage': self.data_lineage,
            'privacy_level': self.privacy_level,
            'retention_period': self.retention_period,
            'storage_location': self.storage_location,
            'access_permissions': self.access_permissions,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'version': self.version,
            'checksum': self.checksum,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50))  # project_status, financial, performance, ai_model_performance, etc.
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    generated_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_period_start = db.Column(db.DateTime)
    report_period_end = db.Column(db.DateTime)
    data_sources = db.Column(db.Text)  # JSON string
    metrics = db.Column(db.Text)  # JSON string
    visualizations = db.Column(db.Text)  # JSON string
    insights = db.Column(db.Text)  # JSON string
    recommendations = db.Column(db.Text)  # JSON string
    file_url = db.Column(db.String(500))
    sharing_permissions = db.Column(db.Text)  # JSON string
    is_automated = db.Column(db.Boolean, default=False)
    schedule = db.Column(db.String(100))  # للتقارير المجدولة
    next_generation = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='completed')  # generating, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='reports')
    generator = db.relationship('User', backref='generated_reports')

    def __repr__(self):
        return f'<Report {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'report_type': self.report_type,
            'project_id': self.project_id,
            'generated_by': self.generated_by,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'report_period_start': self.report_period_start.isoformat() if self.report_period_start else None,
            'report_period_end': self.report_period_end.isoformat() if self.report_period_end else None,
            'data_sources': self.data_sources,
            'metrics': self.metrics,
            'visualizations': self.visualizations,
            'insights': self.insights,
            'recommendations': self.recommendations,
            'file_url': self.file_url,
            'sharing_permissions': self.sharing_permissions,
            'is_automated': self.is_automated,
            'schedule': self.schedule,
            'next_generation': self.next_generation.isoformat() if self.next_generation else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Metrics(db.Model):
    __tablename__ = 'metrics'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    metric_type = db.Column(db.String(50))  # productivity, quality, performance, cost, etc.
    metric_name = db.Column(db.String(100))
    metric_value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    context = db.Column(db.Text)  # JSON string
    benchmark_value = db.Column(db.Float)
    target_value = db.Column(db.Float)
    trend = db.Column(db.String(20))  # improving, declining, stable
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='metrics')
    user = db.relationship('User', backref='metrics')

    def __repr__(self):
        return f'<Metrics {self.metric_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'metric_type': self.metric_type,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'unit': self.unit,
            'measurement_date': self.measurement_date.isoformat() if self.measurement_date else None,
            'context': self.context,
            'benchmark_value': self.benchmark_value,
            'target_value': self.target_value,
            'trend': self.trend,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


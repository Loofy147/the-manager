from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.ai_model import AIModel, Dataset, Report, Metrics
from datetime import datetime
import json

ai_model_bp = Blueprint('ai_model', __name__)

# AI Model endpoints

@ai_model_bp.route('/ai-models', methods=['GET'])
def get_ai_models():
    """Get all AI models with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    project_id = request.args.get('project_id')
    model_type = request.args.get('model_type')
    framework = request.args.get('framework')
    deployment_status = request.args.get('deployment_status')
    search = request.args.get('search', '')
    
    query = AIModel.query
    
    if project_id:
        query = query.filter(AIModel.project_id == project_id)
    
    if model_type:
        query = query.filter(AIModel.model_type == model_type)
    
    if framework:
        query = query.filter(AIModel.framework == framework)
    
    if deployment_status:
        query = query.filter(AIModel.deployment_status == deployment_status)
    
    if search:
        query = query.filter(
            (AIModel.name.contains(search)) |
            (AIModel.description.contains(search))
        )
    
    models = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ai_models': [model.to_dict() for model in models.items],
        'total': models.total,
        'pages': models.pages,
        'current_page': page,
        'per_page': per_page
    })

@ai_model_bp.route('/ai-models', methods=['POST'])
def create_ai_model():
    """Create a new AI model"""
    data = request.json
    
    ai_model = AIModel(
        name=data['name'],
        description=data.get('description'),
        project_id=data.get('project_id'),
        model_type=data.get('model_type'),
        algorithm=data.get('algorithm'),
        framework=data.get('framework'),
        version=data.get('version', '1.0'),
        training_dataset_id=data.get('training_dataset_id'),
        validation_dataset_id=data.get('validation_dataset_id'),
        test_dataset_id=data.get('test_dataset_id'),
        hyperparameters=json.dumps(data.get('hyperparameters', {})),
        performance_metrics=json.dumps(data.get('performance_metrics', {})),
        training_duration=data.get('training_duration'),
        model_size=data.get('model_size'),
        inference_time=data.get('inference_time'),
        deployment_status=data.get('deployment_status', 'development'),
        model_file_url=data.get('model_file_url'),
        documentation_url=data.get('documentation_url'),
        api_endpoint=data.get('api_endpoint'),
        monitoring_metrics=json.dumps(data.get('monitoring_metrics', {})),
        bias_assessment=json.dumps(data.get('bias_assessment', {})),
        explainability_report=data.get('explainability_report'),
        compliance_status=data.get('compliance_status'),
        created_by=data.get('created_by')
    )
    
    db.session.add(ai_model)
    db.session.commit()
    return jsonify(ai_model.to_dict()), 201

@ai_model_bp.route('/ai-models/<model_id>', methods=['GET'])
def get_ai_model(model_id):
    """Get a specific AI model by ID"""
    ai_model = AIModel.query.get_or_404(model_id)
    model_data = ai_model.to_dict()
    
    # Include dataset information
    if ai_model.training_dataset:
        model_data['training_dataset'] = ai_model.training_dataset.to_dict()
    if ai_model.validation_dataset:
        model_data['validation_dataset'] = ai_model.validation_dataset.to_dict()
    if ai_model.test_dataset:
        model_data['test_dataset'] = ai_model.test_dataset.to_dict()
    
    return jsonify(model_data)

@ai_model_bp.route('/ai-models/<model_id>', methods=['PUT'])
def update_ai_model(model_id):
    """Update an AI model"""
    ai_model = AIModel.query.get_or_404(model_id)
    data = request.json
    
    ai_model.name = data.get('name', ai_model.name)
    ai_model.description = data.get('description', ai_model.description)
    ai_model.model_type = data.get('model_type', ai_model.model_type)
    ai_model.algorithm = data.get('algorithm', ai_model.algorithm)
    ai_model.framework = data.get('framework', ai_model.framework)
    ai_model.version = data.get('version', ai_model.version)
    ai_model.training_dataset_id = data.get('training_dataset_id', ai_model.training_dataset_id)
    ai_model.validation_dataset_id = data.get('validation_dataset_id', ai_model.validation_dataset_id)
    ai_model.test_dataset_id = data.get('test_dataset_id', ai_model.test_dataset_id)
    ai_model.training_duration = data.get('training_duration', ai_model.training_duration)
    ai_model.model_size = data.get('model_size', ai_model.model_size)
    ai_model.inference_time = data.get('inference_time', ai_model.inference_time)
    ai_model.deployment_status = data.get('deployment_status', ai_model.deployment_status)
    ai_model.model_file_url = data.get('model_file_url', ai_model.model_file_url)
    ai_model.documentation_url = data.get('documentation_url', ai_model.documentation_url)
    ai_model.api_endpoint = data.get('api_endpoint', ai_model.api_endpoint)
    ai_model.explainability_report = data.get('explainability_report', ai_model.explainability_report)
    ai_model.compliance_status = data.get('compliance_status', ai_model.compliance_status)
    
    if 'hyperparameters' in data:
        ai_model.hyperparameters = json.dumps(data['hyperparameters'])
    
    if 'performance_metrics' in data:
        ai_model.performance_metrics = json.dumps(data['performance_metrics'])
    
    if 'monitoring_metrics' in data:
        ai_model.monitoring_metrics = json.dumps(data['monitoring_metrics'])
    
    if 'bias_assessment' in data:
        ai_model.bias_assessment = json.dumps(data['bias_assessment'])
    
    ai_model.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(ai_model.to_dict())

@ai_model_bp.route('/ai-models/<model_id>', methods=['DELETE'])
def delete_ai_model(model_id):
    """Delete an AI model"""
    ai_model = AIModel.query.get_or_404(model_id)
    db.session.delete(ai_model)
    db.session.commit()
    return '', 204

@ai_model_bp.route('/ai-models/<model_id>/deploy', methods=['POST'])
def deploy_ai_model(model_id):
    """Deploy an AI model to a specific environment"""
    ai_model = AIModel.query.get_or_404(model_id)
    data = request.json
    
    deployment_status = data.get('deployment_status', 'staging')
    api_endpoint = data.get('api_endpoint')
    
    ai_model.deployment_status = deployment_status
    if api_endpoint:
        ai_model.api_endpoint = api_endpoint
    
    ai_model.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': f'Model deployed to {deployment_status}',
        'model': ai_model.to_dict()
    })

# Dataset endpoints

@ai_model_bp.route('/datasets', methods=['GET'])
def get_datasets():
    """Get all datasets with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    project_id = request.args.get('project_id')
    dataset_type = request.args.get('dataset_type')
    data_source = request.args.get('data_source')
    privacy_level = request.args.get('privacy_level')
    search = request.args.get('search', '')
    
    query = Dataset.query
    
    if project_id:
        query = query.filter(Dataset.project_id == project_id)
    
    if dataset_type:
        query = query.filter(Dataset.dataset_type == dataset_type)
    
    if data_source:
        query = query.filter(Dataset.data_source == data_source)
    
    if privacy_level:
        query = query.filter(Dataset.privacy_level == privacy_level)
    
    if search:
        query = query.filter(
            (Dataset.name.contains(search)) |
            (Dataset.description.contains(search))
        )
    
    datasets = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'datasets': [dataset.to_dict() for dataset in datasets.items],
        'total': datasets.total,
        'pages': datasets.pages,
        'current_page': page,
        'per_page': per_page
    })

@ai_model_bp.route('/datasets', methods=['POST'])
def create_dataset():
    """Create a new dataset"""
    data = request.json
    
    dataset = Dataset(
        name=data['name'],
        description=data.get('description'),
        project_id=data.get('project_id'),
        dataset_type=data.get('dataset_type'),
        data_source=data.get('data_source'),
        file_format=data.get('file_format'),
        file_size=data.get('file_size'),
        record_count=data.get('record_count'),
        feature_count=data.get('feature_count'),
        target_variable=data.get('target_variable'),
        data_quality_score=data.get('data_quality_score'),
        missing_values_percentage=data.get('missing_values_percentage'),
        duplicate_records_percentage=data.get('duplicate_records_percentage'),
        data_schema=json.dumps(data.get('data_schema', {})),
        preprocessing_steps=json.dumps(data.get('preprocessing_steps', [])),
        data_lineage=json.dumps(data.get('data_lineage', [])),
        privacy_level=data.get('privacy_level', 'internal'),
        retention_period=data.get('retention_period'),
        storage_location=data.get('storage_location'),
        access_permissions=json.dumps(data.get('access_permissions', [])),
        last_updated=datetime.fromisoformat(data['last_updated']) if data.get('last_updated') else datetime.utcnow(),
        version=data.get('version', '1.0'),
        checksum=data.get('checksum'),
        created_by=data.get('created_by')
    )
    
    db.session.add(dataset)
    db.session.commit()
    return jsonify(dataset.to_dict()), 201

@ai_model_bp.route('/datasets/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    """Get a specific dataset by ID"""
    dataset = Dataset.query.get_or_404(dataset_id)
    dataset_data = dataset.to_dict()
    
    # Include models that use this dataset
    training_models = AIModel.query.filter_by(training_dataset_id=dataset_id).all()
    validation_models = AIModel.query.filter_by(validation_dataset_id=dataset_id).all()
    test_models = AIModel.query.filter_by(test_dataset_id=dataset_id).all()
    
    dataset_data['used_in_models'] = {
        'training': [model.to_dict() for model in training_models],
        'validation': [model.to_dict() for model in validation_models],
        'test': [model.to_dict() for model in test_models]
    }
    
    return jsonify(dataset_data)

@ai_model_bp.route('/datasets/<dataset_id>', methods=['PUT'])
def update_dataset(dataset_id):
    """Update a dataset"""
    dataset = Dataset.query.get_or_404(dataset_id)
    data = request.json
    
    dataset.name = data.get('name', dataset.name)
    dataset.description = data.get('description', dataset.description)
    dataset.dataset_type = data.get('dataset_type', dataset.dataset_type)
    dataset.data_source = data.get('data_source', dataset.data_source)
    dataset.file_format = data.get('file_format', dataset.file_format)
    dataset.file_size = data.get('file_size', dataset.file_size)
    dataset.record_count = data.get('record_count', dataset.record_count)
    dataset.feature_count = data.get('feature_count', dataset.feature_count)
    dataset.target_variable = data.get('target_variable', dataset.target_variable)
    dataset.data_quality_score = data.get('data_quality_score', dataset.data_quality_score)
    dataset.missing_values_percentage = data.get('missing_values_percentage', dataset.missing_values_percentage)
    dataset.duplicate_records_percentage = data.get('duplicate_records_percentage', dataset.duplicate_records_percentage)
    dataset.privacy_level = data.get('privacy_level', dataset.privacy_level)
    dataset.retention_period = data.get('retention_period', dataset.retention_period)
    dataset.storage_location = data.get('storage_location', dataset.storage_location)
    dataset.version = data.get('version', dataset.version)
    dataset.checksum = data.get('checksum', dataset.checksum)
    
    if data.get('last_updated'):
        dataset.last_updated = datetime.fromisoformat(data['last_updated'])
    
    if 'data_schema' in data:
        dataset.data_schema = json.dumps(data['data_schema'])
    
    if 'preprocessing_steps' in data:
        dataset.preprocessing_steps = json.dumps(data['preprocessing_steps'])
    
    if 'data_lineage' in data:
        dataset.data_lineage = json.dumps(data['data_lineage'])
    
    if 'access_permissions' in data:
        dataset.access_permissions = json.dumps(data['access_permissions'])
    
    db.session.commit()
    return jsonify(dataset.to_dict())

@ai_model_bp.route('/datasets/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    """Delete a dataset"""
    dataset = Dataset.query.get_or_404(dataset_id)
    
    # Check if dataset is being used by any models
    models_using_dataset = AIModel.query.filter(
        (AIModel.training_dataset_id == dataset_id) |
        (AIModel.validation_dataset_id == dataset_id) |
        (AIModel.test_dataset_id == dataset_id)
    ).count()
    
    if models_using_dataset > 0:
        return jsonify({'error': 'Cannot delete dataset that is being used by AI models'}), 400
    
    db.session.delete(dataset)
    db.session.commit()
    return '', 204

# Report endpoints

@ai_model_bp.route('/reports', methods=['GET'])
def get_reports():
    """Get all reports with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    project_id = request.args.get('project_id')
    report_type = request.args.get('report_type')
    generated_by = request.args.get('generated_by')
    status = request.args.get('status')
    
    query = Report.query
    
    if project_id:
        query = query.filter(Report.project_id == project_id)
    
    if report_type:
        query = query.filter(Report.report_type == report_type)
    
    if generated_by:
        query = query.filter(Report.generated_by == generated_by)
    
    if status:
        query = query.filter(Report.status == status)
    
    reports = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reports': [report.to_dict() for report in reports.items],
        'total': reports.total,
        'pages': reports.pages,
        'current_page': page,
        'per_page': per_page
    })

@ai_model_bp.route('/reports', methods=['POST'])
def create_report():
    """Create a new report"""
    data = request.json
    
    report = Report(
        title=data['title'],
        description=data.get('description'),
        report_type=data.get('report_type'),
        project_id=data.get('project_id'),
        generated_by=data.get('generated_by'),
        report_period_start=datetime.fromisoformat(data['report_period_start']) if data.get('report_period_start') else None,
        report_period_end=datetime.fromisoformat(data['report_period_end']) if data.get('report_period_end') else None,
        data_sources=json.dumps(data.get('data_sources', [])),
        metrics=json.dumps(data.get('metrics', {})),
        visualizations=json.dumps(data.get('visualizations', [])),
        insights=json.dumps(data.get('insights', [])),
        recommendations=json.dumps(data.get('recommendations', [])),
        file_url=data.get('file_url'),
        sharing_permissions=json.dumps(data.get('sharing_permissions', [])),
        is_automated=data.get('is_automated', False),
        schedule=data.get('schedule'),
        next_generation=datetime.fromisoformat(data['next_generation']) if data.get('next_generation') else None,
        status=data.get('status', 'completed')
    )
    
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201

@ai_model_bp.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    """Get a specific report by ID"""
    report = Report.query.get_or_404(report_id)
    return jsonify(report.to_dict())

@ai_model_bp.route('/reports/<report_id>', methods=['PUT'])
def update_report(report_id):
    """Update a report"""
    report = Report.query.get_or_404(report_id)
    data = request.json
    
    report.title = data.get('title', report.title)
    report.description = data.get('description', report.description)
    report.report_type = data.get('report_type', report.report_type)
    report.file_url = data.get('file_url', report.file_url)
    report.is_automated = data.get('is_automated', report.is_automated)
    report.schedule = data.get('schedule', report.schedule)
    report.status = data.get('status', report.status)
    
    if data.get('report_period_start'):
        report.report_period_start = datetime.fromisoformat(data['report_period_start'])
    
    if data.get('report_period_end'):
        report.report_period_end = datetime.fromisoformat(data['report_period_end'])
    
    if data.get('next_generation'):
        report.next_generation = datetime.fromisoformat(data['next_generation'])
    
    if 'data_sources' in data:
        report.data_sources = json.dumps(data['data_sources'])
    
    if 'metrics' in data:
        report.metrics = json.dumps(data['metrics'])
    
    if 'visualizations' in data:
        report.visualizations = json.dumps(data['visualizations'])
    
    if 'insights' in data:
        report.insights = json.dumps(data['insights'])
    
    if 'recommendations' in data:
        report.recommendations = json.dumps(data['recommendations'])
    
    if 'sharing_permissions' in data:
        report.sharing_permissions = json.dumps(data['sharing_permissions'])
    
    db.session.commit()
    return jsonify(report.to_dict())

@ai_model_bp.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Delete a report"""
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    return '', 204

# Metrics endpoints

@ai_model_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get all metrics with optional filtering"""
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    metric_type = request.args.get('metric_type')
    metric_name = request.args.get('metric_name')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Metrics.query
    
    if project_id:
        query = query.filter(Metrics.project_id == project_id)
    
    if user_id:
        query = query.filter(Metrics.user_id == user_id)
    
    if metric_type:
        query = query.filter(Metrics.metric_type == metric_type)
    
    if metric_name:
        query = query.filter(Metrics.metric_name == metric_name)
    
    if date_from:
        query = query.filter(Metrics.measurement_date >= datetime.fromisoformat(date_from))
    
    if date_to:
        query = query.filter(Metrics.measurement_date <= datetime.fromisoformat(date_to))
    
    metrics = query.all()
    return jsonify([metric.to_dict() for metric in metrics])

@ai_model_bp.route('/metrics', methods=['POST'])
def create_metric():
    """Create a new metric entry"""
    data = request.json
    
    metric = Metrics(
        project_id=data.get('project_id'),
        user_id=data.get('user_id'),
        metric_type=data.get('metric_type'),
        metric_name=data['metric_name'],
        metric_value=data['metric_value'],
        unit=data.get('unit'),
        measurement_date=datetime.fromisoformat(data['measurement_date']) if data.get('measurement_date') else datetime.utcnow(),
        context=json.dumps(data.get('context', {})),
        benchmark_value=data.get('benchmark_value'),
        target_value=data.get('target_value'),
        trend=data.get('trend')
    )
    
    db.session.add(metric)
    db.session.commit()
    return jsonify(metric.to_dict()), 201

@ai_model_bp.route('/metrics/<metric_id>', methods=['GET'])
def get_metric(metric_id):
    """Get a specific metric by ID"""
    metric = Metrics.query.get_or_404(metric_id)
    return jsonify(metric.to_dict())

@ai_model_bp.route('/metrics/<metric_id>', methods=['PUT'])
def update_metric(metric_id):
    """Update a metric entry"""
    metric = Metrics.query.get_or_404(metric_id)
    data = request.json
    
    metric.metric_type = data.get('metric_type', metric.metric_type)
    metric.metric_name = data.get('metric_name', metric.metric_name)
    metric.metric_value = data.get('metric_value', metric.metric_value)
    metric.unit = data.get('unit', metric.unit)
    metric.benchmark_value = data.get('benchmark_value', metric.benchmark_value)
    metric.target_value = data.get('target_value', metric.target_value)
    metric.trend = data.get('trend', metric.trend)
    
    if data.get('measurement_date'):
        metric.measurement_date = datetime.fromisoformat(data['measurement_date'])
    
    if 'context' in data:
        metric.context = json.dumps(data['context'])
    
    db.session.commit()
    return jsonify(metric.to_dict())

@ai_model_bp.route('/metrics/<metric_id>', methods=['DELETE'])
def delete_metric(metric_id):
    """Delete a metric entry"""
    metric = Metrics.query.get_or_404(metric_id)
    db.session.delete(metric)
    db.session.commit()
    return '', 204

# Analytics endpoints

@ai_model_bp.route('/analytics/model-performance', methods=['GET'])
def get_model_performance_analytics():
    """Get AI model performance analytics"""
    project_id = request.args.get('project_id')
    model_type = request.args.get('model_type')
    framework = request.args.get('framework')
    
    query = AIModel.query
    
    if project_id:
        query = query.filter(AIModel.project_id == project_id)
    
    if model_type:
        query = query.filter(AIModel.model_type == model_type)
    
    if framework:
        query = query.filter(AIModel.framework == framework)
    
    models = query.all()
    
    # Calculate analytics
    total_models = len(models)
    deployed_models = len([m for m in models if m.deployment_status == 'production'])
    avg_training_duration = sum(m.training_duration for m in models if m.training_duration) / total_models if total_models > 0 else 0
    avg_inference_time = sum(m.inference_time for m in models if m.inference_time) / total_models if total_models > 0 else 0
    
    # Group by deployment status
    status_distribution = {}
    for model in models:
        status = model.deployment_status
        status_distribution[status] = status_distribution.get(status, 0) + 1
    
    # Group by model type
    type_distribution = {}
    for model in models:
        model_type = model.model_type
        type_distribution[model_type] = type_distribution.get(model_type, 0) + 1
    
    return jsonify({
        'total_models': total_models,
        'deployed_models': deployed_models,
        'deployment_rate': (deployed_models / total_models * 100) if total_models > 0 else 0,
        'avg_training_duration_minutes': avg_training_duration,
        'avg_inference_time_ms': avg_inference_time,
        'status_distribution': status_distribution,
        'type_distribution': type_distribution,
        'models': [model.to_dict() for model in models]
    })

@ai_model_bp.route('/analytics/dataset-quality', methods=['GET'])
def get_dataset_quality_analytics():
    """Get dataset quality analytics"""
    project_id = request.args.get('project_id')
    dataset_type = request.args.get('dataset_type')
    
    query = Dataset.query
    
    if project_id:
        query = query.filter(Dataset.project_id == project_id)
    
    if dataset_type:
        query = query.filter(Dataset.dataset_type == dataset_type)
    
    datasets = query.all()
    
    # Calculate analytics
    total_datasets = len(datasets)
    avg_quality_score = sum(d.data_quality_score for d in datasets if d.data_quality_score) / total_datasets if total_datasets > 0 else 0
    avg_missing_values = sum(d.missing_values_percentage for d in datasets if d.missing_values_percentage) / total_datasets if total_datasets > 0 else 0
    avg_duplicates = sum(d.duplicate_records_percentage for d in datasets if d.duplicate_records_percentage) / total_datasets if total_datasets > 0 else 0
    
    # Group by privacy level
    privacy_distribution = {}
    for dataset in datasets:
        privacy = dataset.privacy_level
        privacy_distribution[privacy] = privacy_distribution.get(privacy, 0) + 1
    
    # Group by data source
    source_distribution = {}
    for dataset in datasets:
        source = dataset.data_source
        source_distribution[source] = source_distribution.get(source, 0) + 1
    
    return jsonify({
        'total_datasets': total_datasets,
        'avg_quality_score': avg_quality_score,
        'avg_missing_values_percentage': avg_missing_values,
        'avg_duplicate_records_percentage': avg_duplicates,
        'privacy_distribution': privacy_distribution,
        'source_distribution': source_distribution,
        'datasets': [dataset.to_dict() for dataset in datasets]
    })


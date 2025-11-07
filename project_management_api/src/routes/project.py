from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.project import Project, Task, ProjectTeam
from datetime import datetime
import json

project_bp = Blueprint('project', __name__)

# Project endpoints

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    project_type = request.args.get('project_type')
    priority = request.args.get('priority')
    project_manager_id = request.args.get('project_manager_id')
    client_id = request.args.get('client_id')
    search = request.args.get('search', '')
    is_archived = request.args.get('is_archived', 'false').lower() == 'true'
    
    query = Project.query.filter(Project.is_archived == is_archived)
    
    if status:
        query = query.filter(Project.status == status)
    
    if project_type:
        query = query.filter(Project.project_type == project_type)
    
    if priority:
        query = query.filter(Project.priority == priority)
    
    if project_manager_id:
        query = query.filter(Project.project_manager_id == project_manager_id)
    
    if client_id:
        query = query.filter(Project.client_id == client_id)
    
    if search:
        query = query.filter(
            (Project.name.contains(search)) |
            (Project.description.contains(search))
        )
    
    projects = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'projects': [project.to_dict() for project in projects.items],
        'total': projects.total,
        'pages': projects.pages,
        'current_page': page,
        'per_page': per_page
    })

@project_bp.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.json
    
    project = Project(
        name=data['name'],
        description=data.get('description'),
        project_type=data.get('project_type'),
        ai_project_category=data.get('ai_project_category'),
        status=data.get('status', 'planning'),
        priority=data.get('priority', 'medium'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        estimated_duration=data.get('estimated_duration'),
        budget=data.get('budget'),
        currency=data.get('currency', 'USD'),
        client_id=data.get('client_id'),
        project_manager_id=data.get('project_manager_id'),
        team_lead_id=data.get('team_lead_id'),
        repository_url=data.get('repository_url'),
        documentation_url=data.get('documentation_url'),
        demo_url=data.get('demo_url'),
        technologies=json.dumps(data.get('technologies', [])),
        ai_frameworks=json.dumps(data.get('ai_frameworks', [])),
        datasets_used=json.dumps(data.get('datasets_used', [])),
        compliance_requirements=json.dumps(data.get('compliance_requirements', [])),
        risk_assessment=data.get('risk_assessment'),
        success_criteria=json.dumps(data.get('success_criteria', [])),
        created_by=data.get('created_by')
    )
    
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

@project_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project by ID"""
    project = Project.query.get_or_404(project_id)
    project_data = project.to_dict()
    
    # Include team members
    team_members = ProjectTeam.query.filter_by(project_id=project_id, is_active=True).all()
    project_data['team_members'] = [tm.to_dict() for tm in team_members]
    
    # Include task summary
    tasks = Task.query.filter_by(project_id=project_id).all()
    project_data['task_summary'] = {
        'total_tasks': len(tasks),
        'completed_tasks': len([t for t in tasks if t.status == 'completed']),
        'in_progress_tasks': len([t for t in tasks if t.status == 'in_progress']),
        'blocked_tasks': len([t for t in tasks if t.status == 'blocked'])
    }
    
    return jsonify(project_data)

@project_bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    project = Project.query.get_or_404(project_id)
    data = request.json
    
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.project_type = data.get('project_type', project.project_type)
    project.ai_project_category = data.get('ai_project_category', project.ai_project_category)
    project.status = data.get('status', project.status)
    project.priority = data.get('priority', project.priority)
    project.estimated_duration = data.get('estimated_duration', project.estimated_duration)
    project.actual_duration = data.get('actual_duration', project.actual_duration)
    project.budget = data.get('budget', project.budget)
    project.spent_budget = data.get('spent_budget', project.spent_budget)
    project.currency = data.get('currency', project.currency)
    project.client_id = data.get('client_id', project.client_id)
    project.project_manager_id = data.get('project_manager_id', project.project_manager_id)
    project.team_lead_id = data.get('team_lead_id', project.team_lead_id)
    project.repository_url = data.get('repository_url', project.repository_url)
    project.documentation_url = data.get('documentation_url', project.documentation_url)
    project.demo_url = data.get('demo_url', project.demo_url)
    project.deployment_environment = data.get('deployment_environment', project.deployment_environment)
    project.risk_assessment = data.get('risk_assessment', project.risk_assessment)
    
    if data.get('start_date'):
        project.start_date = datetime.fromisoformat(data['start_date'])
    
    if data.get('end_date'):
        project.end_date = datetime.fromisoformat(data['end_date'])
    
    if 'technologies' in data:
        project.technologies = json.dumps(data['technologies'])
    
    if 'ai_frameworks' in data:
        project.ai_frameworks = json.dumps(data['ai_frameworks'])
    
    if 'datasets_used' in data:
        project.datasets_used = json.dumps(data['datasets_used'])
    
    if 'compliance_requirements' in data:
        project.compliance_requirements = json.dumps(data['compliance_requirements'])
    
    if 'success_criteria' in data:
        project.success_criteria = json.dumps(data['success_criteria'])
    
    if 'model_performance_metrics' in data:
        project.model_performance_metrics = json.dumps(data['model_performance_metrics'])
    
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(project.to_dict())

@project_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Archive a project"""
    project = Project.query.get_or_404(project_id)
    project.is_archived = True
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return '', 204

# Task endpoints

@project_bp.route('/projects/<project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    """Get all tasks for a project"""
    status = request.args.get('status')
    assigned_to = request.args.get('assigned_to')
    priority = request.args.get('priority')
    parent_task_id = request.args.get('parent_task_id')
    
    query = Task.query.filter_by(project_id=project_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if parent_task_id:
        query = query.filter(Task.parent_task_id == parent_task_id)
    elif parent_task_id == 'null':
        query = query.filter(Task.parent_task_id.is_(None))
    
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])

@project_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.json
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        project_id=data['project_id'],
        parent_task_id=data.get('parent_task_id'),
        assigned_to=data.get('assigned_to'),
        assigned_by=data.get('assigned_by'),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        difficulty=data.get('difficulty', 'medium'),
        estimated_hours=data.get('estimated_hours'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
        tags=json.dumps(data.get('tags', [])),
        dependencies=json.dumps(data.get('dependencies', [])),
        attachments=json.dumps(data.get('attachments', [])),
        comments=json.dumps(data.get('comments', [])),
        created_by=data.get('created_by')
    )
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@project_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = Task.query.get_or_404(task_id)
    task_data = task.to_dict()
    
    # Include subtasks
    subtasks = Task.query.filter_by(parent_task_id=task_id).all()
    task_data['subtasks'] = [subtask.to_dict() for subtask in subtasks]
    
    return jsonify(task_data)

@project_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.assigned_to = data.get('assigned_to', task.assigned_to)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.difficulty = data.get('difficulty', task.difficulty)
    task.estimated_hours = data.get('estimated_hours', task.estimated_hours)
    task.actual_hours = data.get('actual_hours', task.actual_hours)
    task.progress_percentage = data.get('progress_percentage', task.progress_percentage)
    task.quality_score = data.get('quality_score', task.quality_score)
    task.code_review_status = data.get('code_review_status', task.code_review_status)
    task.testing_status = data.get('testing_status', task.testing_status)
    
    if data.get('start_date'):
        task.start_date = datetime.fromisoformat(data['start_date'])
    
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data['due_date'])
    
    if data.get('status') == 'completed' and not task.completed_at:
        task.completed_at = datetime.utcnow()
    
    if 'tags' in data:
        task.tags = json.dumps(data['tags'])
    
    if 'dependencies' in data:
        task.dependencies = json.dumps(data['dependencies'])
    
    if 'attachments' in data:
        task.attachments = json.dumps(data['attachments'])
    
    if 'comments' in data:
        task.comments = json.dumps(data['comments'])
    
    if 'ai_model_metrics' in data:
        task.ai_model_metrics = json.dumps(data['ai_model_metrics'])
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())

@project_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # Check if task has subtasks
    subtasks = Task.query.filter_by(parent_task_id=task_id).count()
    if subtasks > 0:
        return jsonify({'error': 'Cannot delete task with subtasks'}), 400
    
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Project Team endpoints

@project_bp.route('/projects/<project_id>/team', methods=['GET'])
def get_project_team(project_id):
    """Get project team members"""
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    team_members = ProjectTeam.query.filter_by(
        project_id=project_id,
        is_active=is_active
    ).all()
    
    return jsonify([tm.to_dict() for tm in team_members])

@project_bp.route('/projects/<project_id>/team', methods=['POST'])
def add_team_member():
    """Add a team member to a project"""
    data = request.json
    
    # Check if user is already in the project team
    existing = ProjectTeam.query.filter_by(
        project_id=data['project_id'],
        user_id=data['user_id'],
        is_active=True
    ).first()
    
    if existing:
        return jsonify({'error': 'User is already a team member'}), 400
    
    team_member = ProjectTeam(
        project_id=data['project_id'],
        user_id=data['user_id'],
        role_in_project=data.get('role_in_project'),
        responsibilities=json.dumps(data.get('responsibilities', [])),
        access_level=data.get('access_level', 'read'),
        billable_rate=data.get('billable_rate')
    )
    
    db.session.add(team_member)
    db.session.commit()
    return jsonify(team_member.to_dict()), 201

@project_bp.route('/project-team/<team_member_id>', methods=['PUT'])
def update_team_member(team_member_id):
    """Update a team member"""
    team_member = ProjectTeam.query.get_or_404(team_member_id)
    data = request.json
    
    team_member.role_in_project = data.get('role_in_project', team_member.role_in_project)
    team_member.access_level = data.get('access_level', team_member.access_level)
    team_member.performance_rating = data.get('performance_rating', team_member.performance_rating)
    team_member.contribution_percentage = data.get('contribution_percentage', team_member.contribution_percentage)
    team_member.billable_rate = data.get('billable_rate', team_member.billable_rate)
    team_member.is_active = data.get('is_active', team_member.is_active)
    
    if 'responsibilities' in data:
        team_member.responsibilities = json.dumps(data['responsibilities'])
    
    if data.get('is_active') == False and not team_member.left_at:
        team_member.left_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(team_member.to_dict())

@project_bp.route('/project-team/<team_member_id>', methods=['DELETE'])
def remove_team_member(team_member_id):
    """Remove a team member from a project"""
    team_member = ProjectTeam.query.get_or_404(team_member_id)
    team_member.is_active = False
    team_member.left_at = datetime.utcnow()
    db.session.commit()
    return '', 204

@project_bp.route('/users/<user_id>/projects', methods=['GET'])
def get_user_projects(user_id):
    """Get all projects for a specific user"""
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    team_memberships = ProjectTeam.query.filter_by(
        user_id=user_id,
        is_active=is_active
    ).all()
    
    result = []
    for tm in team_memberships:
        project_data = tm.project.to_dict()
        project_data['team_role'] = {
            'role_in_project': tm.role_in_project,
            'access_level': tm.access_level,
            'joined_at': tm.joined_at.isoformat() if tm.joined_at else None,
            'responsibilities': tm.responsibilities
        }
        result.append(project_data)
    
    return jsonify(result)

@project_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    """Advanced task search"""
    query = request.args.get('q', '')
    project_ids = request.args.getlist('project_ids')
    statuses = request.args.getlist('statuses')
    priorities = request.args.getlist('priorities')
    assigned_to = request.args.get('assigned_to')
    due_date_from = request.args.get('due_date_from')
    due_date_to = request.args.get('due_date_to')
    
    task_query = Task.query
    
    if query:
        task_query = task_query.filter(
            (Task.title.contains(query)) |
            (Task.description.contains(query))
        )
    
    if project_ids:
        task_query = task_query.filter(Task.project_id.in_(project_ids))
    
    if statuses:
        task_query = task_query.filter(Task.status.in_(statuses))
    
    if priorities:
        task_query = task_query.filter(Task.priority.in_(priorities))
    
    if assigned_to:
        task_query = task_query.filter(Task.assigned_to == assigned_to)
    
    if due_date_from:
        task_query = task_query.filter(Task.due_date >= datetime.fromisoformat(due_date_from))
    
    if due_date_to:
        task_query = task_query.filter(Task.due_date <= datetime.fromisoformat(due_date_to))
    
    tasks = task_query.all()
    return jsonify([task.to_dict() for task in tasks])


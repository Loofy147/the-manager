from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.role import Role, UserRole
from datetime import datetime
import json

role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['GET'])
def get_roles():
    """Get all roles with optional filtering and hierarchy"""
    parent_id = request.args.get('parent_id')
    level = request.args.get('level', type=int)
    is_active = request.args.get('is_active')
    include_hierarchy = request.args.get('include_hierarchy', 'false').lower() == 'true'
    
    query = Role.query
    
    if parent_id:
        query = query.filter(Role.parent_role_id == parent_id)
    elif parent_id == 'null':
        query = query.filter(Role.parent_role_id.is_(None))
    
    if level is not None:
        query = query.filter(Role.level == level)
    
    if is_active:
        query = query.filter(Role.is_active == (is_active.lower() == 'true'))
    
    roles = query.all()
    
    if include_hierarchy:
        # Build hierarchical structure
        role_dict = {role.id: role.to_dict() for role in roles}
        for role_data in role_dict.values():
            role_data['subroles'] = []
        
        for role in roles:
            if role.parent_role_id and role.parent_role_id in role_dict:
                role_dict[role.parent_role_id]['subroles'].append(role_dict[role.id])
        
        # Return only root roles (those without parents)
        root_roles = [role_data for role_data in role_dict.values() 
                     if not role_data['parent_role_id']]
        return jsonify(root_roles)
    
    return jsonify([role.to_dict() for role in roles])

@role_bp.route('/roles', methods=['POST'])
def create_role():
    """Create a new role"""
    data = request.json
    
    # Calculate level and path based on parent role
    level = 0
    path = f"/{data['name']}"
    
    if data.get('parent_role_id'):
        parent_role = Role.query.get(data['parent_role_id'])
        if not parent_role:
            return jsonify({'error': 'Parent role not found'}), 404
        
        level = parent_role.level + 1
        path = f"{parent_role.path}/{data['name']}"
    
    role = Role(
        name=data['name'],
        description=data.get('description'),
        parent_role_id=data.get('parent_role_id'),
        level=level,
        path=path,
        permissions=json.dumps(data.get('permissions', [])),
        max_subordinates=data.get('max_subordinates', 0),
        can_create_subroles=data.get('can_create_subroles', False),
        can_assign_roles=data.get('can_assign_roles', False),
        can_manage_projects=data.get('can_manage_projects', False),
        can_manage_budgets=data.get('can_manage_budgets', False),
        can_view_reports=data.get('can_view_reports', False),
        salary_range_min=data.get('salary_range_min'),
        salary_range_max=data.get('salary_range_max'),
        required_skills=json.dumps(data.get('required_skills', [])),
        created_by=data.get('created_by')
    )
    
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_dict()), 201

@role_bp.route('/roles/<role_id>', methods=['GET'])
def get_role(role_id):
    """Get a specific role by ID"""
    role = Role.query.get_or_404(role_id)
    role_data = role.to_dict()
    
    # Include subroles
    subroles = Role.query.filter_by(parent_role_id=role_id).all()
    role_data['subroles'] = [subrole.to_dict() for subrole in subroles]
    
    # Include assigned users
    user_roles = UserRole.query.filter_by(role_id=role_id, status='active').all()
    role_data['assigned_users'] = [ur.user.to_public_dict() for ur in user_roles]
    
    return jsonify(role_data)

@role_bp.route('/roles/<role_id>', methods=['PUT'])
def update_role(role_id):
    """Update a role"""
    role = Role.query.get_or_404(role_id)
    data = request.json
    
    # Update basic fields
    role.name = data.get('name', role.name)
    role.description = data.get('description', role.description)
    role.max_subordinates = data.get('max_subordinates', role.max_subordinates)
    role.can_create_subroles = data.get('can_create_subroles', role.can_create_subroles)
    role.can_assign_roles = data.get('can_assign_roles', role.can_assign_roles)
    role.can_manage_projects = data.get('can_manage_projects', role.can_manage_projects)
    role.can_manage_budgets = data.get('can_manage_budgets', role.can_manage_budgets)
    role.can_view_reports = data.get('can_view_reports', role.can_view_reports)
    role.salary_range_min = data.get('salary_range_min', role.salary_range_min)
    role.salary_range_max = data.get('salary_range_max', role.salary_range_max)
    role.is_active = data.get('is_active', role.is_active)
    
    if 'permissions' in data:
        role.permissions = json.dumps(data['permissions'])
    
    if 'required_skills' in data:
        role.required_skills = json.dumps(data['required_skills'])
    
    # Update path if name changed
    if 'name' in data and data['name'] != role.name:
        if role.parent_role_id:
            parent_role = Role.query.get(role.parent_role_id)
            role.path = f"{parent_role.path}/{data['name']}"
        else:
            role.path = f"/{data['name']}"
    
    role.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(role.to_dict())

@role_bp.route('/roles/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    """Delete a role (soft delete)"""
    role = Role.query.get_or_404(role_id)
    
    # Check if role has subroles
    subroles = Role.query.filter_by(parent_role_id=role_id).count()
    if subroles > 0:
        return jsonify({'error': 'Cannot delete role with subroles'}), 400
    
    # Check if role has active assignments
    active_assignments = UserRole.query.filter_by(role_id=role_id, status='active').count()
    if active_assignments > 0:
        return jsonify({'error': 'Cannot delete role with active assignments'}), 400
    
    role.is_active = False
    role.updated_at = datetime.utcnow()
    db.session.commit()
    return '', 204

@role_bp.route('/roles/<role_id>/hierarchy', methods=['GET'])
def get_role_hierarchy(role_id):
    """Get the complete hierarchy for a role (ancestors and descendants)"""
    role = Role.query.get_or_404(role_id)
    
    # Get ancestors
    ancestors = []
    current_role = role
    while current_role.parent_role_id:
        parent = Role.query.get(current_role.parent_role_id)
        ancestors.insert(0, parent.to_dict())
        current_role = parent
    
    # Get descendants (recursive)
    def get_descendants(parent_id):
        children = Role.query.filter_by(parent_role_id=parent_id).all()
        result = []
        for child in children:
            child_data = child.to_dict()
            child_data['subroles'] = get_descendants(child.id)
            result.append(child_data)
        return result
    
    descendants = get_descendants(role_id)
    
    return jsonify({
        'role': role.to_dict(),
        'ancestors': ancestors,
        'descendants': descendants
    })

# User Role Assignment endpoints

@role_bp.route('/user-roles', methods=['GET'])
def get_user_roles():
    """Get user role assignments with filtering"""
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')
    status = request.args.get('status')
    is_primary = request.args.get('is_primary')
    
    query = UserRole.query
    
    if user_id:
        query = query.filter(UserRole.user_id == user_id)
    
    if role_id:
        query = query.filter(UserRole.role_id == role_id)
    
    if status:
        query = query.filter(UserRole.status == status)
    
    if is_primary:
        query = query.filter(UserRole.is_primary == (is_primary.lower() == 'true'))
    
    user_roles = query.all()
    return jsonify([ur.to_dict() for ur in user_roles])

@role_bp.route('/user-roles', methods=['POST'])
def assign_role():
    """Assign a role to a user"""
    data = request.json
    
    # Check if assignment already exists
    existing = UserRole.query.filter_by(
        user_id=data['user_id'],
        role_id=data['role_id'],
        status='active'
    ).first()
    
    if existing:
        return jsonify({'error': 'User already has this role assigned'}), 400
    
    # If this is a primary role, unset other primary roles for this user
    if data.get('is_primary', False):
        UserRole.query.filter_by(
            user_id=data['user_id'],
            is_primary=True
        ).update({'is_primary': False})
    
    user_role = UserRole(
        user_id=data['user_id'],
        role_id=data['role_id'],
        assigned_by=data.get('assigned_by'),
        expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None,
        is_primary=data.get('is_primary', False),
        notes=data.get('notes'),
        approval_status=data.get('approval_status', 'approved')
    )
    
    db.session.add(user_role)
    db.session.commit()
    return jsonify(user_role.to_dict()), 201

@role_bp.route('/user-roles/<user_role_id>', methods=['PUT'])
def update_user_role(user_role_id):
    """Update a user role assignment"""
    user_role = UserRole.query.get_or_404(user_role_id)
    data = request.json
    
    # If setting as primary, unset other primary roles for this user
    if data.get('is_primary', False) and not user_role.is_primary:
        UserRole.query.filter_by(
            user_id=user_role.user_id,
            is_primary=True
        ).update({'is_primary': False})
    
    user_role.status = data.get('status', user_role.status)
    user_role.is_primary = data.get('is_primary', user_role.is_primary)
    user_role.notes = data.get('notes', user_role.notes)
    user_role.approval_status = data.get('approval_status', user_role.approval_status)
    
    if data.get('expires_at'):
        user_role.expires_at = datetime.fromisoformat(data['expires_at'])
    
    if data.get('approved_by'):
        user_role.approved_by = data['approved_by']
        user_role.approved_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(user_role.to_dict())

@role_bp.route('/user-roles/<user_role_id>', methods=['DELETE'])
def revoke_role(user_role_id):
    """Revoke a role assignment"""
    user_role = UserRole.query.get_or_404(user_role_id)
    user_role.status = 'expired'
    db.session.commit()
    return '', 204

@role_bp.route('/users/<user_id>/roles', methods=['GET'])
def get_user_roles_by_user(user_id):
    """Get all roles for a specific user"""
    user_roles = UserRole.query.filter_by(user_id=user_id, status='active').all()
    
    result = []
    for ur in user_roles:
        role_data = ur.role.to_dict()
        role_data['assignment'] = {
            'id': ur.id,
            'assigned_at': ur.assigned_at.isoformat() if ur.assigned_at else None,
            'expires_at': ur.expires_at.isoformat() if ur.expires_at else None,
            'is_primary': ur.is_primary,
            'notes': ur.notes
        }
        result.append(role_data)
    
    return jsonify(result)

@role_bp.route('/roles/<role_id>/users', methods=['GET'])
def get_role_users(role_id):
    """Get all users assigned to a specific role"""
    user_roles = UserRole.query.filter_by(role_id=role_id, status='active').all()
    
    result = []
    for ur in user_roles:
        user_data = ur.user.to_public_dict()
        user_data['assignment'] = {
            'id': ur.id,
            'assigned_at': ur.assigned_at.isoformat() if ur.assigned_at else None,
            'expires_at': ur.expires_at.isoformat() if ur.expires_at else None,
            'is_primary': ur.is_primary,
            'notes': ur.notes
        }
        result.append(user_data)
    
    return jsonify(result)


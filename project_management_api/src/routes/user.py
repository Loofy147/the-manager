from flask import Blueprint, jsonify, request
from src.models.user import User, db
from datetime import datetime
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    experience_level = request.args.get('experience_level', '')
    availability_status = request.args.get('availability_status', '')
    is_active = request.args.get('is_active', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search)) |
            (User.email.contains(search))
        )
    
    if experience_level:
        query = query.filter(User.experience_level == experience_level)
    
    if availability_status:
        query = query.filter(User.availability_status == availability_status)
    
    if is_active:
        query = query.filter(User.is_active == (is_active.lower() == 'true'))
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_public_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
        'per_page': per_page
    })

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        bio=data.get('bio'),
        skills=json.dumps(data.get('skills', [])),
        experience_level=data.get('experience_level', 'junior'),
        hourly_rate=data.get('hourly_rate'),
        availability_status=data.get('availability_status', 'available'),
        timezone=data.get('timezone', 'UTC'),
        language_preferences=json.dumps(data.get('language_preferences', ['en']))
    )
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # Check for unique constraints
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    # Update other fields
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    user.bio = data.get('bio', user.bio)
    user.experience_level = data.get('experience_level', user.experience_level)
    user.hourly_rate = data.get('hourly_rate', user.hourly_rate)
    user.availability_status = data.get('availability_status', user.availability_status)
    user.timezone = data.get('timezone', user.timezone)
    user.is_active = data.get('is_active', user.is_active)
    
    if 'skills' in data:
        user.skills = json.dumps(data['skills'])
    
    if 'language_preferences' in data:
        user.language_preferences = json.dumps(data['language_preferences'])
    
    if 'password' in data:
        user.set_password(data['password'])
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user (soft delete by setting is_active to False)"""
    user = User.query.get_or_404(user_id)
    user.is_active = False
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return '', 204

@user_bp.route('/users/<user_id>/login', methods=['POST'])
def update_last_login(user_id):
    """Update user's last login timestamp"""
    user = User.query.get_or_404(user_id)
    user.last_login = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Last login updated'})

@user_bp.route('/users/<user_id>/verify', methods=['POST'])
def verify_user(user_id):
    """Verify a user account"""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    if user.verification_token == data.get('token'):
        user.is_verified = True
        user.verification_token = None
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'User verified successfully'})
    else:
        return jsonify({'error': 'Invalid verification token'}), 400

@user_bp.route('/users/search', methods=['GET'])
def search_users():
    """Advanced user search"""
    query = request.args.get('q', '')
    skills = request.args.getlist('skills')
    experience_levels = request.args.getlist('experience_levels')
    availability_statuses = request.args.getlist('availability_statuses')
    min_hourly_rate = request.args.get('min_hourly_rate', type=float)
    max_hourly_rate = request.args.get('max_hourly_rate', type=float)
    
    user_query = User.query.filter(User.is_active == True)
    
    if query:
        user_query = user_query.filter(
            (User.username.contains(query)) |
            (User.first_name.contains(query)) |
            (User.last_name.contains(query)) |
            (User.bio.contains(query))
        )
    
    if skills:
        for skill in skills:
            user_query = user_query.filter(User.skills.contains(skill))
    
    if experience_levels:
        user_query = user_query.filter(User.experience_level.in_(experience_levels))
    
    if availability_statuses:
        user_query = user_query.filter(User.availability_status.in_(availability_statuses))
    
    if min_hourly_rate is not None:
        user_query = user_query.filter(User.hourly_rate >= min_hourly_rate)
    
    if max_hourly_rate is not None:
        user_query = user_query.filter(User.hourly_rate <= max_hourly_rate)
    
    users = user_query.all()
    return jsonify([user.to_public_dict() for user in users])

@user_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    
    user = User.query.filter(
        (User.username == username_or_email) | 
        (User.email == username_or_email)
    ).first()
    
    if user and user.check_password(password) and user.is_active:
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })
    else:
        return jsonify({'error': 'Invalid credentials or inactive account'}), 401

@user_bp.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.json
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        bio=data.get('bio'),
        skills=json.dumps(data.get('skills', [])),
        experience_level=data.get('experience_level', 'junior'),
        timezone=data.get('timezone', 'UTC'),
        language_preferences=json.dumps(data.get('language_preferences', ['en']))
    )
    
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Registration successful',
        'user': user.to_public_dict()
    }), 201


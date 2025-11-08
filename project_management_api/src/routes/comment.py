from flask import Blueprint, request, jsonify
from src.models.comment import Comment
from src.models.project import Task
from src.models.user import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/tasks/<string:task_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(task_id):
    data = request.get_json()
    content = data.get('content')
    user_id = get_jwt_identity()

    if not content:
        return jsonify({'message': 'Content is required'}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201

@comment_bp.route('/tasks/<string:task_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify([comment.to_dict() for comment in task.comments]), 200

@comment_bp.route('/comments/<string:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    content = data.get('content')
    user_id = get_jwt_identity()

    if not content:
        return jsonify({'message': 'Content is required'}), 400

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    if comment.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    comment.content = content
    db.session.commit()

    return jsonify(comment.to_dict()), 200

@comment_bp.route('/comments/<string:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    if comment.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted'}), 200

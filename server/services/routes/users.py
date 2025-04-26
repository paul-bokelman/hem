from flask import Blueprint, jsonify, abort
import uuid
from db.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by their ID."""
    try:
        u = User.get(User.id == uuid.UUID(user_id))
    except Exception:
        abort(404)
    return jsonify({'id': str(u.id)})

@users_bp.route('/users', methods=['POST'])
def create_user():
    u = User.create(id=uuid.uuid4())
    return jsonify({'id': str(u.id)}), 201

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        u = User.get(User.id == uuid.UUID(user_id))
    except Exception:
        abort(404)
    u.delete_instance(recursive=True)
    return '', 204

@users_bp.route('/users/<user_id>/macros', methods=['GET'])
def get_user_macros(user_id):
    try:
        u = User.get(User.id == uuid.UUID(user_id))
    except Exception:
        abort(404)
    macros = []
    for m in u.macros:
        actions = [{'id': ma.action.id, 'name': ma.action.name} for ma in m.required_actions]
        macros.append({
            'id': m.id,
            'name': m.name,
            'prompt': m.prompt,
            'allow_other_actions': m.allow_other_actions,
            'required_actions': actions
        })
    return jsonify(macros)
from flask import Blueprint, jsonify, abort, request
from db.models import Action
from services.middleware import admin_required

actions_bp = Blueprint('actions', __name__)

@actions_bp.route('/actions', methods=['GET'])
def list_actions():
    actions = [{'id': a.id, 'name': a.name, 'description': a.description} for a in Action.select()]
    return jsonify(actions)

@actions_bp.route('/actions', methods=['POST'])
@admin_required
def create_action():
    data = request.get_json() or {}
    a = Action.create(name=data.get('name'), description=data.get('description', ''))
    return jsonify({'id': a.id, 'name': a.name}), 201

@actions_bp.route('/actions/<int:action_id>', methods=['PUT'])
@admin_required
def edit_action(action_id):
    a = Action.get_or_none(Action.id == action_id)
    if not a:
        abort(404)
    data = request.get_json() or {}
    a.name = data.get('name', a.name)
    a.description = data.get('description', a.description)
    a.save()
    return jsonify({'id': a.id, 'name': a.name})

@actions_bp.route('/actions/<int:action_id>', methods=['DELETE'])
@admin_required
def delete_action(action_id):
    a = Action.get_or_none(Action.id == action_id)
    
    if not a:
        abort(404)

    a.delete_instance()
    return '', 204
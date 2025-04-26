from flask import Blueprint, jsonify, abort, request
from db.models import Macro, MacroAction, Action
from services.utils import get_user_from_header

macros_bp = Blueprint('macros', __name__)

@macros_bp.route('/macros', methods=['POST'])
def create_macro():
    user = get_user_from_header()
    data = request.get_json() or {}
    m = Macro.create(
        user=user,
        name=data.get('name'),
        prompt=data.get('prompt'),
        allow_other_actions=data.get('allow_other_actions', False)
    )
    req_ids = data.get('required_actions', [])
    for aid in req_ids:
        act = Action.get_or_none(Action.id == aid)

        if not act:
            continue

        MacroAction.create(macro=m, action=act)
    return jsonify({'id': m.id, 'name': m.name}), 201

@macros_bp.route('/macros/<string:macro_id>', methods=['PUT'])
def edit_macro(macro_id):
    user = get_user_from_header()
    m = Macro.get_or_none(Macro.id == macro_id)

    if not m:
        abort(404)

    if m.user != user:
        abort(403)

    data = request.get_json() or {}
    m.name = data.get('name', m.name)
    m.prompt = data.get('prompt', m.prompt)
    m.allow_other_actions = data.get('allow_other_actions', m.allow_other_actions)
    m.save()
    if 'required_actions' in data:
        MacroAction.delete().where(MacroAction.macro == m).execute()
        for aid in data['required_actions']:
            act = Action.get_or_none(Action.id == aid)

            if not act:
                continue

            MacroAction.create(macro=m, action=act)
    return jsonify({'id': m.id, 'name': m.name})

@macros_bp.route('/macros/<string:macro_id>', methods=['DELETE'])
def delete_macro(macro_id):
    user = get_user_from_header()
    m = Macro.get_or_none(Macro.id == macro_id)
    
    if not m:
        abort(404)
        
    if m.user != user:
        abort(403)
    m.delete_instance(recursive=True)
    return '', 204
from flask import request, abort
import uuid
from db.models import User

def get_user_from_header():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        abort(401, 'Missing X-User-ID')
    try:
        user = User.get(User.id == uuid.UUID(user_id))
    except Exception:
        abort(401, 'Invalid User ID')
    return user
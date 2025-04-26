from flask import request, abort
import os
from functools import wraps

def admin_required(f):
    """Decorator middleware to check if the request has a valid admin key."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-Admin-Key')
        if key != os.getenv('ADMIN_API_KEY'):
            abort(403, 'Admin key required')
        return f(*args, **kwargs)
    return decorated_function
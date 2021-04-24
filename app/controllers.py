from flask import session, redirect, jsonify
from werkzeug.security import safe_str_cmp
from functools import wraps

from app import app
from app.mod_user.models import User

def is_admin(id):
    user = User.lookup_id(id)

    return user.admin

def get_field(orig):
    return str(orig).split('for key')[-1].replace("'", "").replace('"', '').replace(' ', '').replace(')', '')

def assign(source, target):
    for key in source:
        try:
            t = type(getattr(target, key))
            if type(source[key]) == t:
                setattr(target, key, source[key])
        except Exception:
            pass

    return target

def mime(file):
    matches = list(filter(lambda h: h[0] == 'Content-Type', file.headers))
    
    if len(matches) > 0:
        return matches[0][1]
    else:
        return '*'

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return jsonify({'error': 'You are unauthorized to access this resource. Please log in'}), 200

        return f(*args, **kwargs)

    return decorated_function

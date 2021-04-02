from flask import Blueprint, request, jsonify, make_response, session

from app import app
from app.controllers import get_field, assign, session_required
from app.mod_user.models import User

mod_user = Blueprint('user', __name__, url_prefix='/user')

def gen_session(user, sess):
    sess['user_id'] = user.id
    sess['username'] = user.username
    sess['password'] = user.password
    sess['avatar'] = user.avatar
    sess['admin'] = user.admin

    return sess, {
        'auth_success': True,
        'user_id': user.id,
        'instructor': user.instructor,
        'admin': user.admin
    }


@mod_user.route('/auth', methods=['POST'])
def auth():
    form = request.json
    res = {}

    try:
        identifier = form['identifier']
        password = form['password']
        user = User.lookup(identifier)

        if user and user.password == password:
            global session
            session, res = gen_session(user, session)
        else:
            res = {'error': 'Incorrect credentials'}
    except Exception as e:
        print(e)
        res = {'error': 'There was an error logging you in'}

    return jsonify(res), 200

@mod_user.route('/deauth', methods=['POST'])
@session_required
def deauth():
    session.clear()
    return jsonify({}), 200


@mod_user.route('/', methods=['GET'])
@session_required
def get():
    try:
        id = int(request.args.get('id'))
        user = User.lookup_id(id)
        res = {}

        if user:
            user = user.as_dict()

            if session['user_id'] != user['id']:
                del user['email']
                del user['password']

            res = {'data': user}

    except Exception as e:
        print(e)
        res = {'error': 'There was an error finding this user'}

    return jsonify(res), 200

@mod_user.route('/', methods=['POST'])
@session_required
def post():
    form = request.json
    res = {}

    try:
        user = User(
            email=form['email'],
            username=form['username'],
            first_name=form['first_name'],
            last_name=form['last_name'],
            password=form['password'],
            instructor=form['instructor'],
            admin=False
        )
        user.save()

        global session
        session, res = gen_session(user, session)
    except Exception as e:
        try:
            res = {'error': 'Please choose a unique ' + get_field(e.orig)}
        except Exception:
            res = {'error': 'There was an error creating your account'}

    out = jsonify(res)

    '''
    if res['auth_success']:

        out.set_cookie('sid', session.sid)
    '''

    return out, 200

@mod_user.route('/', methods=['PATCH'])
@session_required
def patch():
    user = User.lookup_id(request.args.get('id'))
    form = request.json
    res = {}
    status = 200

    if user:
        user = assign(form, user)

        try:
            user.save()
            res = {'data': user.as_dict()}
            print(res)
        except Exception:
            status = 500
            res = {'error': 'There was an error validating your account'}
        else:
            status = 404

        return jsonify(res), status

@mod_user.route('/', methods=['DELETE'])
@session_required
def delete():
    user = User.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    if user:
        try:
            user.delete()
            res = {'data': user}
        except Exception:
            res = {'error': 'Error deleting user'}
            status = 500

    return jsonify(res), status

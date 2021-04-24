from flask import Blueprint, request, jsonify, make_response, session
from werkzeug.utils import secure_filename
import os

from app import app
from app.controllers import get_field, assign, session_required, mime
from app.mod_user.models import User

mod_user = Blueprint('user', __name__, url_prefix='/user')

def gen_session(user, sess={}):
    sess['user_id'] = user.id
    sess['admin'] = user.admin

    return sess, {
        'auth_success': True,
        'user_id': user.id,
        'instructor': user.instructor,
        'admin': user.admin,
        'avatar': user.avatar
    }

@mod_user.route('/auth', methods=['POST'])
def auth():
    form = request.json
    if form is None:
        form = {}

    res = {}

    try:
        identifier = form.get('identifier')
        password = form.get('password')
        user = User.lookup(identifier)

        if user and user.password == password:
            global session
            session, res = gen_session(user, session)
        else:
            res = {'error': 'Incorrect credentials'}
    except Exception as e:
        res = {'error': 'There was an error logging you in' + str(e)}

    out = jsonify(res)

    return out, 200

@mod_user.route('/deauth', methods=['POST'])
@session_required
def deauth():
    session.clear()
    return jsonify({'deauth_success': True}), 200


@mod_user.route('/', methods=['GET'])
@session_required
def get():
    try:
        id = int(request.args.get('id'))
        user = User.lookup_id(id)
        res = {}

        if user:
            user = user.as_dict()

            if session.get('user_id') != id:
                del user['email']
                del user['password']

            res = {'data': user}

    except Exception as e:
        res = {'error': 'There was an error finding this user'}

    return jsonify(res), 200

@mod_user.route('/', methods=['POST'])
def post():
    form = request.json
    res = {}

    try:
        user = User(
            email=form.get('email'),
            username=form.get('username'),
            first_name=form.get('first_name'),
            last_name=form.get('last_name'),
            password=form.get('password'),
            instructor=form.get('instructor'),
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

    return jsonify(res), 200

@mod_user.route('/', methods=['PATCH'])
@session_required
def patch():
    user = User.lookup_id(request.args.get('id'))
    form = request.json
    res = {}

    if user:
        del form['avatar']
        user = assign(form, user)

        try:
            user.update()
            res = {'data': user.as_dict()}
        except Exception:
            res = {'error': 'There was an error updating your account'}

    return jsonify(res), 200

@mod_user.route('/files', methods=['PATCH'])
@session_required
def patch_files():
    res = {}

    try:
        id = request.args.get('id')
        current_id = str(session['user_id'])

        file = request.files['files[0]']
        file_type = mime(file).split('/')[0]

        if file_type == 'image' and current_id == id:
            user = User.lookup_id(id)

            filename = secure_filename(file.filename)
            parts = filename.split('.')
            filename = '.'.join(parts[:-1]) + str(current_id) + '.' + parts[-1]

            destination = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars/' + filename)
            file.save(destination)

            old_avatar = user.avatar
            user.avatar = filename
            user.update()

            try:
                if old_avatar != 'default.png':
                    target = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars/' + old_avatar)
                    os.remove(target)
            except Exception:
                pass

            res = {'upload_success': True}
        elif current_id == id:
            res = {'upload_success': False, 'error': 'Invalid file type'}
        else:
            res = {'upload_success': False, 'error': "You do not have permission to change this user's avatar"}

    except Exception:
        res = {'upload_success': False, 'error': 'There was an error uploading your file'}

    return res, 200

@mod_user.route('/', methods=['DELETE'])
@session_required
def delete():
    id = request.args.get('id')
    user = User.lookup_id(id)
    res = {}
    status = 200

    if user and id == str(session['user_id']):
        try:
            user.delete()
            res = {'data': user}
        except Exception:
            res = {'error': 'Error deleting user'}
            status = 500

    return jsonify(res), status

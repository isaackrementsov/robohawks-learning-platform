from flask import Blueprint, request, jsonify

from app.controllers import get_field, assign
from app.mod_user.models import User


mod_user = Blueprint('user', __name__, url_prefix='/user')


@mod_user.route('/login', methods=['POST'])
def login():
    form = request.json
    user = User.lookup(form['emailOrUsername'])
    res = {}

    if user and user.password == form['password']:
        res = {'data': user}

    return jsonify(res), 200


@mod_user.route('/list', methods=['GET'])
def list():
    res = {}
    status = 200

    try:
        users = User.list(request.args)
        res = {'data': users}
    except Exception as e:
        res = {'error': 'Invalid list filters'}
        status = 400

    return jsonify(res), 200


@mod_user.route('/', methods=['GET'])
def get():
    user = User.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    if user:
        res = {'data': user}
    else:
        status = 404

    return jsonify(res), status


@mod_user.route('/', methods=['POST'])
def post():
    form = request.json
    res = {}

    user = User(
        email=form['email'],
        username=form['username'],
        first_name=form['first_name'],
        last_name=form['last_name'],
        password=form['password'],
        admin=form['admin']
    )

    try:
        user.save()
        res = {'data': user}
    except Exception as e:
        res = {'error': 'Please choose a unique' + get_field(e)}

    return jsonify(res), 200


@mod_user.route('/', methods=['PATCH'])
def patch():
    user = User.lookup_id(request.args.get('id'))
    form = request.json
    res = {}
    status = 200

    if user:
        user = assign(form, user)

        try:
            user.save()
            res = {'data': user}
        except Exception:
            status = 500
            res = {'error': 'There was an error validating your account'}
        else:
            status = 404

        return jsonify(res), status


@mod_user.route('/', methods=['DELETE'])
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

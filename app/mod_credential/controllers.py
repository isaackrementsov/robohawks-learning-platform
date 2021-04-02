from flask import Blueprint, request, jsonify

from app.controllers import assign
from app.mod_credential.models import Credential, UserCredential, CourseCredential, Prerequisite


mod_credential = Blueprint('credential', __name__, url_prefix='/credential')


@mod_credential.route('/', methods=['GET'])
def get():
    credential = Credential.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    if credential:
        res = {'data': credential}
    else:
        status = 404

    return jsonify(res), status


@mod_credential.route('/', methods=['POST'])
def post():
    form = request.json
    res = {}
    status = 200

    credential = Credential(
        name=form['name'],
        icon=form['icon'],
        description=form['description'],
        micro=form['micro'],
        sequence=form['sequence'],
        course_id=form['course_id']
    )

    try:
        credential.save()
        res = {'data': credential}
    except Exception:
        status = 500
        res = {'error': 'There was an error saving the credential'}

    return jsonify(res), status


@mod_credential.route('/', methods=['PATCH'])
def patch():
    credential = Credential.lookup_id(request.args.get('id'))
    form = request.json
    res = {}
    status = 200

    if credential:
        credential = assign(form, credential)

        try:
            credential.save()
            res = {'data': credential}
        except Exception:
            status = 500
            res = {'error': 'There was an error saving credential'}
    else:
        status = 404

    return jsonify(res), status


@mod_credential.route('/', methods=['DELETE'])
def delete():
    credential = Credential.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    # Make sure no students have this credntial
    if credential and credential.recipients.length == 0:
        try:
            credential.delete()
            res = {'data': credential}
        except Exception:
            status = 500
            res = {'error': 'There was an error deleting the credential'}
    else:
        # No special error message is needed for recipients.length > 0, since this should be validated on the frontend anyway
        status = 404

    return jsonify(res), status



@mod_credential.route('/search', methods=['GET'])
def get_search():
    credentials = Credential.list(request.args.get('keyword'))
    res = {'data': credentials}
    status = 200

    return jsonify(res), status

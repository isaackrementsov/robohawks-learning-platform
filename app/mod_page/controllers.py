from flask import Blueprint, request, jsonify

from app.controllers import assign
from app.mod_page.models import Page


mod_page = Blueprint('page', __name__, url_prefix='/page')


@mod_page.route('/', methods=['GET'])
def get():
    page = Page.lookup(request.args.get('id'))
    res = {}
    status = 200

    if page:
        form = request.json
        res = {'data': page}
    else:
        status = 404

    return res, status


@mod_page.route('/', methods=['POST'])
def post():
    form = request.json
    res = {}
    status = 200

    page = Page(
        course_id=form['course_id'],
        unit_id=form['unit_id'],
        name=form['name'],
        text_content=form['text_content'],
        sequence=form['sequence']
    )

    try:
        page.save()
        res = {'data': page}
    except Exception as e:
        res = {'error': 'There was an error saving the page'}
        status = 500

    return jsonify(res), status


@mod_page.route('/', methods=['PATCH'])
def patch():
    page = Page.lookup(request.args.get('id'))
    form = request.json
    res = {}
    status = 200

    if page:
        page = assign(form, page)

        try:
            page.save()
            res = {'data': page}
        except Exception:
            status = 500
            res = {'error': 'There was an error validating your account'}
    else:
        status = 404

    return jsonify(res), status


@mod_page.route('/', methods=['DELETE'])
def delete():
    page = Page.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    if page:
        try:
            page.delete()
            res = {'data': page}
        except Exception:
            status = 500
            res = {'error': 'There was an error deleting the page'}
    else:
        status = 404

    return jsonify(res), status



@mod_page.route('/resource', methods=['POST'])
def post_resource():
    form = request.json
    res = {}
    status = 200

    try:
        res = {}
    except Exception:
        status = 500
        res = {'error': 'There was an error saving the resource'}

    return jsonify(res), status


@mod_page.route('/resource', methods=['PATCH'])
def patch_resource():
    resource = PageResource.lookup_id(request.args.get('id'))
    form = request.json
    res = {}
    status = 200

    if resource:
        page = assign(form, resource)

        try:
            page.save()
            res = {'data': page}
        except Exception:
            status = 500
            res = {'error': 'There was an error updating the resource'}
    else:
        status = 404

    return jsonify(res), status


@mod_page.route('/resource', methods=['DELETE'])
def delete_resource():
    resource = PageResource.lookup_id(request.args.get('id'))
    res = {}
    status = 200

    if resource:
        try:
            resource.delete()
            res = {'data': resource}
        except Exception:
            status = 500
            res = {'error': 'There was an error deleting the resource'}
    else:
        status = 404

    return jsonify(res), status

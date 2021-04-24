from flask import Blueprint, request, jsonify

from app.mod_course.models import Course, UserCourse, CourseRequest

mod_course = Blueprint('course', __name__, url_prefix='/course')

@mod_course.route('/all', methods=['GET'])
def get_all():
    res = {}

    try:
        courses = Course.list(request.args)
        res = {'data': courses}
    except Exception:
        res = {'error': 'There was an error finding courses'}

    return jsonify(res), 200

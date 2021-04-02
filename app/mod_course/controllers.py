from flask import Blueprint, request, jsonify

from app.mod_course.models import Course, UserCourse, CourseRequest

mod_course = Blueprint('course', __name__, url_prefix='/course')

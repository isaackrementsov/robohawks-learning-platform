from flask import Blueprint, request, jsonify

from app.controllers import assign
from app.mod_credential.models import Credential, Prerequisite


mod_course = Blueprint('course', __name__, url_prefix='/course')

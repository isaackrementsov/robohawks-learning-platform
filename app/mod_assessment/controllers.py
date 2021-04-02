from flask import Blueprint

from app.mod_assessment.models import Assessment, Question, Option, Response, ResponseOption 

mod_assessment = Blueprint('assessment', __name__, url_prefix='/assessment')

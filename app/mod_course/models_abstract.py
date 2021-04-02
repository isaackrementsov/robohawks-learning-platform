from app import db
from app.models import Base


class CourseModule:

    name = db.Column(db.String(128), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)

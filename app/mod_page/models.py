from app import db
from sqlalchemy.orm import relationship
from app.models import Base
from app.mod_course.models_abstract import CourseModule


class Page(CourseModule, Base):

    __tablename__ = 'page'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    link = db.Column(db.String(192), nullable=False)
    name = db.Column(db.String(128), nullable=False)

    # TODO: change this to self.resources or move to PageResource class?
    def next_sequence(self):
        return PageResource.query(db.func.max(PageResource.sequence)).filter_by(PageResource.page_id==self.id)

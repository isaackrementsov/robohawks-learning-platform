from app import db
from sqlalchemy.orm import relationship
from app.models import Base



class Page(CourseModule):


    __tablename__ = 'page'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    unit_id = db.Column(db.Integer, ForeignKey('unit.id'))

    resources = relationship('PageResource')


    # TODO: change this to self.resources or move to PageResource class?
    def next_sequence(self):
        return PageResource.query(db.func.max(PageResource.sequence)).filter_by(PageResource.page_id=self.id)



class PageResource(Base):


    __tablename__ = 'page_resource'

    link = db.Column(db.String(256), nullable=True)
    file = db.Column(db.String(192), nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

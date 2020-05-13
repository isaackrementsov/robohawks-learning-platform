from app import db
from sqlalchemy.orm import relationship
from app.mod_assessment.models import Assessment
from app.mod_page.models import Page
from app.models import Base



class Course(Base):


    __tablename__ = 'course'

    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    users = relationship('User', secondary='user_course')
    user_requests = relationship('User', secondary='course_request')
    prerequisites = relationship('Credential', secondary='prerequisite')
    credentials = relationship('Credential')
    assessments = relationship('Assessment')
    pages = relationship('Page')
    chats = relationship('SupportChat')


    # TODO: change this to use self.assessments and self.pages
    def next_sequence(self):
    	max_assessment = Assessment.query(db.func.max(Assessment.sequence)).filter_by(Assessment.course_id=self.id)
    	max_page = Page.query(db.func.max(Page.sequence)).filter_by(Page.course_id=self.id)

    	return max(max_assessment, max_page) + 1



class UserCourse(Base):


    __tablename__ = 'user_course'

    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    progress = db.Column(db.Integer, nullable=True, default=0)



class CourseRequest(Base):


    __tablename__ = 'course_request'

    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))



class CourseModule(Base):


    __abstract__ = True

    course_id = db.Column(db.Integer, ForeignKey('course.id'))

    name = db.Column(db.String(128), nullable=False)
    text_content = db.Column(db.Text, nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

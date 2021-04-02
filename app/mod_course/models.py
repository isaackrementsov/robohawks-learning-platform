from app import db
from sqlalchemy.orm import relationship
from app.mod_user.models import User
from app.mod_assessment.models import Assessment
from app.mod_page.models import Page
from app.mod_credential.models import Credential
from app.models import Base



class Course(Base):


    __tablename__ = 'course'

    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    users = relationship('User', secondary='user_course')
    requests = relationship('CourseRequest')
    prerequisites = relationship('Credential', secondary='prerequisite')
    assessments = relationship('Assessment')
    pages = relationship('Page')


    # TODO: change this to use self.assessments and self.pages
    def next_sequence(self):
    	max_assessment = Assessment.query(db.func.max(Assessment.sequence)).filter_by(Assessment.course_id==self.id)
    	max_page = Page.query(db.func.max(Page.sequence)).filter_by(Page.course_id==self.id)

    	return max(max_assessment, max_page) + 1


    def register_user(self, id):
        user_course = UserCourse(course_id=self.id, user_id=id, progress=0)
        user_course.save()


class UserCourse(Base):


    __tablename__ = 'user_course'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # -1 for instructors
    progress = db.Column(db.Integer, nullable=True, default=-1)


    # TODO: Test whether appending is necessary in a join table
    def save(self):
        course = Course.lookup_id(self.course_id)
        user = Course.lookup_id(self.user_id)

        course.users.append(user)
        user.courses.append(course)

        Base.save(self)


class CourseRequest(Base):


    __tablename__ = 'course_request'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def accept(self):
        course = Course.lookup_id(self.course_id)
        course.register_user(self.user_id)

        self.delete()


    def deny(self):
        # TODO: Possibly let denied user know, list reason
        self.delete()


    def save(self, warned):
        credentials = User.lookup_id(self.user_id)
        prerequisites = Course.lookup_id(self.course_id).prerequisites

        conflict = None
        if not warned:

            for prerequisite in prerequisites:
                matched = [c for c in credentials if c.id == prerequisite.credential_id]

                if matched.length == 0:
                    conflict = prerequisite.id
                    break

        if conflict:
            return "Missing prerequisite: " + Credential.lookup_id(conflict).name
        else:
            Base.save(self)

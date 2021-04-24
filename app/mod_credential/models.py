from app import db
from sqlalchemy.orm import relationship
from app.models import Base
from app.mod_course.models_abstract import CourseModule


class Credential(Base):

    __tablename__ = 'credential'

    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    micro = db.Column(db.Boolean, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)

    #credentials = relationship('CourseCredential')
    users = relationship('User', secondary='user_credential')
    required_for = relationship('Course', secondary='prerequisite')

    @staticmethod
    def list_user(user_id):
        Credential.query.filter(Credential.users.any(id=user_id)).all()


class UserCredential(Base):


    __tablename__ = 'user_credential'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    credential_id = db.Column(db.Integer, db.ForeignKey('credential.id'))


class CourseCredential(CourseModule, Base):

    __tablename__ = 'course_credential'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    credential_id = db.Column(db.Integer, db.ForeignKey('credential.id'))


class Prerequisite(Base):


    __tablename__ = 'prerequisite'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    credential_id = db.Column(db.Integer, db.ForeignKey('credential.id'))

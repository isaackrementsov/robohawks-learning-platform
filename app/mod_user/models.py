from app import db
from sqlalchemy.orm import relationship
from app.models import Base


class User(Base):


    DEFAULT_AVATAR = 'default.png'

    __tablename__ = 'user'

    email = db.Column(db.String(128), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.String(192), nullable=False)
    last_name = db.Column(db.String(192), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    avatar = db.Column(db.String(256), nullable=False, default=DEFAULT_AVATAR)

    admin = db.Column(db.Boolean, nullable=False, default=False)
    instructor = db.Column(db.Boolean, nullable=False, default=False)

    courses = relationship('Course', secondary='user_course')
    course_requests = relationship('CourseRequest')
    credentials = relationship('Credential', secondary='user_credential')
    responses = relationship('Response')


    @staticmethod
    def lookup(identifier):
        return User.query.filter(db.or_(User.username == identifier, User.email == identifier)).first()

    @staticmethod
    def matches_id(id):
        return User.query.get(id) is not None

    @staticmethod
    def lookup_id(id):
        return Base.lookup_id(User, id)

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
    instructor = db.Column(db.Boolean, nullable=False)

    courses = relationship('Course', secondary='user_course')
    course_requests = relationship('Course', secondary='course_request')
    credentials = relationship('Credential', secondary='user_credential')
    chats = relationship('SupportChat')
    messages_sent = relationship('SupportMessage')
    response = relationship('AssessmentResponse')


    @staticmethod
    def lookup(identifier):
        return User.query.filter(db.or_(User.username == identifier, User.email == identifier)).first()


    @staticmethod
    def matches_id(id):
        return User.query.get(id) is not None


    @staticmethod
    def list(criteria):
        query = []

        for key in criteria:
            query.append(criteria[key] == User.__dict__[key])

        return User.query.filter(db.and_(*query)).all()



class SupportChat(Base):


    __tablename__ = 'support_chat'

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    messages = relationship('SupportMessage')


class SupportMessage(Base):


    __tablename__ = 'support_message'

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))

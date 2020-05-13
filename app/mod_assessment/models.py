from app import db
from sqlalchemy.orm import relationship
from app.mod_course.models import CourseModule
from app.models import Base



class Assessment(CourseModule):


    __tablename__ = 'assessment'

    questions = relationship('AssessmentQuestion')


    # TODO: change this to self.questions
    def next_sequence(self):
        return AssessmentQuestion.query(db.func.max(AssessmentQuestion.sequence)).filter_by(AssessmentQuestion.assessment_id=self.id)



class AssessmentQuestion(Base):


    __tablename__ = 'assessment_question'

    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))

    text_content = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(192), nullable=True)
    type = db.Column(db.String(128), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)

    answers = relationship('AssessmentAnswer')
    responses = relationship('AssessmentResponse')



class AssessmentEntry(Base):


    __abstract__ = True

    letter = db.Column(db.Char, nullable=True)
    correct = db.Column(db.Boolean, nullable=True)
    text = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(192), nullable=True)

    question_id = db.Column(db.Integer, db.ForeignKey('assessment_question.id'))



class AssessmentAnswer(AssessmentEntry):


    __tablename__ = 'assessment_answer'

    strict = db.Column(db.Boolean, nullable=True)
    sequence = db.Column(db.Integer, nullable=False)



class AssessmentResponse(AssessmentEntry):


    __tablename__ = 'assessment_response'

    score = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

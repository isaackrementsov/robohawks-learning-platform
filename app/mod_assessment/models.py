from app import db
from sqlalchemy.orm import relationship
from app.mod_course.models_abstract import CourseModule
from app.models import Base



class Assessment(Base):

    __tablename__ = 'assessment'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    name = db.Column(db.String(128), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    questions = relationship('Question')

    # TODO: change this to self.questions
    def next_sequence(self):
        return AssessmentQuestion.query(db.func.max(Question.sequence)).filter_by(Question.assessment_id==self.id)



class Question(Base):

    __tablename__ = 'question'

    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))

    text_content = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(192), nullable=True)
    type = db.Column(db.String(128), nullable=False)
    score_total = db.Column(db.Integer, nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

    options = relationship('Option')
    responses = relationship('Response')


class Option(Base):

    __tablename__ = 'option'

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    manual = db.Column(db.Boolean, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

    correct = db.Column(db.Boolean, nullable=True)
    file = db.Column(db.String(192), nullable=True)
    text_content = db.Column(db.Text, nullable=True)

    responses = relationship('Response', secondary='response_option')

    def lookup(question_id):
        return Option.query.filter(Option.question_id == question_id)


class Response(Base):

    __tablename__ = 'response'

    score = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    correct = db.Column(db.Boolean, nullable=True)
    file = db.Column(db.String(192), nullable=True)
    text_content = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    options = relationship('Option', secondary='response_option')

    def grade(self, score, feedback=None):
        if not self.question.strict:
            self.feedback = feedback
            self.score = score
            self.save()

    def auto_grade(self):
        if self.question.strict:
            correct = False
            answers = AssessmentAnswer.lookup(self.question_id)

            if self.type == 'multiple_choice':
                for answer in answers:
                    if self.question.all_required:
                        if self.letter == answer.letter and not answer.correct:
                            break
                    else:
                        if self.letter == answer.letter and answer.correct:
                            correct = True
                            break

            elif self.type == 'short_answer':
                for answer in answers:
                    if self.text == answer.text and answer.correct:
                        correct = True
                        break

            self.correct = correct
            self.save()


class ResponseOption(Base):

    __tablename__ = 'response_option'

    response_id = db.Column(db.Integer, db.ForeignKey('response.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))

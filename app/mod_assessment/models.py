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
    score_total = db.Column(db.Integer, nullable=True)
    sequence = db.Column(db.Integer, nullable=False)
    all_required = db.Column(db.Boolean, nullable=False, default=False)

    answers = relationship('AssessmentAnswer')
    responses = relationship('AssessmentResponse', back_populates='question')



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


    def lookup(question_id):
        return AssessmentAnswer.query.filter(AssessmentAnswer.question_id == question_id)


class AssessmentResponse(AssessmentEntry):


    __tablename__ = 'assessment_response'

    score = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = relationship('AssessmentQuestion', back_populates='responses')


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

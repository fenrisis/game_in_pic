from app import db
from sqlalchemy.orm import relationship

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    questions = relationship('Question', backref='quiz')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    image = db.Column(db.String(100))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    answers = relationship('Answer', backref='question')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    results = relationship('Result', backref='user')

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)


if __name__ == '__main__':
    db.create_all()
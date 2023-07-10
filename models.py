from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(120), nullable=False)
    number_of_questions = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    required_score_to_pass = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(6), nullable=False)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = 'Quizzes'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answers.all()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

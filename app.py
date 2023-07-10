from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Quiz, Question, Answer
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # Replace with your database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'adwefadad'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


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


admin = Admin(app)

# Create all database tables
with app.app_context():
    db.create_all()

# Register models with Flask-Admin
admin.add_view(ModelView(Quiz, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Answer, db.session))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz-data', methods=['POST'])
def quiz_data():
    # Fetch quiz data from the database
    quiz_data = []
    quizzes = Quiz.query.all()
    for quiz in quizzes:
        questions = []
        for question in quiz.questions:
            options = []
            for answer in question.answers:
                options.append({
                    'id': answer.id,
                    'text': answer.text,
                })
            questions.append({
                'id': question.id,
                'text': question.text,
                'image': question.image,
                'options': options,
            })
        quiz_data.append({
            'id': quiz.id,
            'name': quiz.name,
            'topic': quiz.topic,
            'number_of_questions': quiz.number_of_questions,
            'time': quiz.time,
            'required_score_to_pass': quiz.required_score_to_pass,
            'difficulty': quiz.difficulty,
            'questions': questions,
        })
    
    return jsonify({'data': quiz_data})

@app.route('/quiz/<quiz_id>/add-question', methods=['POST'])
def add_question(quiz_id):
    text = request.form['text']
    image = request.form['image']
    quiz = Quiz.query.get(quiz_id)

    # Create a new question object and associate it with the quiz
    question = Question(text=text, image=image, quiz=quiz)
    db.session.add(question)
    db.session.commit()

    return redirect(url_for('quiz'))  # Redirect back to the quiz page


@app.route('/quiz-results', methods=['POST'])
def quiz_results():
    # Process the submitted quiz and calculate results
    data = request.json
    # Process the data and calculate the results

    # Replace this with your actual calculation logic
    score = 75  # Example score

    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your-secret-key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    results = db.relationship('Result', backref='user')

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    questions = db.relationship('Question', backref='quiz')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    image = db.Column(db.String(100))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    answers = db.relationship('Answer', backref='question')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    quizzes = Quiz.query.all()
    return render_template('home.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    if request.method == 'POST':
        # Logic to calculate score and result
        return redirect(url_for('result', result_id=result.id))
    else:
        # Logic to fetch and display quiz questions
        quiz = Quiz.query.get(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        return render_template('quiz.html', quiz=quiz, questions=questions)

@app.route('/result/<int:result_id>')
@login_required
def result(result_id):
    result = Result.query.get(result_id)
    return render_template('result.html', result=result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

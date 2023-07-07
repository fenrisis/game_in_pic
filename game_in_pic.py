from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
db = SQLAlchemy(app)

class GameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(100))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        game_data = GameData.query.first()
        correct_answer = game_data.correct_answer
        if user_input.lower() == correct_answer.lower():
            result = 'Correct'
        else:
            result = 'Incorrect'
        return render_template('result.html', result=result)
    return render_template('play.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

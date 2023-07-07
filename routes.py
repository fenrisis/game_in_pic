from flask import render_template, request
from game_in_pic import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        # Compare user input with the correct answer
        if user_input == 'correct_answer':
            # Render the correct.html template
            return render_template('correct.html')
        else:
            # Render the incorrect.html template
            return render_template('incorrect.html')
    
    # Render the play.html template
    return render_template('play.html')


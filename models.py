from game_in_pic import db

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    prompt_text = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))

from ..database import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.String(30), unique=True)

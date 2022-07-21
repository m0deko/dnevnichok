from ..database import db

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    homeworkText = db.Column(db.String(500), default="")
    homeworkFile = db.Column(db.LargeBinary, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

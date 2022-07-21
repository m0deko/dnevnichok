from ..database import db

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'))
    timetable_file = db.Column(db.LargeBinary, nullable=True)
    data = db.Column(db.DateTime, nullable=False)
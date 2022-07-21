from ..database import db
from datetime import datetime

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'))
    lesson_id = db.Column(db.Integer)
    mark = db.Column(db.Integer)
    coefficient = db.Column(db.Integer, default=1)
    reason = db.Column(db.String(100), default="")
    date = db.Column(db.DateTime, default=datetime.utcnow())

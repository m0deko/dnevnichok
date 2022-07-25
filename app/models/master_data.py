from ..database import db
from datetime import datetime


class Master_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'))
    groups_id = db.Column(db.String, default=None)
    date = db.Column(db.DateTime, default=datetime.utcnow)
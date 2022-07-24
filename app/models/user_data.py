from ..database import db
from datetime import datetime

class User_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String)
    surname = db.Column(db.String(30))
    name = db.Column(db.String(30))
    patronymic = db.Column(db.String(30))
    city = db.Column(db.String(30))
    law = db.Column(db.Integer)
    avatar = db.Column(db.LargeBinary, default=None)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'), default=0)

    def __repr__(self):
        return f"<user {self.id}>"

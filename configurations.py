from flask_sqlalchemy import SQLAlchemy
from flask import *
import os
from algoritms import middle_marks, png_check
from dateGet import *
from werkzeug.security import generate_password_hash, check_password_hash

MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0615609b11c2c41a136402df37ad24a31374d5a'
app.config.from_object(__name__)
app.permanent_session_lifetime = datetime.timedelta(hours=4)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnevnik.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Group_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    lessons = db.Column(db.LargeBinary)
    timetable = db.Column(db.LargeBinary, nullable=True)
    def __repr__(self):
        return f"<group {self.id}>"

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
    date = db.Column(db.DateTime, default= datetime.datetime.utcnow)

    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'), default=0)

    def __repr__(self):
        return f"<user {self.id}>"

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.String(30), unique=True)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'))
    lesson_id = db.Column(db.Integer)
    mark = db.Column(db.Integer)
    coefficient = db.Column(db.Integer, default=1)
    reason = db.Column(db.String(100), default="")
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    homeworkText = db.Column(db.String(500), default="")
    homeworkFile = db.Column(db.LargeBinary, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_data.id'))
    timetable_file = db.Column(db.LargeBinary, nullable=True)
    data = db.Column(db.DateTime, nullable=False)
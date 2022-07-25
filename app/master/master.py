from flask import request, session, redirect, url_for, render_template, Blueprint, make_response

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework
from ..models.master_data import Master_data

master = Blueprint('master', __name__, template_folder='templates', static_folder='static')

def getstids(grade_id):
    ids = []
    students = []
    users = User_data.query.filter(User_data.group_id == int(grade_id)).all()
    for user in users:
        ids.append(user.id)
        students.append(user.surname + " " + user.name + " " + user.patronymic)
    return ids, students

def getgrade(grade_id):
    return Group_data.query.filter(Group_data.id == int(grade_id)).first().grade

def check(str, dates):
    i = 0
    for i in range(len(dates)):
        if(str == dates[i]):
            return i
    return None

def getmarks(s_ids, dates, l_id):
    marks = []
    for id in s_ids:
        _marks = [' ']*len(dates)
        for mark in Mark.query.filter(Mark.user_id == int(id) and Mark.lesson_id == int(l_id)).all():
             k = check(mark.date, dates)
             if(k != None):
                 _marks[k] = str(mark.mark)
        marks.append(_marks)
    return marks

@master.route('/')
def index():
    print(url_for('.index'))
    return "<h1>Hey, man</h1>"

@master.route('/gradeselect', methods=['GET', 'POST'])
def gradeselect():
    grades = ['9О', '7Ш', '11Б']
    ids = [1, 2, 3]
    return render_template('gradeChoose.html', grades=grades, ids=ids, len=len(ids))

@master.route('/<grade>/marks', methods=['GET', 'POST'])
def marks(grade):
    dates = ['2022-07-25', '2022-07-18', '2022-07-11']#getdates()
    _dates = []
    for date in dates:
        _dates.append(date[date.rfind('-') + 1:] + '.' + date[date.find('-') + 1: date.rfind('-')])
    s_ids, students = getstids(grade)
    _grade = getgrade(grade)
    s_marks = getmarks(s_ids, dates, 1)
    return render_template('markInput.html', dates=_dates, grade=grade, students=students, s_marks=s_marks, len=len(s_ids), s_ids=s_ids, _grade=_grade)

@master.route('/<grade>/homework', methods=['GET', 'POST'])
def homework(grade):
    dates = ['12.11.2022', '15.11.2022', '16.11.2022']
    return render_template('createHomework.html', grade=grade, dates=dates)

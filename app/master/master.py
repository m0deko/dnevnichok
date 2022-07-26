from flask import request, session, redirect, url_for, render_template, Blueprint, make_response, g

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework
from ..models.master_data import Master_data

from .action import *

master = Blueprint('master', __name__, template_folder='templates', static_folder='static')


@master.route('/')
def index():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    session['cur_page'] = 'index'
    try:
        master_data = Master_data.query.filter(Master_data.user_id == session['id']).first()

        session['gradesID'] = master_data.groups_id.split()
        session['lessonsID'] = master_data.subject.split()

        session['curGradeID'] = session['gradesID'][0]
        session['curLessonID'] = session['lessonsID'][0]


    except Exception as ex:
        print(ex)

    return redirect(url_for('.mainpage'))


@master.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    g.grades = []
    g.lessons = []
    try:
        g.grades = [Group_data.query.filter(Group_data.id == grade_id).first().grade for grade_id in
                    session['gradesID']]
        g.lessons = [Lesson.query.filter(Lesson.id == int(lesson_id)).first().lesson for lesson_id in
                     session['lessonsID']]
    except Exception as ex:
        print(ex)
    return render_template('master_mainmenu.html', grades=g.grades, lessons=g.lessons, grades_id=session['gradesID'],
                           lessons_id=session['lessonsID'])


@master.route('/marks/<gradeID>/<lessonID>', methods=['GET', 'POST'])
def marks(gradeID, lessonID):
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    session['curGradeID'] = gradeID
    dates = [11, 12]
    students = []

    students_id, students = getstids(gradeID)
    _grade = getgrade(gradeID)
    s_marks = getmarks()
    return render_template('master_mark.html', dates=dates, grade=gradeID, students=students, s_marks=s_marks,
                           s_ids=students_id, _grade=_grade)


@master.route('/<grade>/homework', methods=['GET', 'POST'])
def homework(grade):
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    dates = ['12.11.2022', '15.11.2022', '16.11.2022']
    return render_template('master_homework.html', grade=grade, dates=dates)


@master.route('/logout')
def logout():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    session.pop('logged')
    session.pop('id')
    session.pop('cur_page')
    return redirect(url_for('main.login'))


def getstids(grade_id):
    users_id = []
    students = []
    users = User_data.query.filter(User_data.group_id == int(grade_id)).all()
    for user in users:
        users_id.append(user.id)
        students.append(user.surname + " " + user.name + " " + user.patronymic)
    return users_id, students


def getgrade(grade_id):
    res = Group_data.query.filter(Group_data.id == int(grade_id)).first().grade
    return res


def getmarks():
    pass

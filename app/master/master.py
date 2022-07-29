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
    grades = []
    lessons = []
    try:
        data = User_data.query.filter(User_data.id == session['id']).first()
        grades = [Group_data.query.filter(Group_data.id == grade_id).first().grade for grade_id in
                    session['gradesID']]
        lessons = [Lesson.query.filter(Lesson.id == int(lesson_id)).first().lesson for lesson_id in
                     session['lessonsID']]

    except Exception as ex:
        print(ex)
    return render_template('master_mainmenu.html', grades=grades, lessons=lessons, grades_id=session['gradesID'],
                           lessons_id=session['lessonsID'], data=data)


@master.route('/marks', methods=['GET', 'POST'])
def marks():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    if request.method == 'POST':
        session['curGradeID'] = request.form['grade_les'].split()[0]
        session['curLessonID'] = request.form['grade_les'].split()[1]
    dates = [11, 12]
    students = []

    students_id, students = getstids(session['curGradeID'])
    _grade = getgrade(session['curGradeID'])
    s_marks = getmarks()
    return render_template('master_mark.html', dates=dates, grade=session['curGradeID'], students=students,
                           s_marks=s_marks,
                           s_ids=students_id, _grade=_grade)


@master.route('/homework', methods=['GET', 'POST'])
def homework():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    dates = []
    cur_grade = ''
    cur_lesson = ''
    user_data = User_data.query.filter(User_data.id == session['id']).first()
    if request.method == 'POST':
        file = request.files['file']
        if Homework.query.filter(Homework.date == request.form['secret_date']).filter(
                Homework.group_id == session['curGradeID']).filter(
            Homework.lesson_id == session['curLessonID']).first() is None:
            if file and txt_check(file.filename):
                try:
                    les = file.read()

                    crt = Homework(group_id=session['curGradeID'], lesson_id=session['curLessonID'],
                                   homeworkText=request.form['com'], homeworkFile=les, date=request.form['secret_date'])
                    db.session.add(crt)
                    db.session.flush()

                    db.session.commit()
                except Exception as ex:
                    db.session.rollback()
                    print(ex)
    try:
        cur_grade = Group_data.query.filter(Group_data.id == session['curGradeID']).first().grade
        cur_lesson = Lesson.query.filter(Lesson.id == session['curLessonID']).first().lesson.capitalize().split()[0]
        data = Timetable.query.filter(Timetable.group_id == session['curGradeID']).all()
        for item in data:
            if checkMonth(item.data):
                file = item.timetable_file.decode('utf-8')

                if cur_lesson in file:
                    dates.append(item.data)
    except Exception as ex:
        print(ex)
    return render_template('master_homework.html', grade_id=session['curGradeID'], dates=dates, grade=cur_grade,
                           lesson=cur_lesson, data=user_data)


@master.route('/userava')
def userava():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    avatar = User_data.query.filter(User_data.id == session['id']).first().avatar
    img = getAvatar(avatar)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@master.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    if session['law'] == 0:
        return redirect(url_for('main.mainpage'))
    if request.method == 'POST':
        file = request.files['file']
        if file and png_check(file.filename):
            try:
                img = file.read()
                db.session.query(User_data).filter(User_data.id == session['id']).update({User_data.avatar: img})
                db.session.flush()

                db.session.commit()
            except Exception as ex:
                print(ex)
                db.session.rollback()
    return redirect(url_for('.mainpage'))


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

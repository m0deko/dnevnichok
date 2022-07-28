from flask import request, session, redirect, url_for, render_template, Blueprint, make_response, g
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework

from .action import middle_mark, png_check, getAvatar, getDate, getWeekday, generateWeekMas, minusDate, plusDate, \
    getDateObject, checkRange
from datetime import datetime

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if ('logged' not in session):
        if request.method == 'POST':
            data = User_data.query.filter(
                (User_data.username == request.form['identification']) and (
                        User_data.email == request.form['identification'])).first()
            if data:
                if check_password_hash(data.psw, request.form['password']):
                    if 'sessionCheckbox' in request.form:
                        session.permanent = True
                    else:
                        session.permanent = False
                    session['logged'] = 1
                    session['id'] = data.id
                    session['law'] = data.law
                    if session['law'] == 1:
                        return redirect(url_for('master.index'))
                    session['group_id'] = data.group_id
                    return redirect(url_for('.mainpage'))
    elif session['logged']:
        return redirect(url_for('.mainpage'))
    return render_template('main/login.html')


@main.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['password'])
            u = User_data(username=request.form['username'], email=request.form['email'], psw=hash,
                          surname=request.form['surname'], name=request.form['name'],
                          patronymic=request.form['patronymic'], city=request.form['city'], law=0)
            db.session.add(u)
            db.session.flush()

            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
    return render_template('main/register.html')


@main.route('/', methods=['GET', 'POST'])
def mainpage():
    if ('logged' not in session):
        return redirect(url_for('.login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))
    session['cur_page'] = 'mainpage'
    data = User_data.query.filter(User_data.id == session['id']).first()
    path = request.full_path
    getting_date = getDate()
    actives = ['inactive' for x in range(7)]
    if len(path) > 17:
        if request.method == "GET":
            getting_date = path[16:]
    weekday = getWeekday(getting_date)
    actives[weekday] = 'active'
    mas_date = generateWeekMas(getting_date, weekday)
    timetable_data = []
    try:
        preres = Timetable.query.filter(
            Timetable.group_id == session['group_id']).filter(Timetable.data == getting_date).first()
        timetable_data = preres.timetable_file.decode().split('\n')
        timetable_data = [line.rstrip() for line in timetable_data]
        timetable_data = [line.split() for line in timetable_data]
    except AttributeError as ex:
        print('Расписание не найдено ', ex)
    return render_template('main/mainpage.html', data=data, activate=actives, days=mas_date,
                           left=minusDate(mas_date[0]), right=plusDate(mas_date[0]), timetable=timetable_data)


@main.route('/marks', methods=['GET', 'POST'])
def marks():
    if ('logged' not in session):
        return redirect(url_for('login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))

    session['cur_page'] = 'marks'
    all_les_data = Group_data.query.first()
    all_les = []
    date_corners = ['2020-09-01', '2020-10-29']
    quarter_string = 'Никакая'
    date_corners1 = ['2022-09-01', '2022-10-29']
    date_corners2 = ['2022-11-08', '2022-12-29']
    date_corners3 = ['2023-01-10', '2023-03-23']
    date_corners4 = ['2023-04-01', '2023-06-26']

    if checkRange(date_corners1, str(datetime.now())):
        date_corners = date_corners1
        quarter_string = 'Первая'
    elif checkRange(date_corners2, str(datetime.now())):
        date_corners = date_corners2
        quarter_string = 'Вторая'

    elif checkRange(date_corners3, str(datetime.now())):
        date_corners = date_corners3
        quarter_string = 'Третья'
    elif checkRange(date_corners4, str(datetime.now())):
        date_corners = date_corners4
        quarter_string = 'Четвертая'

    if request.method == 'POST':
        if request.form['quarter'] == '1':
            date_corners = date_corners1
            quarter_string = 'Первая'
        elif request.form['quarter'] == '2':
            date_corners = date_corners2
            quarter_string = 'Вторая'
        elif request.form['quarter'] == '3':
            date_corners = date_corners3
            quarter_string = 'Третья'
        elif request.form['quarter'] == '4':
            date_corners = date_corners4
            quarter_string = 'Четвертая'
    try:
        all_les = all_les_data.lessons.decode().split('\n')
        all_les = [line.rstrip() for line in all_les]
    except Exception as ex:
        print(ex)
    all_les_dict = []
    for les in all_les:
        les_id = Lesson.query.filter(Lesson.lesson == les).first().id
        preres = Mark.query.filter(Mark.user_id == session['id']).filter(Mark.lesson_id == les_id).all()
        print(preres)
        print(date_corners)
        marks = []
        for mrk in preres:
            if checkRange(date_corners, mrk.date):
                marks.append(mrk)
        mid_mark = middle_mark([[mark.mark, mark.coefficient] for mark in marks])
        if mid_mark >= 4.5:
            col = 'good'
        elif mid_mark >= 3.5:
            col = 'normal'
        else:
            col = 'bad'
        _marks = [[mark.mark, mark.coefficient, mark.reason, mark.date] for mark in marks]
        all_les_dict += [[les, [_marks, mid_mark, col]]]

    data = User_data.query.filter(User_data.id == session['id']).first()
    return render_template('main/markpage.html', data=data, all_les=all_les_dict, quarter_str = quarter_string)


@main.route('/lessons', methods=['GET', 'POST'])
def lessons():
    if ('logged' not in session):
        return redirect(url_for('login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))
    session['cur_page'] = 'lessons'
    data = User_data.query.filter(User_data.id == session['id']).first()

    getting_date = getDate()
    weekday = getWeekday(getting_date)
    mas_date = generateWeekMas(getting_date, weekday)
    result = []
    for date in mas_date:
        try:
            date = date.rstrip()
            preres = Timetable.query.filter(
                Timetable.data == date).filter(Timetable.group_id == session['group_id']).first().timetable_file
            timetable_data = preres.decode().split('\n')
            timetable_data = [line.rstrip() for line in timetable_data]
            timetable_data = [line.split() for line in timetable_data]
            timetable_data.append(getWeekday(date))
            result.append(timetable_data)
        except Exception as ex:
            print(ex)
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']
    return render_template("main/timetable.html", data=data, timetable_data=result, wd=weekdays)


@main.route('/homework', methods=['GET', 'POST'])
def homework():
    if ('logged' not in session):
        return redirect(url_for('login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))
    session['cur_page'] = 'homework'
    data = User_data.query.filter(User_data.id == session['id']).first()
    hw_data = Homework.query.filter(Homework.group_id == data.group_id).all()
    hw_date_dict = {}
    for hw in hw_data:
        if getDateObject(hw.date) > datetime.now() and getDateObject(minusDate(hw.date)) < datetime.now():
            if hw.date not in hw_date_dict.keys():
                hw_date_dict[hw.date] = []
            route = r'C:\Users\sterl\PycharmProjects\dnevnikProject\app\main\static\txt_files\hwfile_' + str(
                hw.group_id) + '_' + str(hw.lesson_id) + '_' + str(hw.date) + '.txt'
            filename = 'hwfile_' + str(hw.group_id) + '_' + str(hw.lesson_id) + '_' + str(hw.date) + '.txt'
            with open(route, 'w', encoding='utf-8') as f:
                f.write(hw.homeworkFile.decode('utf-8'))
            hw_date_dict[hw.date] += [
                [Lesson.query.filter(Lesson.id == hw.lesson_id).first().lesson, hw.homeworkText, filename]]
    print(hw_date_dict)
    return render_template("main/homework.html", data=data, homework=hw_date_dict)


@main.route('/userava')
def userava():
    if ('logged' not in session):
        return redirect(url_for('login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))
    avatar = User_data.query.filter(User_data.id == session['id']).first().avatar
    img = getAvatar(avatar)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@main.route('/upload', methods=['POST', 'GET'])
def upload():
    if ('logged' not in session):
        return redirect(url_for('login'))
    if session['law'] == 1:
        return redirect(url_for('master.index'))
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


@main.route('/logout')
def logout():
    if 'logged' not in session:
        return redirect(url_for('.login'))
    session.pop('logged')
    session.pop('id')
    session.pop('cur_page')
    session.pop('group_id')
    return redirect(url_for('.login'))

from flask import *
import sqlite3 as sq
import datetime
import os
from FDataBase import FDataBase
from algoritms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerhjhgfbgtrf12345rf4h1jn3k7'
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

datetime.datetime.today()
datetime.datetime(2021, 3, 23, 23, 24, 55, 123456)
data_num = datetime.datetime.today().weekday()
date_string = ''
if data_num == 0:
    date_string = 'Понедельник'
elif data_num == 1:
    date_string = 'Вторник'
elif data_num == 2:
    date_string = 'Среда'
elif data_num == 3:
    date_string = 'Четверг'
elif data_num == 4:
    date_string = 'Пятница'
elif data_num == 5:
    date_string = 'Суббота'
else:
    date_string = 'Воскресение'

uroki = {'Понедельник': {0: 'Русский язык', 1: 'Английский язык', 2: 'Физика', 3: 'Физ-ра'},
         'Вторник': {0: '-', 1: 'Английский язык', 2: 'Физика', 3: 'Физ-ра'},
         'Среда': {0: 'Русский язык', 1: 'Английский язык', 2: 'Физика', 3: 'Физ-ра'},
         'Четверг': {0: 'Русский язык', 1: 'Английский язык', 2: 'Физика', 3: 'Физ-ра'},
         'Пятница': {0: 'Русский язык', 1: 'Английский язык', 2: 'Физика',  3: 'Физ-ра'},
         'Суббота': {0: 'Русский язык', 1: 'Английский язык', 2: 'Физика', 3: 'Физ-ра'},
         'Воскресение': ['Уроков нет']
         }
times1 = ['9:00-9:40', '9:50-10:30', '10:45:11:25', '11:40-12:20', '12:40-13:20', '13:40-14:20', '14:40-15:20',
          '15:30-16:10', '16:20-17:00']


day_times = times1[0:len(uroki[date_string])]


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if session.get('logged_in') and ('ddata' in session):
        return render_template('start_page.html', name=session["ddata"][5],
                               day_ras=uroki[date_string], time=day_times,
                               length=len(uroki[date_string]), day=date_string, surname = session['ddata'][4])
    else:
        session['logged_in'] = False
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logged_in']:
        return redirect(url_for('start_page'))
    elif request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        session['ddata'] = dbase.getMenu(request.form['uname'])

        if (session['ddata'] != []):
            if request.form['psw'] == (session['ddata'][2]):
                session['logged_in'] = True
                session['id'] = session['ddata'][0]
                session['username'] = request.form['uname']
                session['lesson'] = dbase.getLes(int(session['ddata'][9][0]))

                return redirect(url_for('start_page'))

    return render_template('login.html')

@app.route('/loginTeacher', methods=['GET', 'POST'])
def login_for_teacher():
    if session['logged_in']:
        return redirect(url_for('mark_input'))
    elif request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        session['ddata'] = dbase.getMenuForTeacher(request.form['uname'])
        if (session['ddata'] != []):
            if request.form['psw'] == session['ddata'][2]:
                session['logged_in'] = True
                session['id'] = session['ddata'][0]
                session['username'] = request.form['uname']
                session['class'] = dbase.getTeacher(session['ddata'][1])[9]
                session['subject'] = dbase.getTeacher(session['ddata'][1])[10]
                print(session['class'], session['subject'])
                return redirect(url_for('mark_input'))
    return render_template('login_teacher.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        if request.form['psw'] != request.form['psw-repeat']:
            flash('', category='error')
        elif not ('@' in request.form['email']):
            flash('', category='error')
        elif dbase.getMenu(request.form['username']) != [] or dbase.getMenu(request.form['email']) != []:
            flash('Аккаунт с данной почтой или логином уже существует', category='error')
        elif request.form['name'].isdigit() or request.form['second_name'].isdigit() or request.form['surname'].isdigit():
            flash('', category='error')
        else:
            flash('Регистрация прошла успешно!', category='success')
            surname = ''
            name = ''
            second_name = ''
            city = ''
            school_num = ''
            school_class = ''
            surname += request.form['surname']
            name += request.form['name']
            second_name += request.form['second_name']
            city += request.form['city']
            school_num += request.form['school_num']
            school_class += request.form['school_class']
            res = dbase.addPost(request.form['username'], request.form['psw'], request.form['email'],
                                surname, name, second_name,
                                city, school_num, school_class)
    return render_template('register.html')

@app.route('/register_teacher', methods=['POST', 'GET'])
def register_for_teacher():
    if request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        if request.form['psw'] != request.form['psw-repeat']:
            flash('', category='error')
        elif not ('@' in request.form['email']):
            flash('', category='error')
        elif dbase.getMenuForTeacher(request.form['username']) != []:
            flash('Аккаунт с данной почтой или логином уже существует', category='error')
        else:
            flash('Регистрация прошла успешно!', category='success')
            surname = request.form['surname']
            name = request.form['name']
            second_name = request.form['second_name']
            city = request.form['city']
            school_num = request.form['school_num']
            school_class = request.form['school_class']
            subject = request.form['subject']
            if subject == 'Математика' and int(school_class[0]) >= 7:
                subject = 'Алгебра'
            res = dbase.addTeacher(request.form['username'], request.form['psw'], request.form['email'],
                                surname, name, second_name,
                                city, school_num, school_class, subject)
    return render_template('reg_teacher.html')

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    db = get_db()
    dbase = FDataBase(db)
    student_mark = {}
    for les in session['lesson'][1].split():
        mark_res = dbase.getMark(les, session['id'])
        student_mark[les] = mark_res
    sred_marks = middle_marks(student_mark)
    if session.get('logged_in'):
        return render_template('page_with_mark.html', name=session["ddata"][5],
                               lessons=session['lesson'][1].split(),
                               marks=student_mark, sred=sred_marks, surname = session['ddata'][4])
    else:
        return redirect(url_for("login"))

# @app.route('/mark_input', methods=['GET', 'POST'])
# def mark_input():
#     if session.get('logged_in') and 'ddata' in session and 'class' in session:
#         db = get_db()
#         dbase = FDataBase(db)
#         result = dbase.getClass(session['class'])
#         mark = {}
#         for child in result:
#             print(child, dbase.getID(child[0]))
#             child_id = dbase.getID(child[0])
#             mark[child] = dbase.getMarks(child_id, session['class'])
#         return render_template('mark_input.html', children_list = result, marks = mark, glav = session['subject'])
#     else:
#         return redirect(url_for("login"))

@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    if session.get('logged_in'):
        return render_template('page_with_lessons.html', name=session["ddata"][5], times=times1,
                               raspis=uroki,
                               length=len(times1), surname = session['ddata'][4])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    if 'class' in session and 'subject' in session:
        session.pop('class')
        session.pop('subject')
    elif 'lesson' in session:
        session.pop('lesson')
    session.pop('username')
    session.pop('id')
    return start_page()

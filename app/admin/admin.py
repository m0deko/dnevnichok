from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework

from .action import txt_check

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [
    {'url': '.index', "title": 'Панель'},
    {'url': '.list_users', 'title': 'Список пользователей'},
    {'url': '.list_group', 'title': 'Список классов'},
    {'url': '.list_lesson', 'title': 'Список уроков'},
    {'url': '.logout', 'title': 'Выйти'},
]


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged'):
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == "admin" and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", 'error')
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list-users')
def list_users():
    if not isLogged():
        return redirect(url_for('.login'))
    a = []
    if db:
        try:
            a = User_data.query.all()
        except Exception as ex:
            print(ex)
    return render_template('admin/listusers.html', menu=menu, title='Список пользователей', list=a)


@admin.route('/list-group')
def list_group():
    if not isLogged():
        return redirect(url_for('.login'))
    a = []
    if db:
        try:
            a = Group_data.query.all()
        except Exception as ex:
            print(ex)
    return render_template('admin/listgroup.html', menu=menu, title='Список классов', list=a)

@admin.route('create-group', methods=['GET', 'POST'])
def create_group():
    if not isLogged():
        return redirect(url_for('.login'))
    if db:
        if request.method == 'POST':
            file = request.files['file']
            if file and txt_check(file.filename):
                try:
                    les = file.read()
                    group = Group_data(school=request.form['school'], grade=request.form['grade'], lessons=les)
                    db.session.add(group)
                    db.session.flush()

                    db.session.commit()
                    flash('Класс создан', category='success')
                except Exception as ex:
                    print(ex)
                    flash('Упс... Возникла ошибка', category='error')
                    db.session.rollback()

        return render_template('admin/creategroup.html', menu=menu, title='Создание класса')

@admin.route('/list-lesson')
def list_lesson():
    if not isLogged():
        return redirect(url_for('.login'))
    a = []
    if db:
        try:
            a = Lesson.query.all()
        except Exception as ex:
            print(ex)
    return render_template('admin/listlesson.html', menu=menu, title='Список уроков', list=a)

@admin.route('/create-lesson', methods=['GET', 'POST'])
def create_lesson():
    if not isLogged():
        return redirect(url_for('.login'))
    if db:
        if request.method == 'POST':
            try:
                lesson = Lesson(lesson=request.form['lesson'])
                db.session.add(lesson)
                db.session.flush()

                db.session.commit()
                flash('Урок создан', category='success')
            except Exception as ex:
                print(ex)
                flash('Упс... Возникла ошибка', category='error')
                db.session.rollback()

    return render_template('admin/createlesson.html', menu=menu, title='Форма для создания урока')

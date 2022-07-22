from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework

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
    {'url': '.logout', 'title': 'Выйти'}
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


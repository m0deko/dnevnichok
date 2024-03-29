from flask import render_template, Blueprint, session, request, redirect, url_for, flash, g
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


# ====================Login&logout=======================

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


# ======================users=======================
@admin.route('/list-users', methods=['GET', 'POST'])
def list_users():
    if not isLogged():
        return redirect(url_for('.login'))
    all_users = []
    if db:
        try:
            if request.method == 'POST':
                dl = db.session.query(User_data).get(request.form['delete'])
                db.session.delete(dl)
                db.session.commit()

            all_users = User_data.query.all()
        except Exception as ex:
            print(ex)
            db.session.rollback()

    return render_template('admin/listusers.html', menu=menu, title='Список пользователей', list=all_users)


@admin.route('/remake-user', methods=['GET', 'POST'])
def remake_user():
    if not isLogged():
        return redirect(url_for('.login'))
    if db:
        try:
            if request.method == 'POST':
                db.session.query(User_data).filter(User_data.id == all_user_data.id).update(
                    {User_data.username: request.form['username'], User_data.email: request.form['email'],
                     User_data.group_id: request.form['group_id']})
                db.session.commit()
                return redirect(url_for('.list_users'))
        except Exception as ex:
            print(ex)
            db.session.rollback()

    return render_template('admin/remake_user.html', menu=menu, title='Переназначение пользователя', data=all_user_data)


@admin.route('/commit-user', methods=['GET', 'POST'])
def commit_user():
    if not isLogged():
        return redirect(url_for('.login'))
    if request.method == 'POST':
        g.cur_id = request.form['remake']
        global all_user_data
        all_user_data = User_data.query.filter(User_data.id == g.cur_id).first()

    return redirect(url_for('.remake_user'))


# ===================group=========================
@admin.route('/list-group', methods=["GET", "POST"])
def list_group():
    if not isLogged():
        return redirect(url_for('.login'))
    all = []
    if db:
        try:
            if request.method == 'POST':
                dl = db.session.query(Group_data).get(request.form['delete'])
                db.session.delete(dl)
                db.session.commit()
            all = Group_data.query.all()

        except Exception as ex:
            print(ex)
    return render_template('admin/listgroup.html', menu=menu, title='Список классов', list=all)


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


@admin.route('/remake-group', methods=['GET', 'POST'])
def remake_group():
    if not isLogged():
        return redirect(url_for('.login'))
    if db:

        if request.method == 'POST':
            file = request.files['file']
            if file and txt_check(file.filename):
                try:
                    les = file.read()
                    db.session.query(Group_data).filter(Group_data.id == all_group_data.id).update(
                        {Group_data.school: request.form['school'], Group_data.grade: request.form['grade'],
                         Group_data.lessons: les})
                    db.session.flush()
                    db.session.commit()
                    return redirect(url_for('.list_group'))
                except Exception as ex:
                    print(ex)
                    db.session.rollback()

    return render_template('admin/remake_group.html', menu=menu, title='Переназначение класса', data=all_group_data)


@admin.route('/commit-group', methods=['GET', 'POST'])
def commit_group():
    if not isLogged():
        return redirect(url_for('.login'))
    if request.method == 'POST':
        g.cur_id = request.form['remake']
        global all_group_data
        all_group_data = Group_data.query.filter(Group_data.id == g.cur_id).first()

    return redirect(url_for('.remake_group'))


# =============================Lesson==============================
@admin.route('/list-lesson', methods=['GET', 'POST'])
def list_lesson():
    if not isLogged():
        return redirect(url_for('.login'))
    all = []
    if db:
        try:
            if request.method == 'POST':
                dl = db.session.query(Lesson).get(request.form['delete'])
                db.session.delete(dl)
                db.session.commit()
            all = Lesson.query.all()
        except Exception as ex:
            print(ex)
    return render_template('admin/listlesson.html', menu=menu, title='Список уроков', list=all)


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


@admin.route('/remake-lesson', methods=['GET', 'POST'])
def remake_lesson():
    if not isLogged():
        return redirect(url_for('.login'))
    if db:
        try:
            if request.method == 'POST':
                db.session.query(Lesson).filter(Lesson.id == all_lesson_data.id).update(
                    {Lesson.lesson: request.form['lesson']})
                db.session.commit()
                return redirect(url_for('.list_lesson'))
        except Exception as ex:
            print(ex)
            db.session.rollback()

    return render_template('admin/remake_lesson.html', menu=menu, title='Переназначение урока', data=all_lesson_data)


@admin.route('/commit-lesson', methods=['GET', 'POST'])
def commit_lesson():
    if not isLogged():
        return redirect(url_for('.login'))
    if request.method == 'POST':
        g.cur_id = request.form['remake']
        global all_lesson_data
        all_lesson_data = Lesson.query.filter(Lesson.id == g.cur_id).first()

    return redirect(url_for('.remake_lesson'))

from flask import render_template, Blueprint, session, request, redirect, url_for, flash, make_response, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework
from ..models.master_data import Master_data

from .action import checkLogin, checkEmail, codeSend, getAvatar, png_check, checkPassword
import os

change = Blueprint('change', __name__, template_folder='templates', static_folder='static')


@change.route('/')
def changes():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' in session:
        session.pop('confirm_code')
    if 'new_email' in session:
        session.pop('new_email')

    return render_template('change/changes.html', data=User_data.query.filter(User_data.id == session['id']).first())


@change.route('/changingLogin', methods=['GET', 'POST'])
def changingLogin():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' in session:
        session.pop('confirm_code')
    if request.method == 'POST':
        data = User_data.query.filter(User_data.id == session['id']).first()
        if check_password_hash(data.psw, request.form['confirmpsw']):
            if checkLogin(request.form['newLogin']):
                if User_data.query.filter(User_data.username == request.form['newLogin']).first() is None:

                    try:
                        db.session.query(User_data).filter(User_data.id == session['id']).update(
                            {User_data.username: request.form['newLogin']})
                        db.session.flush()
                        db.session.commit()

                        flash('Логин сменен успешно!', category='success')
                    except Exception as ex:
                        print(ex)
                        db.session.rollback()
                        flash('Возникла какая-то ошибка', category='error')
                else:
                    flash('Пользователь с таким логином уже существует', category='error')
            else:
                flash('Логин не соответствует требованиям', category='error')
        else:
            flash('Пароль неверен', category='error')

    return render_template('change/changingLogin.html')


@change.route('/changingEmail', methods=['GET', 'POST'])
def changingEmail():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' in session:
        session.pop('confirm_code')
    if request.method == 'POST':
        data = User_data.query.filter(User_data.id == session['id']).first()
        if check_password_hash(data.psw, request.form['confirmpsw']):
            if checkEmail(request.form['newEmail']):
                if User_data.query.filter(User_data.username == request.form['newEmail']).first() is None:
                    try:
                        session['confirm_code'] = [os.urandom(5).hex(), request.form['newEmail']]
                        return redirect(url_for('.sendCode'))
                        
                    except Exception as ex:
                        print(ex)
                        flash('Возникла какая-то ошибка', category='error')
                else:
                    flash('Пользователь с таким логином уже существует', category='error')
            else:
                flash('Логин не соответствует требованиям', category='error')
        else:
            flash('Пароль неверен', category='error')

    return render_template('change/changingEmail.html')

@change.route('/sendCode')
def sendCode():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' not in session:
        return redirect(url_for('.changes'))
    codeSend(session['confirm_code'][1], session['confirm_code'][0])
    return redirect(url_for('.confirmCode'))

@change.route('/confirmCode', methods=['GET', 'POST'])
def confirmCode():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' not in session:
        return redirect(url_for('.changes'))
    if request.method == 'POST':
        if request.form['confirmCode'] == session['confirm_code'][0]:
            try:
                db.session.query(User_data).filter(User_data.id == session['id']).update(
                    {User_data.email: session['confirm_code'][1]})
                db.session.flush()
                db.session.commit()
                flash('Вы сменили почту', category='success')
                session.pop('confirm_code')
            except Exception as ex:
                db.session.rollback()
                print(ex)
                flash('Возникла какая-то ошибка', category='error')
        else:
            flash('Код неверен', category='error')
    return render_template('change/confirmCode.html')


@change.route('/changingPsw', methods=['GET', 'POST'])
def changingPsw():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    if 'confirm_code' in session:
        session.pop('confirm_code')
    if request.method == 'POST':
        data = User_data.query.filter(User_data.id == session['id']).first()
        if check_password_hash(data.psw, request.form['confirmpsw']):
            if checkPassword(request.form['newPsw']):
                if request.form['newPsw'] == request.form['newPswRepeat']:
                    try:
                        hash = generate_password_hash(request.form['newPsw'])
                        db.session.query(User_data).filter(User_data.id == session['id']).update(
                            {User_data.psw: hash})
                        db.session.flush()
                        db.session.commit()

                        flash('Пароль сменен успешно!', category='success')
                    except Exception as ex:
                        print(ex)
                        db.session.rollback()
                        flash('Возникла какая-то ошибка', category='error')
                else:
                    flash('Пароли не совпадают', category='error')
            else:
                flash('Пароль не соответствует требованиям', category='error')
        else:
            flash('Пароль неверен', category='error')
    return render_template('change/changingPsw.html')

@change.route('/userava')
def userava():
    if ('logged' not in session):
        return redirect(url_for('main.login'))
    avatar = User_data.query.filter(User_data.id == session['id']).first().avatar
    img = getAvatar(avatar)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

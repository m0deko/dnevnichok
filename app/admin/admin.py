from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from ..database import db
from ..models.user_data import User_data
from ..models.group_data import Group_data
from ..models.lesson import Lesson
from ..models.mark import Mark
from ..models.timetable import Timetable
from ..models.homework import Homework

admini = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


admin = Admin(admini, name='Мой блог', template_mode='bootstrap3', index_view=DashBoardView(), endpoint='admin')
admin.add_view(ModelView(User_data, db.session, name='Пользователь'))

@admin.route('/')
def index():
    return render_template('admin/index.html')
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

@master.route('/')
def index():
    return "<h1>Hello</h1>"

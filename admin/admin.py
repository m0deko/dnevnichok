from flask import request, session, redirect, url_for, render_template, Blueprint

from database import db

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
def index():
    return render_template('admin/index.html')
from flask import *
import sqlite3 as sq
import os
from FDataBase import FDataBase
from algoritms import *
from dateGet import *

MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0615609b11c2c41a136402df37ad24a31374d5a'
app.config.from_object(__name__)
app.permanent_session_lifetime = datetime.timedelta(hours=4)

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


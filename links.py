from configurations import *
from dnevnik_api import DnevnikAPI


@app.before_request
def before_request():
    global base
    base = DnevnikAPI(db=db)
    global cur_page
    cur_page = ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('logged' not in session):
        if request.method == 'POST':
            cur_id = base.getAccess(request.form['identification'], request.form['password'])
            if cur_id != None:
                if 'sessionCheckbox' in request.form:
                    session.permanent = True
                else:
                    session.permanent = False
                session['logged'] = 1
                session['id'] = cur_id
                session['group_id'] = base.getGroupID(session['id'])
                print(session['id'], session['group_id'])
                return redirect(url_for('mainpage'))

            # if session['user_id']:
                # if 'sessionCheckbox' in request.form:
                #     session.permanent = True
                # else:
                #     session.permanent = False
                # session['logged'] = True
                # session['data'] = dbase.getData(session['user_id'])
                # session['group_id'] = str(session['data'][6])
                # return redirect(url_for('mainpage'))
    # elif session['logged']:
    #     return redirect(url_for('mainpage'))
    return render_template('login.html')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['password'])
            u = User_data(username=request.form['username'], email=request.form['email'], psw=hash,
                          surname=request.form['surname'], name=request.form['name'],
                          patronymic=request.form['patronymic'], city=request.form['city'], law=0)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as ex:
            db.session.rollback()
            print(ex)
    return render_template('new_register.html')


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if ('logged' not in session):
        return redirect(url_for('login'))
    session['cur_page'] = 'mainpage'
    # if request.method == "GET":
    #     print(1)
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable'][week_string]
    return render_template('new_mainpage.html', date_info=date_mas, cur_day_time=timetable, data=session['data'])


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if ('logged' not in session):
        return redirect(url_for('login'))
    session['cur_page'] = 'marks'
    with open('dnevnik.json', encoding='utf-8') as f:
        all_lessons = json.load(f)['class_id'][session['group_id']]['all_lessons']
    student_mark = []
    # for les in all_lessons:
    #     mark_res = dbase.getMarks(1, les)
    #     student_mark.append([les, mark_res])
    # sred_marks = middle_marks(student_mark)
    # return render_template('new_markpage.html', all_les=sred_marks, all_marks=student_mark, data=session['data'])


@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    if ('logged' not in session):
        return redirect(url_for('login'))
    session['cur_page'] = 'lessons'
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable']

    return render_template("timetable.html", week_timetable=timetable, data=session['data'])


@app.route('/homework', methods=['GET', 'POST'])
def homework():
    if ('logged' not in session):
        return redirect(url_for('login'))
    session['cur_page'] = 'homework'
    with open('dnevnik.json', encoding='utf-8') as f:
        homework = json.load(f)['class_id'][session['group_id']]['homework']
    return render_template("homework.html", data=session['data'], homework=homework)


@app.route('/userava')
def userava():
    if ('logged' not in session):
        return redirect(url_for('login'))
    # img = dbase.getAvatar(session['user_id'], app)
    # if not img:
    #     return ""
    # h = make_response(img)
    # h.headers['Content-Type'] = 'image/png'
    # return h


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
    #     if file and png_check(file.filename):
    #         try:
    #             img = file.read()
    #             dbase.updateAvatar(img, session['user_id'])
    #         except Exception as ex:
    #             print(ex)
    # return redirect(url_for(session['cur_page']))


@app.route('/logout')
def logout():
    if 'logged' not in session:
        return redirect(url_for('login'))
    session.pop('logged')
    session.pop('id')
    session.pop('group_id')
    return redirect(url_for('login'))

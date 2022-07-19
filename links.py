from configurations import *

@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)
    global cur_page
    cur_page = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('logged' not in session) or (not session['logged']):
        if request.method == 'POST':
            session['user_id'] = dbase.getAccess(request.form['identification'], request.form['password'])
            if session['user_id']:
                if 'sessionCheckbox' in request.form:
                    session.permanent = True
                else:
                    session.permanent = False
                session['logged'] = True
                session['data'] = dbase.getData(session['user_id'])
                session['group_id'] = str(session['data'][6])
                return redirect(url_for('mainpage'))
    elif session['logged']:
        return redirect(url_for('mainpage'))
    return render_template('login.html')



@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        dbase.addStudent(request.form['username'], request.form['password'], request.form['email'],
                         request.form['surname'], request.form['name'], request.form['name'],
                         request.form['second_name'], request.form['school'], request.form['grade'])
        return redirect(url_for('login'))
    return render_template('new_register.html')

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
    session['cur_page'] = 'mainpage'
    if request.method == "GET":
        print(1)
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable'][week_string]
    return render_template('new_mainpage.html', date_info=date_mas, cur_day_time = timetable, data = session['data'])


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
    session['cur_page'] = 'marks'
    with open('dnevnik.json', encoding='utf-8') as f:
        all_lessons = json.load(f)['class_id'][session['group_id']]['all_lessons']
    student_mark = []
    for les in all_lessons:
        mark_res = dbase.getMarks(1, les)
        student_mark.append([les, mark_res])
    sred_marks = middle_marks(student_mark)
    return render_template('new_markpage.html', all_les=sred_marks, all_marks=student_mark, data=session['data'])


@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
    session['cur_page'] = 'lessons'
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable']

    return render_template("timetable.html", week_timetable = timetable, data = session['data'])

@app.route('/homework', methods=['GET', 'POST'])
def homework():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
    session['cur_page'] = 'homework'
    with open('dnevnik.json', encoding='utf-8') as f:
        homework = json.load(f)['class_id'][session['group_id']]['homework']
    return render_template("homework.html", data=session['data'], homework=homework)

@app.route('/userava')
def userava():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))

    img = dbase.getAvatar(session['user_id'], app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and png_check(file.filename):
            try:
                img = file.read()
                dbase.updateAvatar(img, session['user_id'])
            except Exception as ex:
                print(ex)
    return redirect(url_for(session['cur_page']))

@app.route('/logout')
def logout():
    session.pop('logged')
    session.pop('user_id')
    session.pop('data')
    return redirect(url_for('login'))
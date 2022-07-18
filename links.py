from configurations import *

@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('logged' not in session) or (not session['logged']):
        if request.method == 'POST':
            session['user_id'] = dbase.getAccess(request.form['identification'], request.form['password'])
            if session['user_id']:
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
    if request.method == "GET":
        print(1)
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable'][week_string]
    return render_template('new_mainpage.html', date_info=date_mas, cur_day_time = timetable, data = session['data'])


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
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
    with open('dnevnik.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id'][session['group_id']]['timetable']

    return render_template("timetable.html", week_timetable = timetable, data = session['data'])

@app.route('/homework', methods=['GET', 'POST'])
def homework():
    if ('logged' not in session) or (not session['logged']):
        return redirect(url_for('login'))
    with open('dnevnik.json', encoding='utf-8') as f:
        homework = json.load(f)['class_id'][session['group_id']]['homework']
    return render_template("homework.html", data=session['data'], homework=homework)

@app.route('/logout')
def logout():
    session['logged'] = False
    session['user_id'] = None
    session['data'] = None
    return redirect(url_for('login'))

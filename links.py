from configurations import *


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == "GET":
        print(1)
    with open('timetable.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id']['1']["date_activity"]["2022-07-18"]['timetable']
        print(timetable)
    return render_template('new_mainpage.html', date_info=date_mas, cur_day_time = timetable)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if session['logged_in']:
    #     return redirect(url_for('start_page'))
    # elif request.method == 'POST':
    #     db = get_db()
    #     dbase = FDataBase(db)
    #     # session['ddata'] = dbase.getMenu(request.form['uname'])
    #
    #     if (session['ddata'] != []):
    #         if request.form['psw'] == (session['ddata'][2]):
    #             session['logged_in'] = True
    #             session['id'] = session['ddata'][0]
    #             session['username'] = request.form['uname']
    #             session['lesson'] = dbase.getLes(int(session['ddata'][9][0]))
    #
    #             return redirect(url_for('start_page'))
    if request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        print(dbase.getAccess(request.form['identification'], request.form['password']))
        if dbase.getAccess(request.form['identification'], request.form['password']) == 1:
            print(1)
            return redirect(url_for('mainpage'))
    return render_template('login.html')



@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = get_db()
        dbase = FDataBase(db)
        dbase.addStudent(request.form['username'], request.form['password'], request.form['email'],
                         request.form['surname'], request.form['name'], request.form['name'],
                         request.form['second_name'], request.form['school'], request.form['grade'])
        return redirect(url_for('login'))
    return render_template('new_register.html')


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    db = get_db()
    dbase = FDataBase(db)
    with open('timetable.json', encoding='utf-8') as f:
        all_lessons = json.load(f)['class_id']['1']['all_lessons']
    student_mark = []
    for les in all_lessons:
        mark_res = dbase.getMarks(1, les)
        student_mark.append([les, mark_res])
    sred_marks = middle_marks(student_mark)

    # if session.get('logged_in'):
    #     return render_template('page_with_mark.html', name=session["ddata"][5],
    #                            lessons=session['lesson'][1].split(),
    #                            marks=student_mark, sred=sred_marks, surname=session['ddata'][4])
    # else:
    #     return redirect(url_for("login"))
    return render_template('new_markpage.html', all_les = sred_marks, all_marks = student_mark)


@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    # if session.get('logged_in'):
    #     return render_template('page_with_lessons.html', name=session["ddata"][5], times=times1,
    #                            raspis=uroki,
    #                            length=len(times1), surname=session['ddata'][4])
    # else:
    #     return redirect(url_for('login'))
    with open('timetable.json', encoding='utf-8') as f:
        timetable = json.load(f)['class_id']['1']['timetable']
        print(timetable)
    return render_template("timetable.html", week_timetable = timetable)

@app.route('/logout')
def logout():
    # session['logged_in'] = False
    # if 'class' in session and 'subject' in session:
    #     session.pop('class')
    #     session.pop('subject')
    # elif 'lesson' in session:
    #     session.pop('lesson')
    # session.pop('username')
    # session.pop('id')
    return redirect(url_for('logout'))

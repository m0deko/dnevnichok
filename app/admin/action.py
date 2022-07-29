def txt_check(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == "txt" or ext == "TXT":
        return True
    return False


def checkAdminGroup(file: str, Lesson, grade:str):
    mas = file.split('\n')
    for x in range(len(mas)):
        if Lesson.query.filter(Lesson.lesson == mas[x].rstrip().lower()).first() is None:
            return False
    if not grade.isalnum() or len(grade.split()) > 1:
        return False

    return True

def checkAdminTimetable(file:str, year:str, month:str, day: str, group_id, Group_data, Lesson):
    if len(year) != 4 or not year.isdigit():
        return False
    if len(month) != 2 or not month.isdigit():
        return False
    if len(day) != 2 or not day.isdigit():
        return False
    if Group_data.query.filter(Group_data.id == group_id).first() is None:
        return False
    
    timetable = file.split('\n')
    res = []
    for x in range(len(timetable)):
        res += [timetable[x].split()]
        res[x][0] = res[x][0].replace('.', ' ')
        if Lesson.query.filter(Lesson.lesson == res[x][0].lower()).first() is None:
            return False
        if len(res[x]) > 4:
            return False
    return True

def checkAdminTimetableOnly(file:str, Lesson):
    timetable = file.split('\n')
    res = []
    for x in range(len(timetable)):
        res += [timetable[x].split()]
        res[x][0] = res[x][0].replace('.', ' ')
        if Lesson.query.filter(Lesson.lesson == res[x][0].lower()).first() is None:
            return False
        if len(res[x]) > 4:
            return False
    return True

def checkAdminDateOnly(date:str):
    if len(date) != 10:
        return False
    if not date[0:4].isdigit() or not date[4] == '-':
        return False
    if not date[5:7].isdigit() or not date[7] == '-':
        return False
    if not date[8:].isdigit():
        return False
    return True

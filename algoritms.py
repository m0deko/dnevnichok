def middle_marks(stud_marks):
    sred_marks = {}
    for lesson in stud_marks.keys():
        try:
            sred_marks[lesson] = (sum(stud_marks[lesson])) / len(stud_marks[lesson])
        except ZeroDivisionError:
            sred_marks[lesson] = 0.0
    return sred_marks

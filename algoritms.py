def middle_marks(stud_marks):
    sred_marks = []
    for lesson in stud_marks:
        sum_marks = 0
        for mark in lesson[1][0:]:
            sum_marks += mark
        try:
            sred_marks.append([lesson[0], sum_marks / len(lesson[1])])
        except ZeroDivisionError:
            sred_marks += [[lesson[0], 0.0]]
        except Exception as ex:
            print(ex)
    return sred_marks

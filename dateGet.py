import datetime

today_num = datetime.datetime.today().day
datetime.datetime(2021, 3, 23, 23, 24, 55, 123456)
week_num = datetime.datetime.today().weekday()
week_string = ''
date_mas = []
if week_num == 0:
    week_string = 'понедельник'
    for x in range(today_num, today_num + 7):
        date_mas.append([x, 'inactive'])

elif week_num == 1:
    week_string = 'вторник'
    for x in range(today_num - 1, today_num + 6):
        date_mas.append([x, 'inactive'])

elif week_num == 2:
    week_string = 'среда'
    for x in range(today_num - 2, today_num + 5):
        date_mas.append([x, 'inactive'])

elif week_num == 3:
    week_string = 'четверг'
    for x in range(today_num - 3, today_num + 4):
        date_mas.append([x, 'inactive'])

elif week_num == 4:
    week_string = 'пятница'
    for x in range(today_num - 4, today_num + 3):
        date_mas.append([x, 'inactive'])

elif week_num == 5:
    week_string = 'суббота'
    for x in range(today_num - 5, today_num + 2):
        date_mas.append([x, 'inactive'])

else:
    week_string = 'воскресение'
    for x in range(today_num - 6, today_num + 1):
        date_mas.append([x, 'inactive'])

date_mas[week_num] = [today_num, 'active']

import datetime

today_num = datetime.datetime.today().day
datetime.datetime(2021, 3, 23, 23, 24, 55, 123456)
week_num = datetime.datetime.today().weekday()
date_string = ''
date_mas = []
if week_num == 0:
    for x in range(today_num, today_num + 7):
        date_mas.append([x, 'inactive'])

elif week_num == 1:
    for x in range(today_num - 1, today_num + 6):
        date_mas.append([x, 'inactive'])

elif week_num == 2:
    for x in range(today_num - 2, today_num + 5):
        date_mas.append([x, 'inactive'])

elif week_num == 3:
    for x in range(today_num - 3, today_num + 4):
        date_mas.append([x, 'inactive'])

elif week_num == 4:
    for x in range(today_num - 4, today_num + 3):
        date_mas.append([x, 'inactive'])

elif week_num == 5:
    for x in range(today_num - 5, today_num + 2):
        date_mas.append([x, 'inactive'])

else:
    for x in range(today_num - 6, today_num + 1):
        date_mas.append([x, 'inactive'])

date_mas[week_num] = [today_num, 'active']

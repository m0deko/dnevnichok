import datetime

datetime.datetime.today()
datetime.datetime(2021, 3, 23, 23, 24, 55, 123456)
data_num = datetime.datetime.today().weekday()
date_string = ''
if data_num == 0:
    date_string = 'Понедельник'
elif data_num == 1:
    date_string = 'Вторник'
elif data_num == 2:
    date_string = 'Среда'
elif data_num == 3:
    date_string = 'Четверг'
elif data_num == 4:
    date_string = 'Пятница'
elif data_num == 5:
    date_string = 'Суббота'
else:
    date_string = 'Воскресение'

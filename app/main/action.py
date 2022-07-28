import datetime
from dateutil.relativedelta import relativedelta
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl


def middle_mark(stud_marks):
    summ = 0
    leng = 0
    for item in stud_marks:
        summ += item[0] * item[1]
        leng += item[1]
    try:
        sred_mark = round(summ / leng, 1)
    except ZeroDivisionError:
        sred_mark = 0.0
    except Exception as ex:
        sred_mark = 0.0
        print(ex)
    return sred_mark


def getAvatar(avatar):
    img = None
    if not avatar:
        try:
            with open('app/main/static/images/default.png', "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = avatar

    return img


def png_check(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == "png" or ext == "PNG" or ext == 'jpg' or ext == 'JPG' or ext == 'jpeg':
        return True
    return False


def getDate():
    return str(datetime.datetime.now())[:10]


def getActives():
    now = datetime.datetime.now()
    active = ["inactive" for x in range(7)]
    active[datetime.datetime.weekday(now)] = 'active'
    return active


def getWeekday(getting_date):
    date = datetime.datetime(int(getting_date[0:4]), int(getting_date[5:7]), int(getting_date[8:10]))
    return datetime.datetime.weekday(date)


def generateWeekMas(getting_date, week_num):
    date = datetime.datetime(int(getting_date[0:4]), int(getting_date[5:7]), int(getting_date[8:10]))
    # date = datetime.datetime(2022, 7, 22)
    res = date - relativedelta(days=week_num)
    abc = []
    for x in range(7):
        preres = res + relativedelta(days=x)
        string = str(preres)[:10]
        abc.append(string)
    return abc


def minusDate(monday):
    date = datetime.datetime(int(monday[0:4]), int(monday[5:7]), int(monday[8:10]))
    date -= relativedelta(days=7)
    string = str(date)[:10]
    return string


def plusDate(monday):
    date = datetime.datetime(int(monday[0:4]), int(monday[5:7]), int(monday[8:10]))
    date += relativedelta(days=7)
    string = str(date)[:10]
    return string


def getDateObject(getting_date):
    date = datetime.datetime(int(getting_date[0:4]), int(getting_date[5:7]), int(getting_date[8:10]))
    return date


def checkRange(date_corners: list, date: str):
    corner1 = datetime.datetime(int(date_corners[0][0:4]), int(date_corners[0][5:7]), int(date_corners[0][8:10]))
    corner2 = datetime.datetime(int(date_corners[1][0:4]), int(date_corners[1][5:7]), int(date_corners[1][8:10]))
    checking_date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))

    if corner1 <= checking_date and corner2 >= checking_date:
        return True
    return False


def checkLogin(login: str):
    if len(login) < 4 or len(login) > 15:
        return False
    if login[0] in '1234567890':
        return False
    for char in login:
        if char in '!@#$%^&*()"№;:?-_+=/|<>`~ ,_аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ':
            return False
    return True


def checkEmail(email: str):
    if '@' not in email and '.' not in email:
        return False
    for char in email:
        if char in '!@#$%^&*()"№;:?-_+=/|<>`~ ,_аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ':
            return False
    return True


def codeSend(email, code):
    my_email = 'meshsender@mail.ru'
    my_psw = 'niGPSnyJR4FyLACEEQBV'

    receiver = email

    sslcontext = ssl.create_default_context()
    port = 465
    connect = smtplib.SMTP_SSL('smtp.mail.ru', port, context=sslcontext)

    msg = MIMEMultipart()
    msg['Subject'] = 'Подтверждение почты на сайте дневника'
    msg['From'] = my_email
    msg.attach(MIMEText(code, 'plain'))

    connect.login(my_email, my_psw)
    connect.sendmail(my_email, receiver, msg.as_string())

    print('message sended!!!')

# confirm_code = os.urandom(5).hex()
# codeSend('meshsender@mail.ru', confirm_code)

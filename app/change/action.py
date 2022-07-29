import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl


def checkLogin(login: str):
    if len(login) < 4 or len(login) > 15:
        return False
    if login[0] in '1234567890':
        return False
    for char in login:
        if char in '!@#$%^&*()"№;:?-_+=/|<>`~ ,_аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ.':
            return False
    return True


def checkEmail(email: str):
    if '@' not in email and '.' not in email:
        return False
    for char in email:
        if char in '!#$%^&*()"№;:?-_+=/|<>`~ ,_аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ':
            return False
    if email[-1] == '.':
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

def checkPassword(psw:str):
    if not psw.isalnum() or psw.isspace():
        return False
    if len(psw) < 6:
        return False
    counter = 1
    past_preres = -99999
    max_counter = 1
    for x in range(1, len(psw)):
        char_last = ord(psw[x - 1])
        char_code = ord(psw[x])
        preres = char_code - char_last
        if preres == past_preres:
            counter += 1
        else:
            if max_counter < counter:
                max_counter = counter
            counter = 1
        past_preres = preres

    max_counter = counter
    if max_counter > 4:
        return False
    return True



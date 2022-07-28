import datetime
from dateutil.relativedelta import relativedelta

def checkMonth(getting_date):
    date = datetime.datetime(int(getting_date[0:4]), int(getting_date[5:7]), int(getting_date[8:10]))
    if datetime.datetime.now() < date and date - relativedelta(months=1) < datetime.datetime.now():
        return True
    return False

def txt_check(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == "txt" or ext == "TXT":
        return True
    return False

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
    if ext == "png" or ext == "PNG":
        return True
    return False
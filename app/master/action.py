import datetime

def checkMonth(getting_date):
    if str(datetime.datetime.now())[:10][5:7] == str(getting_date[5:7]):
        return True
    return False

def txt_check(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == "txt" or ext == "TXT":
        return True
    return False
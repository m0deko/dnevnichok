from configurations import *
import sqlite3
from flask import url_for


class DnevnikAPI:
    def __init__(self, db):
        self.__db = db

    def getAccess(self, identify, password):
        try:
            pre_res = User_data.query.filter(
                (User_data.username == identify) and (User_data.email == identify)).first().psw
            if check_password_hash(pre_res, password):
                return User_data.query.filter(
                    (User_data.username == identify) and (User_data.email == identify)).first().id
        except Exception as ex:
            print(ex)
        return None

    def getGroupID(self, id):
        try:
            res = User_data.query.filter(
                (User_data.id == id)).first().group_id
            return res
        except Exception as ex:
            print(ex)
        return None
    # def getMarks(self, user_id, subject):
    #     try:
    #         result = []
    #         self.__cur.execute(
    #             f'''SELECT mark, coefficient FROM mark_data WHERE user_id = {user_id} AND lesson = "{subject}"''')
    #         res = self.__cur.fetchall()
    #         # print(res, coefficient)
    #         for row in res:
    #             for x in range(row[1]):
    #                 result.append(row[0])
    #             print(row[0])
    #         return result
    #     except Exception as ex:
    #         print(ex)
    #
    # def getGroupID(self, school, grade):
    #     try:
    #         self.__cur.execute(f'''SELECT ROWID FROM schoolGrade WHERE school = "{school}" AND grade = "{grade}"''')
    #         preres = self.__cur.fetchone()
    #         if preres != None:
    #             return [x for x in preres][0]
    #         else:
    #             self.__cur.execute('''INSERT into schoolGrade(school, grade) VALUES (?, ?)''', (school, grade))
    #             self.__db.commit()
    #             self.__cur.execute(f'''SELECT ROWID FROM schoolGrade WHERE school = "{school}" AND grade = "{grade}"''')
    #             preres = self.__cur.fetchone()
    #             return [x for x in preres][0]
    #     except Exception as ex:
    #         print(ex)
    #
    # def getData(self, user_id):
    #     try:
    #         self.__cur.execute(
    #             f'''SELECT username, email, surname, name, second_name, city, group_id FROM user_data WHERE ROWID = "{user_id}"''')
    #         preres = self.__cur.fetchone()
    #         return [x for x in preres]
    #     except Exception as ex:
    #         print(ex)
    #         return None
    #
    # def addStudent(self, username, password, email, surname, name, second_name, city, school, grade):
    #     try:
    #         group_id = self.getGroupID(school, grade)
    #         key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)
    #         self.__cur.execute(
    #             '''INSERT into user_data(group_id, username, key, salt, email, surname, name, second_name, city, law, avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)''',
    #             (group_id, username, key, salt, email, surname, name, second_name, city, 0))
    #         self.__db.commit()
    #         print('successful')
    #         # self.__cur.execute(f'''INSERT into users_data()
    #         # ''')
    #     except Exception as ex:
    #         print(ex)
    #
    #
    # def getAvatar(self, user_id, app):
    #     img = None
    #     try:
    #         self.__cur.execute(f'''SELECT avatar FROM user_data WHERE ROWID = {user_id}''')
    #         img = self.__cur.fetchone()
    #         img = [x for x in img][0]
    #         if not img:
    #             with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), 'rb') as f:
    #                 img = f.read()
    #     except Exception as ex:
    #         print(ex)
    #     return img
    # def updateAvatar(self, avatar, user_id):
    #     if not avatar:
    #         return False
    #     try:
    #         binary = sqlite3.Binary(avatar)
    #         self.__cur.execute(f'''UPDATE user_data SET avatar = ? WHERE ROWID = ?''', (binary, user_id))
    #         self.__db.commit()
    #     except Exception as ex:
    #         print(ex)

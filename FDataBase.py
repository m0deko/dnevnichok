import hashlib
import os

salt = os.urandom(32)

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    # def getMenu(self, username):
    #     sql = f'''SELECT * FROM users_data WHERE username = "{username}"'''
    #     try:
    #         self.__cur.execute(sql)
    #         res = self.__cur.fetchall()
    #
    #         return [item for item in res[0]]
    #     except Exception as ex:
    #         print('Ошибка чтения из БД', ex)
    #     return []
    # def getTeacher(self, username):
    #     sql = f'''SELECT * FROM teacher_maintable WHERE username = "{username}"'''
    #     try:
    #         self.__cur.execute(sql)
    #         res = self.__cur.fetchall()
    #         return [item for item in res[0]]
    #     except Exception as ex:
    #         print('Ошибка чтения из БД', ex)
    #     return []


    def getMarks(self, user_id, subject):
        try:
            result = []
            self.__cur.execute(
                f'''SELECT mark, coefficient FROM mark_data WHERE user_id = {user_id} AND lesson = "{subject}"''')
            res = self.__cur.fetchall()
            # print(res, coefficient)
            for row in res:
                for x in range(row[1]):
                    result.append(row[0])
                print(row[0])
            return result
        except Exception as ex:
            print(ex)
    def getGroupID(self, school, grade):
        try:
            self.__cur.execute(f'''SELECT ROWID FROM schoolGrade WHERE school = "{school}" AND grade = "{grade}"''')
            preres = self.__cur.fetchone()
            if preres != None:
                return [x for x in preres][0]
            else:
                self.__cur.execute('''INSERT into schoolGrade(school, grade) VALUES (?, ?)''', (school, grade))
                self.__db.commit()
                self.__cur.execute(f'''SELECT ROWID FROM schoolGrade WHERE school = "{school}" AND grade = "{grade}"''')
                preres = self.__cur.fetchone()
                return [x for x in preres][0]
        except Exception as ex:
            print(ex)
    def getData(self, user_id):
        try:
            self.__cur.execute(f'''SELECT username, email, surname, name, second_name, city, group_id FROM user_data WHERE ROWID = "{user_id}"''')
            preres = self.__cur.fetchone()
            return [x for x in preres]
        except Exception as ex:
            print(ex)
            return None
    def addStudent(self, username, password, email, surname, name, second_name, city, school, grade):
        try:
            group_id = self.getGroupID(school, grade)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)
            self.__cur.execute('''INSERT into user_data(group_id, username, key, salt, email, surname, name, second_name, city, law) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (group_id, username, key, salt, email, surname, name, second_name, city, 0))
            self.__db.commit()
            print('successful')
            # self.__cur.execute(f'''INSERT into users_data()
            # ''')
        except Exception as ex:
            print(ex)
    def getAccess(self, identify, password):
        try:
            self.__cur.execute(f'''SELECT ROWID, key, salt FROM user_data WHERE username = "{identify}" OR email = "{identify}"''')
            preres = self.__cur.fetchone()
            key = [x for x in preres][1]
            user_salt = [x for x in preres][2]
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user_salt, 100000, dklen=128)
            if key == new_key:
                return [x for x in preres][0]
            return 0
        except Exception as ex:
            print(ex)
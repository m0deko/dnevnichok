import hashlib
import os

salt = os.urandom(32)

class FDataBase():
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

    # def addPost(self, username, psw, email, surname, name, second_name, city, school_num, school_class):
    #     try:
    #         self.__cur.execute(
    #             '''INSERT INTO users_data(group_id,username, password, email, surname, name, second_name, city, law)
    #              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    #             (username, psw, email, surname, name, second_name, city, school_num, school_class))
    #         self.__db.commit()
    #     except sqlite3.Error as ex:
    #         print(str(ex))
    #         return False
    #     return True
    #
    # def getLes(self, num):
    #     try:
    #         self.__cur.execute(f'''SELECT * FROM lessons WHERE class = {num}''')
    #         res = self.__cur.fetchall()
    #         return [item for item in res[0]]
    #     except Exception as ex:
    #         print(ex)
    #         return ''
    # def addTeacher(self, username, psw, email, surname, name, second_name, city, school_num, school_class, subject):
    #     try:
    #         self.__cur.execute(
    #             '''INSERT INTO teacher_maintable(username, password, email, surname, realname, second_name, city, school_num, school_class, subject)
    #              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    #             (username, psw, email, surname, name, second_name, city, school_num, school_class, subject))
    #         self.__db.commit()
    #     except sqlite3.Error as ex:
    #         print(str(ex))
    #         return False
    #     return True
    # def getMenuForTeacher(self, username):
    #     sql = f'''SELECT * FROM teacher_maintable WHERE username = "{username}"'''
    #     try:
    #         self.__cur.execute(sql)
    #         res = self.__cur.fetchall()
    #         return [item for item in res[0]]
    #     except Exception as ex:
    #         print('Ошибка чтения из БД', ex)
    #     return []
    # def getClass(self, class_num):
    #     try:
    #         self.__cur.execute(f'''SELECT surname FROM maintable WHERE school_class = "{class_num}"''')
    #         res = self.__cur.fetchall()
    #         result = []
    #         for x in range(len(res)):
    #             result += res[x]
    #         return result
    #     except Exception as ex:
    #         print('Ошибка чтения бд', ex)
    #     return []
    # def getMarks(self, class_num, subject):
    #     try:
    #         self.__cur.execute(f'''SELECT mark FROM marks WHERE id = {class_num} AND lesson = "{subject}"''')
    #         res = self.__cur.fetchall()
    #         result = []
    #         for x in range(len(res)):
    #             result += res[x]
    #         return result
    #     except Exception as ex:
    #         print('Ошибка чтения бд', ex)
    #     return []
    # def getID(self, username):
    #     try:
    #         self.__cur.execute(f'''SELECT id FROM maintable WHERE username = "{username}"''')
    #         res = self.__cur.fetchall()
    #         result = []
    #         for x in range(len(res)):
    #             result += res[x]
    #             print(result)
    #         return res[0]
    #     except Exception as ex:
    #         print('Ошибка чтения бд', ex)
    #     return []
    #
    # def getMark(self, les, cur_id):
    #     try:
    #         self.__cur.execute(f'''SELECT mark FROM marks WHERE id = {cur_id} AND lesson = "{les}"''')
    #         res = self.__cur.fetchall()
    #         result = []
    #         for x in range(len(res)):
    #             result += res[x]
    #         return result
    #     except Exception as ex:
    #         return []
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
    def addStudent(self, username, password, email, surname, name, second_name, city, school, grade):
        try:
            group_id = self.getGroupID(school, grade)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)
            self.__cur.execute('''INSERT into users_data(group_id, username, password, email, surname, name, second_name, city, law) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (group_id, username, key, email, surname, name, second_name, city, 0))
            self.__db.commit()
            print('successful')
            # self.__cur.execute(f'''INSERT into users_data()
            # ''')
        except Exception as ex:
            print(ex)
    def getAccess(self, identify, password):
        try:
            self.__cur.execute(f'''SELECT password FROM users_data WHERE username = "{identify}" OR email = "{identify}"''')
            preres = self.__cur.fetchone()
            key = [x for x in preres][0]
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)
            if key == new_key:
                return 1
            return 0
        except Exception as ex:
            print(ex)

import sqlite3


class FDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    def getMenu(self, username):
        sql = f'''SELECT * FROM maintable WHERE username = "{username}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()

            return [item for item in res[0]]
        except Exception as ex:
            print('Ошибка чтения из БД', ex)
        return []
    def getTeacher(self, username):
        sql = f'''SELECT * FROM teacher_maintable WHERE username = "{username}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return [item for item in res[0]]
        except Exception as ex:
            print('Ошибка чтения из БД', ex)
        return []

    def addPost(self, username, psw, email, surname, name, second_name, city, school_num, school_class):
        try:
            self.__cur.execute(
                '''INSERT INTO maintable(username, password, email, surname, realname, second_name, city, school_num, school_class)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (username, psw, email, surname, name, second_name, city, school_num, school_class))
            self.__db.commit()
        except sqlite3.Error as ex:
            print(str(ex))
            return False
        return True

    def getLes(self, num):
        try:
            self.__cur.execute(f'''SELECT * FROM lessons WHERE class = {num}''')
            res = self.__cur.fetchall()
            return [item for item in res[0]]
        except Exception as ex:
            print(ex)
            return ''
    def addTeacher(self, username, psw, email, surname, name, second_name, city, school_num, school_class, subject):
        try:
            self.__cur.execute(
                '''INSERT INTO teacher_maintable(username, password, email, surname, realname, second_name, city, school_num, school_class, subject)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (username, psw, email, surname, name, second_name, city, school_num, school_class, subject))
            self.__db.commit()
        except sqlite3.Error as ex:
            print(str(ex))
            return False
        return True
    def getMenuForTeacher(self, username):
        sql = f'''SELECT * FROM teacher_maintable WHERE username = "{username}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return [item for item in res[0]]
        except Exception as ex:
            print('Ошибка чтения из БД', ex)
        return []
    def getClass(self, class_num):
        try:
            self.__cur.execute(f'''SELECT surname FROM maintable WHERE school_class = "{class_num}"''')
            res = self.__cur.fetchall()
            result = []
            for x in range(len(res)):
                result += res[x]

            return result
        except Exception as ex:
            print('Ошибка чтения бд', ex)
        return []
    def getMarks(self, class_num, subject):
        try:
            self.__cur.execute(f'''SELECT mark FROM marks WHERE id = {class_num} AND lesson = "{subject}"''')
            res = self.__cur.fetchall()
            result = []
            for x in range(len(res)):
                result += res[x]
            return result
        except Exception as ex:
            print('Ошибка чтения бд', ex)
        return []
    def getID(self, surname):
        try:
            self.__cur.execute(f'''SELECT id FROM maintable WHERE surname = "{surname}"''')
            res = self.__cur.fetchall()
            result = []
            for x in range(len(res)):
                result += res[x]
                print(result)
            return res[0]
        except Exception as ex:
            print('Ошибка чтения бд', ex)
        return []


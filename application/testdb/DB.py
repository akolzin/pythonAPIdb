import psycopg2
import psycopg2.extras


# декоратор
def toDict(func):
    def wrapper(*args, **kwargs):
        rows = func(*args, **kwargs)
        arr = []
        for row in rows:
            d = {}
            for key in row:
                d[key] = row[key]
            arr.append(d)
        return arr

    return wrapper


class DB:
    def __init__(self):
        try:
            self.connect = psycopg2.connect(
                database="overlor",
                user="overlor",
                password="1234",
                host="127.0.0.1",
                port="5432"
            )

            self.cursor = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            print("'  id':  , 'name': '   ', ' login': '   '")
        except ValueError as err:
            print("ggggg")

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    @toDict
    def getAllUsers(self):
        self.cursor.execute("SELECT id, name, login FROM users")
        return self.cursor.fetchall()

    @toDict
    def getTestResults(self):
        query = "SELECT id, name, result, date_time FROM tests ORDER BY date_time"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insertTestResulr(self, name, result):
        query = "INSERT INTO tests (name, result, date_time) VALUES (%s, %s, now())"
        self.cursor.execute(query, (name, result))
        self.connect.commit()
        return True

# testdb = DB()
#
# #users = testdb.getAllUsers()
# #users = testdb.getTestResults()
# users = testdb.insertTestResulr('3', True)
#
#
# print(users)

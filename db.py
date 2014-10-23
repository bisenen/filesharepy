import sqlite3

db_name = "lol.db"

class MainDb():
    def __init__(self, db_name):
        self.db_name = db_name
        self.read_db_query = 'select * from transcoders;'


    def exsql(self, query):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def read_db(self, add_query=None):
        print self.exsql(self.read_db_query)
        if not add_query == None:
                print "Yay", add_query



db = MainDb(db_name)

db.read_db()
db.read_db("lol")
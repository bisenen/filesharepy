import sqlite3
import os

db_name = "lol.db"

class MainDb():

    def exsql(self, query):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def isSQLite3(self, filename=self.db_name):
        from os.path import isfile, getsize

        if not isfile(filename):
            return False
        if getsize(filename) < 100: # SQLite database file header is 100 bytes
            return False
        else:
            fd = open(filename, 'rb')
            Header = fd.read(100)
            fd.close()

            if Header[0:16] == 'SQLite format 3\000':
                return True
            else:
                return False

    def init_exist_db():
        if self.isSQLite3():
            pass
        else:
            query = """create table transcoders (
                     id integer primary key autoincrement,
                     name text,
                     ip text,
                     fullhd bool,
                     free bool
                     );
                     """
            self.exsql(query)


    def __init__(self, db_name):
        self.db_name = db_name
        self.read_db_query = 'select * from transcoders;'
        self.init_exist_db()




    def read_db(self, add_query=None):
        print self.exsql(self.read_db_query)
        if not add_query == None:
                print "Yay", add_query



db = MainDb(db_name)

db.read_db()
db.read_db("lol")
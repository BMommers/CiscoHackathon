import sqlite3
from sqlite3 import Error
from NFCLezen import nfc


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def resetDB():
    cur = conn.cursor()
    cur.execute(''' DROP TABLE IF EXISTS EIDregels; ''')
    cur.execute(''' DROP TABLE IF EXISTS EID; ''')

    cur.execute(''' 
 CREATE TABLE EID (
 id integer PRIMARY KEY)
 ;
 ''')
    cur.execute('''
 CREATE TABLE EIDregels (
 id integer,
 datetime integer NOT NULL,
 FOREIGN KEY (id) REFERENCES EID)
 ;
 ''')

def nfcAddEID():
    id, eid = reader.read()
    addEID(int(eid))

def manAddEID():
    eid = eval(input("Wat is het EID:   "))
    addEID(eid)



def addEID(eid):
    cur = conn.cursor()
    sql = """ INSERT INTO EID (id) VALUES (?) """
    cur.execute(sql, (eid,))
    conn.commit()


database = "database.sqlite"

# create a database connection
conn = create_connection(database)

reader = SimpleMFRC522.SimpleMFRC522()

menu = """1: Reset Database\n2: Add e-ID\n3: Manually add e-ID\n4:Exit\n\n"""

while True:
    print(menu)
    x = eval(input("      "))

    if x == 1:
        resetDB()
        addEID(123)
    elif x == 2:
        nfcAddEID()
    elif x == 3:
        manAddEID()
    else:
        break

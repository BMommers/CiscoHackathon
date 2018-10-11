import sqlite3, datetime
from sqlite3 import Error


class LED:
    def __init__(self, gpiopin):
        self.state = 0
        self.gpioPin = gpiopin

    def turnOn(self):
        self.state = 1
        self.updateLED()

    def turnOff(self):
        self.state = 0
        self.updateLED()

    def updateLED(self):
        # functie om LED aan te passen aan de state
        pass


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

def epochTime():
    return int(str(datetime.datetime.now().timestamp()).split(".")[0])

def checkEID(eid):
    cur = conn.cursor()
    sql = """ SELECT count(1) FROM EID WHERE id = ? """
    cur.execute(sql, (eid,))
    return bool(cur.fetchone()[0])

def recordVote(eid):
    cur = conn.cursor()
    sql = """ INSERT INTO EIDregels (id, datetime) VALUES (?, ?) """
    cur.execute(sql, (eid, epochTime()))
    conn.commit()

def readNFC():
    return 12345678


greenLED = LED(13)
yellowLED = LED(19)
redLED = LED(26)

database = "D:\\Librarys\\intelliJ-workspace\\CiscoHackathon\\database.sqlite"
conn = create_connection(database)
cur = conn.cursor()



if checkEID(123):
    recordVote(123)

#while True:
#    eid = readNFC()
#    if
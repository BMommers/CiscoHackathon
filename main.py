import sqlite3, datetime, SimpleMFRC522, time
from sqlite3 import Error
import RPi.GPIO as GPIO


class LED:
    def __init__(self, gpiopin):
        self.state = 0
        self.pin = gpiopin
        GPIO.setup(gpiopin, GPIO.OUT)

    def turnOn(self):
        self.state = 1
        self.updateLED()

    def turnOff(self):
        self.state = 0
        self.updateLED()

    def updateLED(self):
        # functie om LED aan te passen aan de state
        GPIO.output(self.pin, self.state)


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


def validEID(eid):
    cur = conn.cursor()
    sql = """ SELECT count(1) FROM EID WHERE id = ? """
    cur.execute(sql, (eid,))
    return bool(cur.fetchone()[0])


def inRecords(eid):
    cur = conn.cursor()
    sql = """ SELECT count(1) FROM EIDregels WHERE id = ? """
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

database = "database.sqlite"
conn = create_connection(database)

reader = SimpleMFRC522.SimpleMFRC522()

while True:
    try:
        id, eid = reader.read()
    finally:
        GPIO.cleanup()

    if validEID(eid):
        if not inRecords(eid):
            recordVote(eid)
            greenLED.turnOn()
            time.sleep(3)
            greenLED.turnOff()
        else:
            redLED.turnOn()
            time.sleep(3)
            redLED.turnOff()
    else:
        redLED.turnOn()
        time.sleep(3)
        redLED.turnOff()
import sqlite3, time
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


class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isPressed(self):
        return GPIO.input(self.pin)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        c = sqlite3.connect(db_file)
        return c
    except Error as e:
        print(e)

    return None


def epochTime():
    return int(str(time.time()).split(".")[0])


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

authCiv = Button(21)
unauthCiv = Button(20)

database = "database.sqlite"
conn = create_connection(database)

while True:
    if authCiv.isPressed():
        eid = 452
    elif unauthCiv.isPressed():
        eid = 738
    else:
        continue
    GPIO.cleanup()

    if validEID(eid) and not inRecords(eid):
        recordVote(eid)
        greenLED.turnOn()
        time.sleep(3)
        greenLED.turnOff()
    else:
        redLED.turnOn()
        time.sleep(3)
        redLED.turnOff()

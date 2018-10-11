import RPi.GPIO as GPIO
import MFRC522
import signal
import time
GPIO.setwarnings(False)
continue_reading = True

# Als het script stopt de GPIO pinnen weer naar normal zetten.
def leesEinde(signal,frame):
    global continue_reading
    continue_reading = False
    #GPIO.cleanup()

# Singaal uitlezem
signal.signal(signal.SIGINT, leesEinde)

# Object aanmaken voor de reader +  een authenticatie code ingeven.
MIFAREReader = MFRC522.MFRC522()
authcode = [114, 97, 115, 112, 98, 101, 114, 114, 121]

def nfc():
    nu = time.time()
    wachtTijd = 0.01
    while nu+wachtTijd > int(time.time()):

        # Scannen voor nfc tags
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Als er een tag is gevonden verder gaan

        # Het kaart Id ophalen.
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # Als het kaart Id bestaat doorgaan.
        if status == MIFAREReader.MI_OK:

            # Standard auth key voor NFC
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            # De NFC tag silecteren
            MIFAREReader.MFRC522_SelectTag(uid)

            # Autenticatie afhandelen
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Bekijken of de autenticatie gelukt is.
            if status == MIFAREReader.MI_OK:
                # 8 blokken van de NFC tag uitlezen
                data = MIFAREReader.MFRC522_Read(8)
                # Kijken of de blokken overeen komen met de Auth code.
		return data
#                if data[:9] == authcode:
#
#                    MIFAREReader.MFRC522_StopCrypto1()
#                    return True
#                else:
#                    print('Deze pas is niet geaccepteerd')
#                    return False
            else:
                print ("Autenticatie mislukt.")

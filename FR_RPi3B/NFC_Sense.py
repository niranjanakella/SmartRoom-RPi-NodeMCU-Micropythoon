import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        id, text = reader.read()
        #print(id)
        #print(text)
        if (id == 78164335817):
            print('hello Niranjan')
        else:
            print('Unknown User')
finally:
        GPIO.cleanup()

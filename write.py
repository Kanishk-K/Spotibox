#!/user/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text=input("Data to write:")
        print(len(text))
        print("Place the tag to write to")
        reader.write(text)
        print("200:Write successful")
finally:
        GPIO.cleanup()
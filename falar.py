# falar.py
import pyttsx3
import time

def falar(texto):
    time.sleep(2)
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1)
    engine.say(texto)
    engine.runAndWait()
    time.sleep(2)

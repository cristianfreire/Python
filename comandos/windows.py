import keyboard
from falar import falar 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import os


def ajustar_volume(delta):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    atual = volume.GetMasterVolumeLevelScalar()
    novo = max(0.0, min(atual + delta, 1.0))
    volume.SetMasterVolumeLevelScalar(novo, None)

def espaco():
    keyboard.send("space")

def k():
    keyboard.send("k")

def next_app():
    keyboard.send("alt+tab")

def arrow(sentido):
    print(sentido)
    keyboard.send(sentido)

def desligar_computador():
    falar("Desligando computador!")
    os.system("taskkill /IM chrome.exe /F")
    os.system("taskkill /IM explorer.exe /F")
    os.system("shutdown /s /t 0")
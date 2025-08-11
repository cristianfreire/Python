import keyboard
from falar import falar 
import math
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


def ajustar_volume(delta):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    atual = volume.GetMasterVolumeLevelScalar()
    novo = max(0.0, min(atual + delta, 1.0))
    volume.SetMasterVolumeLevelScalar(novo, None)
    falar(f"Volume ajustado para {math.floor(novo*100)} por cento")

def espaco():
    keyboard.send("space")

def k():
    keyboard.send("k")
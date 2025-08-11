import webbrowser
from falar import falar  
import requests
import re
import time


def abrir_navegador():
    falar("Abrindo navegador...")
    webbrowser.open("https://www.google.com")

def fechar_aba():
    webbrowser.close()

def proxima_aba():
    webbrowser.next()

def pausar():
    falar("Pausando...")
    webbrowser.pause()

def tocar_musica(musica):
    falar(f"Tocando {musica} no YouTube...")
    url_busca = f"https://www.youtube.com/results?search_query={musica.replace(' ', '+')}&sp=EgIQAw%3D%3D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resposta = requests.get(url_busca, headers=headers)
    if resposta.status_code != 200:
        print("Erro ao acessar YouTube")
        return

    html = resposta.text

    # Regex para encontrar playlist: /playlist?list= seguido de caracteres válidos
    match = re.search(r'(/playlist\?list=[a-zA-Z0-9_-]+)', html)
    if match:
        link_playlist = "https://www.youtube.com" + match.group(1)
        print(f"Abrindo playlist: {link_playlist}")
                
        resposta_playlist = requests.get(link_playlist, headers=headers)
        time.sleep(5)
        html_playlist = resposta_playlist.text
        decoded_url = html_playlist.encode().decode('unicode_escape')
        match_video = re.search(r'(/watch\?v=[a-zA-Z0-9_-]+&list=[a-zA-Z0-9_-]+&pp=[a-zA-Z0-9_-]+)', decoded_url)
        if not match_video:
            falar("Nenhum vídeo encontrado na playlist.")
            return
        primeiro_video_url = "https://www.youtube.com" + match_video.group(1)
        print(f"Abrindo o primeiro vídeo da playlist: {primeiro_video_url}")

        # Abre o primeiro vídeo da playlist, já reproduzindo
        webbrowser.open(primeiro_video_url)
    else:
        print("Nenhuma playlist encontrada para esse termo.")
    

    
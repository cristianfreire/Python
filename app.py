from flask import Flask, render_template, request, jsonify
import os


import speech_recognition as sr
from OpenSSL import crypto



app = Flask(__name__)

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"


def gerar_certificado():
    # Só gera se não existir
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        print("✅ Certificado SSL já existe.")
        return

    print("🔐 Gerando certificado SSL autoassinado...")

    # Cria chave privada
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    # Cria certificado
    cert = crypto.X509()
    cert.get_subject().C = "BR"
    cert.get_subject().ST = "Sao Paulo"
    cert.get_subject().L = "Sao Paulo"
    cert.get_subject().O = "Minha Empresa"
    cert.get_subject().OU = "TI"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 ano
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    # Salva os arquivos
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))

    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8"))

    print("✅ Certificado e chave gerados com sucesso!")


# === Função para falar ===
from falar import falar


# === Funções de ação ===
from comandos.navegador import *
from comandos.windows import *


def desligar_computador():
    falar("Desligando computador!")
    os.system("taskkill /IM chrome.exe /F")
    os.system("taskkill /IM explorer.exe /F")
    os.system("shutdown /s /t 0")




# === Mapeamento ===
comandos = {
    "abrir navegador": abrir_navegador,
    "fechar aba": fechar_aba,
    "proxima aba": proxima_aba,
    "desligar computador": desligar_computador,
    "pausar": pausar,
    "pausar série": pausar,
    "pausar filme": pausar,
    "pausar som": pausar,
    "pausar musica": pausar,
    "continuar série": pausar,
    "continuar filme": pausar,
    "continuar musica": pausar,
    "continuar som": pausar,
    "aumentar volume": lambda: ajustar_volume(0.05),
    "aumentar som": lambda: ajustar_volume(0.05),
    "diminuir volume": lambda: ajustar_volume(-0.05),
    "diminuir som": lambda: ajustar_volume(-0.05),
    "espaco": espaco,
    "k": k,
    "proximo app": next_app,
    "up": lambda: arrow("up"),
    "cima": lambda: arrow("up"),
    "baixo": lambda: arrow("down"),
    "down": lambda: arrow("down"),
    "left": lambda: arrow("left"),
    "right": lambda: arrow("right"),
    "direita": lambda: arrow("right"),
    "esquerda": lambda: arrow("left"),
   
}

# === Rota para página principal ===
@app.route("/")
def home():
    return render_template("index.html")


# === Rota para executar comando ===
@app.route("/executar", methods=["POST"])
def executar():
    data = request.json
    comando = data.get("comando", "").lower().strip()
    print(comando)

    # 1️⃣ Verifica comandos fixos
    for chave, acao in comandos.items():
        if chave in comando:
            acao()
            return jsonify({"resposta": f"Executando: {chave}"})

    # 2️⃣ Verifica comandos que precisam de argumento (ex: tocar música)
    if comando.startswith("tocar "):
        nome_musica = comando.replace("tocar ", "", 1)
        tocar_musica(nome_musica)
        return jsonify({"resposta": f"Tocando música: {nome_musica}"})

    return jsonify({"resposta": "Comando não reconhecido"})

if __name__ == "__main__":
    try:
        from OpenSSL import SSL
    except ImportError:
        print("⚠ É necessário instalar pyOpenSSL: pip install pyopenssl")
        exit(1)

    gerar_certificado()

    import socket
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)

    # Rodar no IP local para acessar no celular
    app.run(host=ip_local, port=5000, ssl_context=(CERT_FILE, KEY_FILE))

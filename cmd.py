from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("command")
        if cmd:
            try:
                # Executa o comando no shell
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)
    return render_template("index.html", output=output)

if __name__ == "__main__":
    # Rodar apenas localmente por segurança
    app.run(debug=True, host="192.168.0.10", port=5000)

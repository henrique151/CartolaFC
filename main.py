from flask import Flask, render_template, jsonify
from alertas import estado, enviar_mensagem, iniciar_verificacao

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", **estado)


@app.route("/status")
def status():
    return jsonify(estado)


@app.route("/forcar-envio")
def forcar_envio():
    enviar_mensagem("🚨 Alerta manual enviado pelo botão!")
    return "[✅] Mensagem manual enviada."


if __name__ == "__main__":
    iniciar_verificacao()
    app.run(host="0.0.0.0", port=5000)

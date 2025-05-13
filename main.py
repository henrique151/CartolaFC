from flask import Flask
from datetime import datetime, timedelta
import requests
from twilio.rest import Client
import os

app = Flask(__name__)

# Credenciais do Twilio (troque pelas suas)
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
number_use = os.environ.get("NUMBERUSE")
client = Client(account_sid, auth_token)


def pegar_fechamento_mercado():
    try:
        url = "https://api.cartola.globo.com/mercado/status"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        fechamento_timestamp = dados["fechamento"]["timestamp"]
        return datetime.fromtimestamp(fechamento_timestamp)
    except Exception as e:
        print(f"[ERRO] Falha ao obter dados do mercado: {e}")
        return None


def enviar_mensagem(mensagem, para="whatsapp:+5511912494624"):
    try:
        from_ = "whatsapp:+14155238886"  # Número de envio do Twilio sandbox
        msg = client.messages.create(body=mensagem, from_=from_, to=para)
        print(f"[✅] Mensagem enviada. SID: {msg.sid}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem: {e}")


@app.route("/")
def home():
    return "Servidor Cartola FC ativo ✅ | ✅ Servidor Flask funcionando no Replit!"


@app.route("/verificar")
def verificar():
    fechamento = pegar_fechamento_mercado()
    agora = datetime.now()

    if fechamento is None:
        return "[❌] Erro ao obter fechamento do mercado."

    print(f"[INFO] Agora: {agora}, Fechamento: {fechamento}")

    if fechamento - agora <= timedelta(hours=1,
                                       minutes=1) and fechamento > agora:
        enviar_mensagem(
            "🚨 O mercado do Cartola FC fecha em 1 hora! Faça seu time!")
        return "[🚨] Alerta enviado!"
    else:
        return "[ℹ️] Ainda não é hora de enviar."


# Executa no Replit
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

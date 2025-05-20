from flask import Flask, render_template_string
from datetime import datetime, timedelta
import requests
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

INSTANCE_ID = os.getenv('INSTANCE_ID')
TOKEN = os.getenv('TOKEN')
NUMERO_DESTINO = os.getenv('NUMERO_DESTINO')
URL_BASE = f'https://api.ultramsg.com/{INSTANCE_ID}/messages/chat'

mensagem_enviada = False


def credenciais_validas():
    """Verifica se as credenciais estão corretas e preenchidas."""
    if not INSTANCE_ID or not TOKEN or not NUMERO_DESTINO:
        print("[❌] Credenciais UltraMsg ausentes.")
        return False
    if not NUMERO_DESTINO.startswith("+55") or len(NUMERO_DESTINO) < 12:
        print("[❌] Número de telefone parece inválido.")
        return False
    return True


def enviar_mensagem(mensagem):
    """Envia mensagem via UltraMsg."""
    if not credenciais_validas():
        return "[❌] Erro: Credenciais inválidas."

    payload = {
        'token': TOKEN,
        'to': NUMERO_DESTINO,
        'body': mensagem
    }

    try:
        response = requests.post(URL_BASE, data=payload, timeout=10)
        response.raise_for_status()
        print(f"[✅] Mensagem enviada: {mensagem}")
        return response.text
    except Exception as e:
        print(f"[❌] Erro ao enviar mensagem: {e}")
        return str(e)


def pegar_fechamento_mercado():
    """Obtém o horário de fechamento do mercado do Cartola FC."""
    try:
        url = "https://api.cartola.globo.com/mercado/status"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        timestamp = dados["fechamento"]["timestamp"]
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"[❌] Erro ao buscar o fechamento do mercado: {e}")
        return None


def verificador_automatico():
    """Verifica periodicamente se está na hora de enviar o alerta automático."""
    global mensagem_enviada
    while True:
        fechamento = pegar_fechamento_mercado()
        agora = datetime.now()

        if fechamento:
            tempo_restante = fechamento - agora
            print(
                f"[🕒] Agora: {agora}, Fechamento: {fechamento}, Faltam: {tempo_restante}")

            if timedelta(minutes=59) <= tempo_restante <= timedelta(hours=1, minutes=1):
                if not mensagem_enviada:
                    enviar_mensagem(
                        "🚨 O mercado do Cartola FC fecha em 1 hora! Faça seu time!")
                    mensagem_enviada = True
            elif tempo_restante > timedelta(hours=1, minutes=1):
                mensagem_enviada = False

        time.sleep(60)


@app.route("/")
def home():
    """Página com botão manual."""
    return render_template_string("""
    <html>
        <head>
            <title>Enviar Alerta Manual</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>🔔 Alerta Cartola FC</h1>
            <button onclick="enviarAlerta()" 
                    style="padding: 10px 20px; font-size: 16px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Enviar Alerta Agora
            </button>
            <p id="resposta" style="margin-top: 20px; font-size: 18px;"></p>

            <script>
                function enviarAlerta() {
                    fetch('/forcar-envio')
                        .then(response => response.text())
                        .then(data => {
                            document.getElementById('resposta').innerText = data;
                        })
                        .catch(error => {
                            document.getElementById('resposta').innerText = 'Erro ao enviar alerta 😢';
                        });
                }
            </script>
        </body>
    </html>
    """)


@app.route("/forcar-envio")
def forcar_envio():
    """Força o envio da mensagem manualmente."""
    resultado = enviar_mensagem("🚨 Alerta manual enviado pelo botão!")
    return f"[✅] Mensagem Manualmente Enviado. \n Resultado:  {resultado}"


def iniciar_thread():
    """Inicia a thread que verifica automaticamente o fechamento."""
    thread = threading.Thread(target=verificador_automatico)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    iniciar_thread()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

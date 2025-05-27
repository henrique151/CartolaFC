from flask import Flask, render_template_string, jsonify
from twilio.rest import Client
from datetime import datetime, timedelta
import requests
import threading
import time
import os
from dotenv import load_dotenv
import pytz

load_dotenv()

app = Flask(__name__)

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = "whatsapp:+14155238886"
NUMERO_DESTINO = os.getenv('NUMERO_DESTINO')

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

mensagem_enviada = False
contador_execucoes = 0
ultimo_horario = None
fuso_brasil = pytz.timezone('America/Sao_Paulo')


def credenciais_validas():
    """Verifica se as credenciais estão corretas e preenchidas."""
    if not TWILIO_SID or not TWILIO_TOKEN or not NUMERO_DESTINO:
        print("[❌] Credenciais Twilio ausentes.")
        return False
    if not NUMERO_DESTINO.startswith("whatsapp:+55") or len(NUMERO_DESTINO) < 20:
        print("[❌] Número de telefone do WhatsApp parece inválido.")
        return False
    return True


def enviar_mensagem(mensagem):
    """Envia mensagem via UltraMsg."""
    if not credenciais_validas():
        return "[❌] Erro: Credenciais inválidas."

    try:
        message = twilio_client.messages.create(
            body=mensagem,
            from_=TWILIO_FROM,
            to=NUMERO_DESTINO
        )
        print(f"[✅] Mensagem enviada. SID: {message.sid}")
        return "Mensagem enviada com sucesso"
    except Exception as e:
        print(f"[❌] Erro ao enviar mensagem: {e}")
        return f"Erro: {e}"


def pegar_fechamento_mercado():
    try:
        url = "https://api.cartola.globo.com/mercado/status"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        timestamp = dados["fechamento"]["timestamp"]

        # converte para timezone Brasília
        dt_utc = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        dt_brasilia = dt_utc.astimezone(fuso_brasil)

        return dt_brasilia
    except Exception as e:
        print(f"[❌] Erro ao buscar o fechamento do mercado: {e}")
        return None


def verificador_automatico():
    """Verifica periodicamente se está na hora de enviar o alerta automático."""
    global mensagem_enviada, contador_execucoes, ultimo_horario
    mensagem_1h_enviada = False
    mensagem_1dia_enviada = False

    while True:
        fechamento = pegar_fechamento_mercado()
        agora_utc = datetime.now(tz=pytz.UTC)
        agora = agora_utc.astimezone(fuso_brasil)  # hora local

        contador_execucoes += 1
        ultimo_horario = agora.strftime("%d/%m/%Y %H:%M:%S")

        if fechamento:
            tempo_restante = fechamento - agora
            print(
                f"[🕒] Agora: {agora}, Fechamento: {fechamento}, Faltam: {tempo_restante}")

            # Alerta de 1 dia
            if timedelta(days=1) <= tempo_restante <= timedelta(days=1, minutes=2):
                if not mensagem_1dia_enviada:
                    enviar_mensagem(
                        "⏳ Faltam 24 horas para o mercado do Cartola FC fechar! Não deixe para a última hora!")
                    mensagem_1dia_enviada = True

            # Alerta de 1 hora
            if timedelta(minutes=59) <= tempo_restante <= timedelta(hours=1, minutes=1):
                if not mensagem_1h_enviada:
                    enviar_mensagem(
                        "🚨 O mercado do Cartola FC fecha em 1 hora! Faça seu time!")
                    mensagem_1h_enviada = True
            elif tempo_restante > timedelta(hours=1, minutes=1):
                mensagem_1h_enviada = False

            # Resetar alerta de 1 dia se o tempo aumentar
            if tempo_restante > timedelta(days=1, minutes=2):
                mensagem_1dia_enviada = False

        time.sleep(60)


@app.route("/status")
def status():
    return jsonify({
        "execucoes": contador_execucoes,
        "horario": ultimo_horario or "Ainda não verificado"
    })


@app.route("/")
def home():
    return render_template_string("""
    <html>
        <head><title>Cartola FC Alerta</title></head>
        <body style="text-align: center; font-family: Arial;">
            <h1>📢 Alerta do Cartola FC</h1>
            <p>⏳ Número de verificações: <strong id="verificacoes">{{ execucoes }}</strong></p>
            <p>🕒 Última verificação: <strong id="horario">{{ horario }}</strong></p>
            <button onclick="enviarAlerta()" 
                style="padding: 10px 20px; font-size: 16px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Enviar Alerta Agora
            </button>
            <p id="resposta" style="margin-top: 20px;"></p>

            <script>
                function enviarAlerta() {
                    fetch('/forcar-envio')
                        .then(response => response.text())
                        .then(data => {
                            document.getElementById('resposta').innerText = data;
                        });
                }
                function atualizarStatus() {
                    fetch('/status')
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('verificacoes').innerText = data.execucoes;
                                document.getElementById('horario').innerText = data.horario;
                            });
                    }

                    setInterval(atualizarStatus, 5000); // Atualiza a cada 5 segundos
            </script>
        </body>
    </html>
    """, execucoes=contador_execucoes, horario=ultimo_horario or "Ainda não verificado")


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

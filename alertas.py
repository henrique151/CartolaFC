from datetime import datetime, timedelta
import pytz
from twilio.rest import Client
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, NUMERO_DESTINO
from cartola_api import pegar_fechamento_mercado
from apscheduler.schedulers.background import BackgroundScheduler

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)
fuso_brasil = pytz.timezone('America/Sao_Paulo')

estado = {
    "contador": 0,
    "horario_atual": None,
    "fechamento": None,
    "dias_restantes": None,
    "horario_previsto_1d": None,
    "horario_previsto_1h": None,
    "alerta_1d": False,
    "alerta_1h": False
}


def enviar_mensagem(mensagem):
    try:
        msg = twilio_client.messages.create(
            body=mensagem,
            from_=TWILIO_FROM,
            to=NUMERO_DESTINO
        )
        print(f"[✅] Mensagem enviada. SID: {msg.sid}")
    except Exception as e:
        print(f"[❌] Erro ao enviar mensagem: {e}")


def verificador_automatico():
    agora = datetime.now(pytz.UTC).astimezone(fuso_brasil)
    fechamento = pegar_fechamento_mercado()
    estado["contador"] += 1
    estado["horario_atual"] = agora.strftime("%d/%m/%Y %H:%M:%S")

    if fechamento:
        tempo = fechamento - agora
        estado["fechamento"] = fechamento.strftime("%d/%m/%Y %H:%M:%S")
        estado["dias_restantes"] = tempo.days

        estado["horario_previsto_1d"] = (
            fechamento - timedelta(days=1)).strftime("%d/%m/%Y %H:%M:%S")
        estado["horario_previsto_1h"] = (
            fechamento - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M:%S")

        if timedelta(hours=23, minutes=55) <= tempo <= timedelta(days=1) and not estado["alerta_1d"]:
            enviar_mensagem(
                "⏳ Faltam 24 horas para o mercado do Cartola FC fechar!")
            estado["alerta_1d"] = True

        if timedelta(minutes=55) <= tempo <= timedelta(hours=1, minutes=5) and not estado["alerta_1h"]:
            enviar_mensagem(
                "🚨 O mercado do Cartola FC fecha em 1 hora! Faça seu time!")
            estado["alerta_1h"] = True

        # Reset se o tempo indicar um novo ciclo
        if tempo > timedelta(days=1, minutes=5):
            estado["alerta_1d"] = False
        if tempo > timedelta(hours=1, minutes=5):
            estado["alerta_1h"] = False
    else:
        estado.update({
            "fechamento": None,
            "dias_restantes": None,
            "horario_previsto_1d": None,
            "horario_previsto_1h": None,
            "alerta_1d": False,
            "alerta_1h": False
        })


def iniciar_verificacao():
    scheduler = BackgroundScheduler(timezone=fuso_brasil)
    scheduler.add_job(verificador_automatico, 'interval',
                      seconds=60, id='verificacao_cartola')
    scheduler.start()
    print("[🟢] Monitoramento do Cartola FC iniciado com APScheduler.")

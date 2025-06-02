from datetime import datetime
import pytz
import requests

fuso_brasil = pytz.timezone('America/Sao_Paulo')


def pegar_fechamento_mercado():
    try:
        response = requests.get(
            "https://api.cartola.globo.com/mercado/status", timeout=10)
        response.raise_for_status()
        timestamp = response.json()["fechamento"]["timestamp"]
        dt_utc = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        return dt_utc.astimezone(fuso_brasil)
    except Exception as e:
        print(f"[❌] Erro ao buscar fechamento do mercado: {e}")
        return None

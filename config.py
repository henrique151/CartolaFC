import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = "whatsapp:+14155238886"
NUMERO_DESTINO = os.getenv("NUMERO_DESTINO")

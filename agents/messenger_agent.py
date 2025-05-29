import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class MessengerAgent:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM")
        self.client = Client(self.account_sid, self.auth_token)

    def send_whatsapp(self, to_number, message):
        try:
            msg = self.client.messages.create(
                from_=self.whatsapp_from,
                body=message,
                to=to_number
            )
            print(f"[✅ WhatsApp sent] SID: {msg.sid}")
        except Exception as e:
            print(f"[❌ WhatsApp Failed] {e}")

import requests
import json

class Telegram():
    def __init__(self):
        self.chat_id = None
        self.base_url = None
        self.api_key = None

    def send_message(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        url = f"{self.base_url}/bot{self.api_key}/sendMessage"

        try:
            response = requests.get(url, params=payload)
            return response.status_code == 200
        except:
            print("Error sending message to Telegram")
            return False
        
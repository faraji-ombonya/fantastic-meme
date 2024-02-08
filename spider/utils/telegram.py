import requests
import json

from django.conf import settings


class Telegram():
    def __init__(self):
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = settings.TELEGRAM_BASE_URL
        self.api_key = settings.TELEGRAM_API_KEY

    def send_message(self, message):
        """
        Send message to a telegram chat.

        Args:
            message (str): The message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        url = f"{self.base_url}/bot{self.api_key}/sendMessage"

        try:
            response = requests.get(url, params=payload)
            print(response.json())
            return response.status_code == 200
        except:
            print("Error sending message to Telegram")
            return False
        
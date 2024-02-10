import base64
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
        
    def send_base64_image(self, base64_data, caption=None):

        base64_data = base64_data.replace("data:image/jpg;base64,", "")
        image_data = base64.b64decode(base64_data)
        with open("image.jpg", "wb") as f:
            f.write(image_data)
            
        with open("image.jpg", "rb") as image:
            files = {"photo": image}
            payload = {"chat_id": self.chat_id}

            if caption:
                payload["caption"] = caption

            url = f"{self.base_url}/bot{self.api_key}/sendPhoto"
            response = requests.post(url, params=payload, files=files)
            print(response.json())
            if response.status_code == 200:
                print("Image sent successfully.")
                return True
            else:
                print("Failed to send image.")
                return False

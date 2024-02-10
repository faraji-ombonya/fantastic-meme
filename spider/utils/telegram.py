import base64
import requests
import logging

from django.conf import settings

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s -%(levelname)s - %(message)s')

class Telegram():
    def __init__(self):
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = settings.TELEGRAM_BASE_URL
        self.api_key = settings.TELEGRAM_API_KEY

    def send_message(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": message}

        url = f"{self.base_url}/bot{self.api_key}/sendMessage"

        try:
            logging.info(f"Sending message: {message}")
            response = requests.get(url, params=payload)

            if response.status_code == 200:
                logging.info("Message sent successfully.")
                return True
            else:
                logging.info(f"An error occurred. Status: {response.status_code}")
                return False
        except:
            logging.error(f"Failed to send message to telegram.")
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

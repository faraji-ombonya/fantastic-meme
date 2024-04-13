import base64
import requests
import logging

from django.conf import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(levelname)s - %(message)s')

class Telegram():
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"    

    def __init__(self):
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = settings.TELEGRAM_BASE_URL
        self.api_key = settings.TELEGRAM_API_KEY
        self.chat_ids = {
            self.SPORTS_KENYA: settings.TELEGRAM_SPORTS_KENYA_CHAT_ID,
            self.KENYAN_POLITICS: settings.TELEGRAM_KENYAN_POLITICS_CHAT_ID,
        }
        self.url = f"{self.base_url}/bot{self.api_key}/sendMessage"

    def send_message(self, message, channel):
        payload = {
            "chat_id": self.chat_ids[channel],
            "text": message
        }

        snippet = f"{message[:32]}..." if len(message) > 32 else message
        logging.info(f"Sending message: {snippet}")

        try:
            response = requests.get(self.url, params=payload)
            if response.status_code == 200:
                logging.info("Message sent successfully.")
                return message
            else:
                logging.info(f"An error occurred. Status: {response.status_code}")
                return False
        except:
            logging.error(f"Failed to send message to telegram.")
            return False
        
    def send_messages(self, messages, chanel):
        sent_messages = []
        for message in messages:
            sent_message = self.send_message(message, chanel)
            if not sent_message:
                continue
            sent_messages.append(sent_message)
        return sent_messages
    
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

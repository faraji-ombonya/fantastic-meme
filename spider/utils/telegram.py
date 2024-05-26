import base64
import requests
import logging
import time
import random

from django.conf import settings
from spider.models import Post

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(levelname)s - %(message)s')


class Telegram():
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"
    TEST_CHANNEL = "test-channel"

    def __init__(self, rate_limited=True, acknowledge=True):
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = settings.TELEGRAM_BASE_URL
        self.api_key = settings.TELEGRAM_API_KEY
        self.chat_ids = {
            self.SPORTS_KENYA: settings.TELEGRAM_SPORTS_KENYA_CHAT_ID,
            self.KENYAN_POLITICS: settings.TELEGRAM_KENYAN_POLITICS_CHAT_ID,
            self.TEST_CHANNEL: settings.TELEGRAM_TEST_CHANNEL_CHAT_ID
        }
        self.url = f"{self.base_url}/bot{self.api_key}/sendMessage"
        self.rate_limited = rate_limited
        self.acknowledge = acknowledge

    def acknowledge_post(self, post_slug):
        """Acknowledge that a post has been sent to the channel."""
        post = Post.objects.get(slug=post_slug)
        post.mark_as_posted()
        return

    def send_post(self, post, channel):
        message = post.get("message")
        slug = post.get("slug")
        payload = {
            "chat_id": self.chat_ids[channel],
            "text": message
        }

        snippet = f"{message[:32]}..." if len(message) > 32 else message
        logging.info(f"Sending message: {snippet}")

        try:
            response = requests.get(self.url, params=payload)

            if response.status_code != 200:
                logging.info(
                    f"An error occurred. Status: {response.status_code}")
                return False

            logging.info("Message sent successfully.")

            if self.acknowledge:
                self.acknowledge_post(post_slug=slug)

            return post

        except:
            logging.error(f"Failed to send message to telegram.")
            return False

    def send_posts(self, posts, chanel):
        sent_posts = []
        for post in posts:
            sent_post = self.send_post(post, chanel)
            if not sent_post:
                continue
            sent_posts.append(sent_post)

            if self.rate_limited:
                time.sleep(random.randint(2, 5))
        return sent_posts

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

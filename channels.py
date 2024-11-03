import base64
import logging
import os
import random

import requests
import time
from dotenv import load_dotenv

from models import Post, PostManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -%(levelname)s - %(message)s'
)

load_dotenv()


TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_SPORTS_KENYA_CHAT_ID = os.getenv("TELEGRAM_SPORTS_KENYA_CHAT_ID")
TELEGRAM_TEST_CHANNEL_CHAT_ID = os.getenv("TELEGRAM_TEST_CHANNEL_CHAT_ID")
TELEGRAM_KENYAN_POLITICS_CHAT_ID = os.getenv(
    "TELEGRAM_KENYAN_POLITICS_CHAT_ID"
)

TELEGRAM_BASE_URL="https://api.telegram.org"


class Telegram():
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"
    TEST_CHANNEL = "test-channel"

    def __init__(self, rate_limited=True, acknowledge=True):
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = TELEGRAM_BASE_URL
        self.api_key = TELEGRAM_API_KEY
        self.chat_ids = {
            self.SPORTS_KENYA: TELEGRAM_SPORTS_KENYA_CHAT_ID,
            self.KENYAN_POLITICS: TELEGRAM_KENYAN_POLITICS_CHAT_ID,
            self.TEST_CHANNEL: TELEGRAM_TEST_CHANNEL_CHAT_ID
        }
        self.url = f"{self.base_url}/bot{self.api_key}/sendMessage"
        self.rate_limited = rate_limited
        self.acknowledge = acknowledge

    def acknowledge_post(self, post_slug: str) -> None:
        """Acknowledge that a post has been sent to the channel."""
        manager = PostManager()
        post = manager.get_post_by_slug(slug=post_slug)
        manager.mark_as_posted(post.id)
        return

    def send_post(self, post, channel):
        """Send a post to a Telegram channel."""
        message = post.message
        slug = post.slug
        payload = {
            "chat_id": self.chat_ids[channel],
            "text": message
        }

        snippet = f"{message[:32]}..." if len(message) > 32 else message
        logging.info(f"Sending message: {snippet}")

        response = requests.get(self.url, params=payload)

        if response.status_code != 200:
            logging.info(
                f"An error occurred. Status: {response.status_code}"
            )
            return False

        logging.info("Message sent successfully.")

        if self.acknowledge:
            self.acknowledge_post(post_slug=slug)

        return post
        
    def send_posts(self, posts, chanel) -> list[Post]:
        """Send posts to a telegram channel."""
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


class TelegramPost:
    """A telegram post."""
    def __init__(self, message: str, slug: str) -> None:
        """Initialize the instance."""
        self.message = message
        self.slug = slug

from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from typing import TYPE_CHECKING

import requests
import time


if TYPE_CHECKING:
    from spider.models import Post


TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_SPORTS_KENYA_CHAT_ID = os.getenv("TELEGRAM_SPORTS_KENYA_CHAT_ID")
TELEGRAM_TEST_CHANNEL_CHAT_ID = os.getenv("TELEGRAM_TEST_CHANNEL_CHAT_ID")
TELEGRAM_KENYAN_POLITICS_CHAT_ID = os.getenv("TELEGRAM_KENYAN_POLITICS_CHAT_ID")

TELEGRAM_BASE_URL = "https://api.telegram.org"


class Sender(ABC):
    @abstractmethod
    def send(self, posts: list[Post]):
        pass


@dataclass
class TelegramPost:
    message: str
    slug: str
    snippet: str


class TelegramSender(Sender):
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"
    TEST_CHANNEL = "test-channel"

    def __init__(self):
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = TELEGRAM_BASE_URL
        self.api_key = TELEGRAM_API_KEY

    def _to_telegram_post(self, post: Post) -> TelegramPost:
        title = post.content.get("title")
        link = post.content.get("link")
        message = f"{title}\n{link}"
        snippet = f"{message[:32]}..." if len(message) > 32 else message
        return {
            "message": message,
            "slug": post.slug,
            "snippet": snippet,
        }

    def send(self, post: Post):
        telegram_post = self._to_telegram_post(post)
        payload = {"chat_id": None, "text": telegram_post.message}
        response = requests.get(self.url, params=payload)

        if response.status_code == 200:
            post.is_posted = True
            post.save()

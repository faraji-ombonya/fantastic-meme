from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from typing import TYPE_CHECKING
from enum import Enum

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


URL = f"{TELEGRAM_BASE_URL}/bot{TELEGRAM_API_KEY}/sendMessage"


class Sender(ABC):
    @abstractmethod
    def send(self, posts: list[Post]):
        pass


@dataclass
class TelegramPost:
    message: str
    slug: str
    snippet: str


class ChannelEnum(Enum):
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"
    TEST_CHANNEL = "test-channel"


class TelegramSender(Sender):
    SPORTS_KENYA = "sports-kenya"
    KENYAN_POLITICS = "kenyan-politics"
    TEST_CHANNEL = "test-channel"

    CHANNEL = ChannelEnum

    CHANNEL_CHAT_ID = {
        CHANNEL.SPORTS_KENYA: TELEGRAM_SPORTS_KENYA_CHAT_ID,
        CHANNEL.TEST_CHANNEL: TELEGRAM_TEST_CHANNEL_CHAT_ID,
        CHANNEL.KENYAN_POLITICS: TELEGRAM_KENYAN_POLITICS_CHAT_ID,
    }

    def __init__(self, channel: ChannelEnum.name, rate_limited=True, acknowledge=True):
        self.chat_id = TELEGRAM_CHAT_ID
        self.rate_limited = rate_limited
        self.acknowledge = acknowledge
        self.channel = channel

    def set_channel(self, channel: ChannelEnum.name):
        self.channel = channel

    def _get_chat_id(self):
        if not self.channel:
            raise ValueError("Channel is not set")
        return self.CHANNEL_CHAT_ID[self.channel]

    def _to_telegram_post(self, post: Post) -> TelegramPost:
        title = post.content.get("title")
        link = post.content.get("link")
        message = f"{title}\n{link}"
        snippet = f"{message[:32]}..." if len(message) > 32 else message
        post = {
            "message": message,
            "slug": post.slug,
            "snippet": snippet,
        }
        return TelegramPost(**post)

    def send(self, post: Post):
        chat_id = self._get_chat_id()
        telegram_post = self._to_telegram_post(post)
        payload = {"chat_id": chat_id, "text": telegram_post.message}
        response = requests.get(URL, params=payload)

        if response.status_code != 200:
            response.raise_for_status()

        if self.acknowledge:
            post.is_posted = True
            post.save()

        if self.rate_limited:
            time.sleep(5)

import feedparser
import logging

from django.conf import settings
from spider.models import Post
from spider.utils.sources.base import BaseSource

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

class Standard(BaseSource):
    SPORTS = 'sports'
    POLITICS = 'politics'

    DOMAIN_URLS = {
        SPORTS: [settings.STANDARD_SPORTS_URL],
        POLITICS: [settings.STANDARD_POLITICS_URL]
    }

    def __init__(self):
        self.standard_sports_url = settings.STANDARD_SPORTS_URL
      
    def extract(self, url):
        feed = feedparser.parse(url)
        return feed.get("entries")
    
    def transform(self, entry):
        post = {}
        post['slug'] = entry.get('id')
        post['content'] = entry
        post['source'] = Post.STANDARD
        return post
        
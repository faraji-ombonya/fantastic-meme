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

    DOMAINS = {
        SPORTS: [settings.STANDARD_SPORTS_URL]
    }

    def __init__(self):
        self.standard_sports_url = settings.STANDARD_SPORTS_URL
      
    def extract(self, url):
        feed = feedparser.parse(self.standard_sports_url)
        return feed.get("entries")
    
    def extract_bulk(self, urls):
        bulk_entries = []
        for url in urls:
            entries = self.extract_v2(url)
            bulk_entries.extend(entries)
        return bulk_entries
    
    def transform(self, entry):
        post = {}
        post['slug'] = entry.get('id')
        post['content'] = entry
        post['source'] = Post.STANDARD
        return post
        
    def transform_bulk(self, entries):
        posts = []
        for entry in entries:
            post = self.transform(entry)
            posts.insert(0, post)
        return posts
    
    
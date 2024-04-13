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

    def get_entries(self):
        logging.info(f"Getting entries from The Standard RSS feed.")
        try:
            feed = feedparser.parse(self.standard_sports_url)
            return feed.get("entries")
        except:
            logging.error("Error getting posts from The standard RSS feed.")
            return False
        
    def get_posts(self, entries):
        if not entries:
            return False

        posts = []
        for entry in entries:
            post = {}
            post['slug'] = entry.get('id')
            post['content'] = entry
            post['source'] = Post.STANDARD
            posts.insert(0, post)
        return posts

    def save_posts(self, posts):
        if not posts:
            return False
        try:
            Post.objects.bulk_create(
                [Post(**post) for post in posts], ignore_conflicts=True)
            return True
        except:
            logging.error("An error occurred while saving posts.")
            return False
        
    def transform_standard_telegram(self, post):
        if not post:
            return False
        content = post.content
        title = content.get('title')
        link = content.get('link')
        return f"{title}\n{link}\n"
    
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
    
    def to_telegram_post(self, post):
        content = post.content
        title = content.get('title')
        link = content.get('link')
        
        telegram_post = {
            "message": f"{title}\n{link}",
            "slug": post.slug
        }

        return telegram_post

    def to_telegram_posts(self, posts):
        telegram_posts = []
        for post in posts:
            telegram_post = self.to_telegram_post(post)
            telegram_posts.append(telegram_post)
        return telegram_posts
    
import feedparser
import logging

from django.conf import settings
from spider.models import Post

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

class Standard():
    def __init__(self):
        self.standard_sports_url = settings.STANDARD_SPORTS_URL

    def get_entries(self):
        logging.info("Getting messages from The Standard RSS Feed.")
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
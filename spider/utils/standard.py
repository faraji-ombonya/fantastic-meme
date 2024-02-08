import feedparser
import json

from django.conf import settings

from spider.models import Post

class Standard():
    def __init__(self):
        self.standard_sports_url = settings.STANDARD_SPORTS_URL

    def get_posts(self):
        feed = feedparser.parse(self.standard_sports_url)

        posts = []

        entries = feed.get("entries")
        if entries:
            for entry in entries:
                post = {}
                post['content'] = entry
                post['slug'] = entry.get('id')

                posts.append(post)


        print(posts)
        return posts

    def save_posts(self, posts):
        Post.objects.bulk_create(
            [Post(**post) for post in posts],
            ignore_conflicts=True)
        
    def transform_standard_telegram(post):
        content = post.get('content')
        title = content.get('title')
        link = content.get('link')
        summary = content.get('summary')

        return f"{title}\n{link}\n{summary}"
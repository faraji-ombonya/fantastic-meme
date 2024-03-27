import requests
import logging
from pprint import pprint
from bs4 import BeautifulSoup

from django.conf import settings
from spider.models import Post


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class Star():
    def __init__(self):
        self.star_base_url = settings.STAR_BASE_URL
        self.urls = [
            settings.STAR_SPORTS_URL,
            settings.STAR_SPORTS_FOOTBALL_URL,
            settings.STAR_SPORTS_ATHLETICS_URL,
            settings.STAR_SPORTS_RUGBY_URL,
            settings.STAR_SPORTS_TENNIS_URL,
            settings.STAR_SPORTS_GOLF_URL,
            settings.STAR_SPORTS_BOXING_URL,
            settings.STAR_SPORTS_BASKETBALL_URL,
        ]

        self.politics_urls = [
            settings.STAR_POLITICS_URL,
        ]

    
    def get_sports_entries(self):
        return self.get_entries(self.urls)

    def get_politics_entries(self):
        return self.get_entries(self.politics_urls)
    

    def get_entries(self, urls):
        logger.info("Getting entries from the Star.")
        entries = []
        for url in urls:
            if url is None:
                continue

            try:
                logger.info(f"Getting posts from {url}")
                response = requests.get(url)
            except:
                logger.error(f"Failed to get posts from {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            if not soup:
                logger.error("Failed to parse response")
                continue

            articles = soup.find_all('div', 'section-article')
            base = self.star_base_url
            for article in articles:
                entry = {}
                entry['source'] = "The Star"

                # title
                entry['title'] = None
                title = article.find('h3')
                if title:
                    entry['title'] = title.contents[0]
                
                # link
                entry['link'] = None
                article_link = article.find('a').get("href")
                if article_link:
                    entry['link'] = f"{base}{article_link}"

                # synopsis
                entry['synopsis'] = None
                article_synopsis = article.find('p', 'article-synopsis')
                if article_synopsis:
                    entry['synopsis'] = article_synopsis.contents[0]

                # author
                entry['author'] = None
                span_article_author = article.find('span', 'article-author')
                if span_article_author:
                    author = span_article_author.contents[0]
                    if author:
                        entry['author'] = span_article_author.contents[0]
                        author_span_link = span_article_author.a
                        if author_span_link:
                            entry['author'] = author_span_link.contents[0]

                # category
                entry['category'] = None
                article_section = article.find('span', 'article-section')
                if article_section:
                    article_section_a = article_section.a
                    if article_section_a:
                        entry['category'] = article_section_a.contents[0]

                if entry.get('synopsis'):
                    entries.append(entry)      
        return entries
   
    def _extract_image_from_style(self, style):
        start_index = style.find("url(")
        end_index = style.find(");", start_index)
        if start_index != -1 and end_index != -1:
            link_style_image = style[start_index + 4:end_index].strip("'\" ")
            return link_style_image
        
    def get_posts(self, entries):
        if not entries:
            raise NoPostsFoundError

        posts = []
        for entry in entries:
            post = {}
            post['slug'] = entry.get('link')
            post['content'] = entry
            post['source'] = Post.STAR
            posts.insert(0, post)
        return posts

    def save_posts(self, posts):
        if not posts:
            return False
        try:
            Post.objects.bulk_create(
                [Post(**post) for post in posts], ignore_conflicts=True)
        except:
            logger.error("An error occurred while saving posts.")
            return False
            
    def transform_star_telegram(self, post):
        if not post:
            raise UnableToTransformPostError
        content = post.content
        title = content.get('title')
        link = content.get('link')
        return f"{title}\n{link}"

    def transform_posts(self, posts):
        if not posts:
            raise NoPostsFoundError
        transformed_posts = []
        for post in posts:
            transformed_post = self.transform_star_telegram(post)
            transformed_posts.append(transformed_post)
        return transformed_posts
    
    def get_pending_posts(self):
        pending_posts = Post.objects.filter(source=Post.STAR, is_posted=False)

        if not pending_posts:
            raise NoPendingPostsError

        return Post.objects.filter(source=Post.STAR, is_posted=False)
    


class NoPendingPostsError(Exception):
    pass

class UnableToTransformPostError(Exception):
    pass

class NoPostsFoundError(Exception):
    pass

class UnableToSavePostsError(Exception):
    pass
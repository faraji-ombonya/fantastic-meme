import requests
import logging
from pprint import pprint
from bs4 import BeautifulSoup

from django.conf import settings
from spider.models import Post
from spider.utils.sources.base import (
    BaseSource,
    NoPendingPostsError,
    UnableToSavePostsError,
    UnableToTransformPostError,
    NoPostsFoundError,
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class Star(BaseSource):
    SPORTS = 'sports'
    POLITICS = 'politics'

    DOMAIN_URLS = {
        SPORTS: [
            settings.STAR_SPORTS_URL,
            settings.STAR_SPORTS_FOOTBALL_URL,
            settings.STAR_SPORTS_ATHLETICS_URL,
            settings.STAR_SPORTS_RUGBY_URL,
            settings.STAR_SPORTS_TENNIS_URL,
            settings.STAR_SPORTS_GOLF_URL,
            settings.STAR_SPORTS_BOXING_URL,
            settings.STAR_SPORTS_BASKETBALL_URL,
        ],
        POLITICS: [
            settings.STAR_POLITICS_URL,
        ]
    }

    def __init__(self):
        self.star_base_url = settings.STAR_BASE_URL
            
    def extract(self, url):
        entries = []
        response = requests.get(url)

        if response.status_code != 200:
            logger.error("Failed to extract entries")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        if not soup:
            logger.error("Failed to parse response")
            return []

        articles = soup.find_all('div', 'section-article')
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
                entry['link'] = f"{self.star_base_url}{article_link}"

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
    
    def transform(self, entry):
        post = {}
        post['slug'] = entry.get("link")
        post['content'] = entry
        post['source'] = Post.STAR
        return post

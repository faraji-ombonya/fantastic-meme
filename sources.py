import logging
from abc import ABC, abstractmethod

import feedparser
import requests
from bs4 import BeautifulSoup

from channels import TelegramPost
from models import PostManager, Post


# Enable logging.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


# The Standard
STANDARD_SPORTS_URL="https://www.standardmedia.co.ke/rss/sports.php"
STANDARD_POLITICS_URL="https://www.standardmedia.co.ke/rss/politics.php"

# The Star
STAR_BASE_URL="https://www.the-star.co.ke"
STAR_SPORTS_URL="https://www.the-star.co.ke/sports/"
STAR_SPORTS_FOOTBALL_URL="https://www.the-star.co.ke/sports/football/"
STAR_SPORTS_ATHLETICS_URL="https://www.the-star.co.ke/sports/athletics/"
STAR_SPORTS_RUGBY_URL="https://www.the-star.co.ke/sports/rugby/"
STAR_SPORTS_TENNIS_URL="https://www.the-star.co.ke/sports/tennis/"
STAR_SPORTS_GOLF_URL="https://www.the-star.co.ke/sports/golf/"
STAR_SPORTS_BOXING_URL="https://www.the-star.co.ke/sports/boxing/"
STAR_SPORTS_BASKETBALL_URL="https://www.the-star.co.ke/sports/basketball/"
STAR_POLITICS_URL="https://www.the-star.co.ke/siasa/"


class BaseSource(ABC):
    def __init__(self) -> None:
        pass

    def load(self, post) -> None:
        """Create a Post."""
        manager = PostManager()
        manager.create(**post)

    def load_bulk(self, posts) -> None:
        """Create Posts in bulk."""
        manager = PostManager()
        manager.bulk_create([Post(**post) for post in posts])
        return

    def get_pending_posts(self, source: str) -> list[Post]:
        """Get all pending posts from the specified source."""
        manager = PostManager()
        posts = manager.get_pending_posts(source)
        return posts

    def to_telegram_post(self, post: Post) -> TelegramPost:
        """Convert a generic post to a telegram post.
        
        Arguments:
            post (Post): A generic post.

        Returns:
            telegram_post (TelegramPost): A telegram post.
        """
        content = post.content
        title = content.get('title')
        link = content.get('link')

        post = {
            "message": f"{title}\n{link}",
            "slug": post.slug
        }

        telegram_post = TelegramPost(**post)

        return telegram_post

    def to_telegram_posts(self, posts: list[Post]) -> list[TelegramPost]:
        """Convert generic posts to telegram posts.
        
        Arguments:
            posts (list[Post]): A list of generic posts.

        Returns:
            telegram_posts (list[TelegramPost]): A list of telegram posts.
        """
        telegram_posts = [self.to_telegram_post(post) for post in posts]
        return telegram_posts

    @abstractmethod
    def transform(self, entry):
        pass

    def transform_bulk(self, entries):
        posts = []
        for entry in entries:
            post = self.transform(entry)
            posts.insert(0, post)
        return posts
    
    @abstractmethod
    def extract(self, url):
        pass

    def extract_bulk(self, urls):
        bulk_entries = []
        for url in urls:
            entries = self.extract(url)
            bulk_entries.extend(entries)
        return bulk_entries


class Standard(BaseSource):
    DOMAIN_URLS = {
        "sports": [STANDARD_SPORTS_URL],
        "politics": [STANDARD_POLITICS_URL]
    }

    def __init__(self) -> None:
        self.standard_sports_url = STANDARD_SPORTS_URL
      
    def extract(self, url: str) -> dict:
        feed = feedparser.parse(url)
        return feed.get("entries")
    
    def transform(self, entry):
        post = {}
        post['slug'] = entry.get('id')
        post['content'] = entry
        post['source'] = "standard"
        return post


class Star(BaseSource):
    SPORTS = 'sports'
    POLITICS = 'politics'

    DOMAIN_URLS = {
        SPORTS: [
            STAR_SPORTS_URL,
            STAR_SPORTS_FOOTBALL_URL,
            STAR_SPORTS_ATHLETICS_URL,
            STAR_SPORTS_RUGBY_URL,
            STAR_SPORTS_TENNIS_URL,
            STAR_SPORTS_GOLF_URL,
            STAR_SPORTS_BOXING_URL,
            STAR_SPORTS_BASKETBALL_URL,
        ],
        POLITICS: [
            STAR_POLITICS_URL,
        ]
    }

    def __init__(self):
        self.star_base_url = STAR_BASE_URL
            
    def extract(self, url: str) -> list[dict]:
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
                entry['synopsis'] = article_synopsis.string

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

from abc import ABC, abstractmethod

import feedparser
import logging
import requests

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass


class TheStandardExtractor(Extractor):
    # The Standard
    STANDARD_SPORTS_URL = "https://www.standardmedia.co.ke/rss/sports.php"
    STANDARD_POLITICS_URL = "https://www.standardmedia.co.ke/rss/politics.php"
    domain_url = {"sports": STANDARD_SPORTS_URL, "politics": STANDARD_POLITICS_URL}

    def __init__(self, domain):
        self.domain = domain

    def extract(self):
        url = self.domain_url[self.domain]
        feed = feedparser.parse(url)
        return feed.get("entries")


class TheStarExtractor(Extractor):
    def extract(self, url):
        entries = []
        response = requests.get(url)

        if response.status_code != 200:
            logger.error("Failed to extract entries")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        if not soup:
            logger.error("Failed to parse response")
            return []

        articles = soup.find_all("div", "section-article")
        for article in articles:
            entry = {}
            entry["source"] = "The Star"

            # title
            entry["title"] = None
            title = article.find("h3")
            if title:
                entry["title"] = title.contents[0]

            # link
            entry["link"] = None
            article_link = article.find("a").get("href")
            if article_link:
                entry["link"] = f"{self.star_base_url}{article_link}"

            # synopsis
            entry["synopsis"] = None
            article_synopsis = article.find("p", "article-synopsis")
            if article_synopsis:
                entry["synopsis"] = article_synopsis.string

            # author
            entry["author"] = None
            span_article_author = article.find("span", "article-author")
            if span_article_author:
                author = span_article_author.contents[0]
                if author:
                    entry["author"] = span_article_author.contents[0]
                    author_span_link = span_article_author.a
                    if author_span_link:
                        entry["author"] = author_span_link.contents[0]

            # category
            entry["category"] = None
            article_section = article.find("span", "article-section")
            if article_section:
                article_section_a = article_section.a
                if article_section_a:
                    entry["category"] = article_section_a.contents[0]

            if entry.get("synopsis"):
                entries.append(entry)

        return entries

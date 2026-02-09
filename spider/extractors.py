from abc import ABC, abstractmethod
from enum import Enum

import feedparser
import logging
import requests

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ExtractorDomain(Enum):
    SPORTS = "sports"
    POLITICS = "politics"


class Extractor(ABC):
    DOMAIN = ExtractorDomain

    @abstractmethod
    def extract(self):
        pass


class TheStandardExtractor(Extractor):
    # The Standard
    STANDARD_SPORTS_URL = "https://www.standardmedia.co.ke/rss/sports.php"
    STANDARD_POLITICS_URL = "https://www.standardmedia.co.ke/rss/politics.php"

    domain_url = {
        ExtractorDomain.SPORTS: STANDARD_SPORTS_URL,
        ExtractorDomain.POLITICS: STANDARD_POLITICS_URL,
    }

    def __init__(self, domain: ExtractorDomain):
        self.domain = domain

    def extract(self):
        url = self.domain_url[self.domain]
        logger.info(f"Extracting: {url}")
        feed = feedparser.parse(url)
        return feed.get("entries")


class TheStarExtractor(Extractor):
    STAR_BASE_URL = "https://www.the-star.co.ke"
    STAR_SPORTS_URL = "https://www.the-star.co.ke/sports/"
    STAR_SPORTS_FOOTBALL_URL = "https://www.the-star.co.ke/sports/football/"
    STAR_SPORTS_ATHLETICS_URL = "https://www.the-star.co.ke/sports/athletics/"
    STAR_SPORTS_RUGBY_URL = "https://www.the-star.co.ke/sports/rugby/"
    STAR_SPORTS_TENNIS_URL = "https://www.the-star.co.ke/sports/tennis/"
    STAR_SPORTS_GOLF_URL = "https://www.the-star.co.ke/sports/golf/"
    STAR_SPORTS_BOXING_URL = "https://www.the-star.co.ke/sports/boxing/"
    STAR_SPORTS_BASKETBALL_URL = "https://www.the-star.co.ke/sports/basketball/"
    STAR_POLITICS_URL = "https://www.the-star.co.ke/siasa/"

    domain_urls = {
        ExtractorDomain.SPORTS: [
            STAR_SPORTS_URL,
            STAR_SPORTS_FOOTBALL_URL,
            STAR_SPORTS_ATHLETICS_URL,
            STAR_SPORTS_RUGBY_URL,
            STAR_SPORTS_TENNIS_URL,
            STAR_SPORTS_GOLF_URL,
            STAR_SPORTS_BOXING_URL,
            STAR_SPORTS_BASKETBALL_URL,
        ],
        ExtractorDomain.POLITICS: [STAR_POLITICS_URL],
    }

    def __init__(self, domain: ExtractorDomain):
        self.domain = domain

    def extract(self):

        if not self.domain:
            raise ValueError("Domain not set")

        urls = self.domain_urls[self.domain]

        all_entries = []

        for url in urls:
            logger.info(f"Extracting: {url}")

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

            all_entries.extend(entries)
        return all_entries

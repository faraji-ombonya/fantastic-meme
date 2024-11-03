"""Web scrapper main module."""

import time
import random
import logging

from sources import BaseSource, Standard, Star
from channels import Telegram

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class SpiderManager:
    """Spider manager.

    Example Usage:
        from spider.utils.managers import SpiderManager
        m = SpiderManager()
        m.run_sources_and_domains(sources=["standard", "star"], domains=["sports", "politics"])
    """

    SOURCE_CLASS = {
        "star": Star,
        "standard": Standard,
    }

    SOURCE_TYPE = {
        "star": "star",
        "standard": "standard",
    }

    DOMAIN_CHANNEL = {
        "sports": Telegram.SPORTS_KENYA,
        "politics": Telegram.KENYAN_POLITICS,
        "test": Telegram.TEST_CHANNEL,
    }

    def __init__(self, acknowledge=True):
        self.acknowledge = acknowledge

    def run_source(self, source: str , domain):
        """Run a source pulling content for a particular domain.

        Arguments:
            source: an object representing a content source e.g. star, standard 
                that has the name of the source and the domains to pull from
        """
        logger.info(f"Running source: {source}, Domain: {domain}")
        source_instance: BaseSource = self.SOURCE_CLASS[source]()

        try:
            urls = source_instance.DOMAIN_URLS[domain]
        except Exception as e:
            logger.warning(e)
            return

        try:
            entries = source_instance.extract_bulk(urls)
        except Exception as e:
            logger.warning("No internet connection")
            return

        posts = source_instance.transform_bulk(entries)

        source_instance.load_bulk(posts)

        pending_posts = source_instance.get_pending_posts(
            source=self.SOURCE_TYPE[source]
        )
        telegram_posts = source_instance.to_telegram_posts(pending_posts)

        telegram = Telegram(acknowledge=self.acknowledge)
        telegram.send_posts(telegram_posts, self.DOMAIN_CHANNEL[domain])

    def run_sources(self, sources: list[dict]) -> None:
        """Run sources.
        
        Arguments:
            sources (list[dict]): A list of dictionaries.
        """
        for source in sources:
            source_name = source.get("name")
            source_domains = source.get("domains")
            for domain in source_domains:
                self.run_source(source=source_name, domain=domain)
                time.sleep(random.randint(10, 20))
            time.sleep(random.randint(20, 30))

    def run_forever(self):
        """Run spider manager forever.

        Run spider manager forever by calling run_sources()
        method in an infinite loop with random sleep times.
        """
        logger.info("Running in forever mode.")
        sources = [
            {"name": "standard", "domains": ["sports", "politics"]},
            {"name": "star", "domains": ["sports", "politics"]},
        ]
        while True:
            self.run_sources(sources=sources)
            logger.info("Done fetching and sharing posts. Going to sleep for a while.")
            time.sleep(random.randint(600, 3600))



if __name__ == "__main__":
    manager = SpiderManager()
    manager.run_forever()

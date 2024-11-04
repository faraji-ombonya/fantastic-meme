"""Web scrapper main module."""

import os
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

from sources import BaseSource, Standard, Star
from channels import Telegram

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class Spider:
    """Spider."""

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

    def run_source(self, source: str , domain: str) -> None:
        """Run a source by pulling content for a particular domain.

        Arguments:
            source (str): an object representing a content source e.g. star, standard 
                that has the name of the source and the domains to pull from.
            domain (str): The domain for which to run the source e.g sports, politics
        """
        logger.info(f"Running source: {source}, Domain: {domain}")

        # Get an instance of the specified source.
        source_instance: BaseSource = self.SOURCE_CLASS[source]()

        # Get the urls of the source.
        try:
            urls = source_instance.DOMAIN_URLS[domain]
        except Exception as e:
            logger.warning(e)
            return

        # Get entries from each url.
        try:
            entries = source_instance.extract_bulk(urls)
        except Exception as e:
            logger.warning("No internet connection")
            return

        # Transform the entries into generic posts.
        posts = source_instance.transform_bulk(entries)

        # Load the generic posts into the database.
        source_instance.load_bulk(posts)

        # Get pending posts from the database.
        pending_posts = source_instance.get_pending_posts(
            source=self.SOURCE_TYPE[source]
        )

        # Convert the generic posts into telegram posts
        telegram_posts = source_instance.to_telegram_posts(pending_posts)

        # Send the posts to the appropriate telegram channel.
        telegram = Telegram(acknowledge=self.acknowledge)
        telegram.send_posts(telegram_posts, self.DOMAIN_CHANNEL[domain])

    def run_sources(self, sources: list[dict[str, list[str]]]) -> None:
        """Run sources.
        
        Arguments:
            sources (list[dict]): A list of dictionaries.
        """
        for source in sources:
            source_name = source.get("name")
            source_domains = source.get("domains")

            # Run each domain in a separate thread
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = [
                    executor.submit(self.run_source, source_name, domain) 
                    for domain in source_domains
                ]

            time.sleep(random.randint(20, 30))

    def run_forever(self) -> None:
        """Run spider manager forever.

        Run spider manager forever by calling run_sources()
        method in an infinite loop with random sleep times.
        """
        logger.info("Running in forever mode.")
        sources: list[dict[str, list[str]]] = [
            {"name": "standard", "domains": ["sports", "politics"]},
            {"name": "star", "domains": ["sports", "politics"]},
        ]
        while True:
            self.run_sources(sources=sources)
            logger.info("Done fetching and sharing posts. Going to sleep for a while.")
            time.sleep(random.randint(600, 3600))



if __name__ == "__main__":
    manager = Spider()
    manager.run_forever()

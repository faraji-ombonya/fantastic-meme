import time
import random
import logging
from spider.models import Post
from spider.utils.sources.standard import Standard
from spider.utils.sources.star import Star
from spider.utils.telegram import Telegram
from spider.utils.sources.base import (
    NoPendingPostsError,
    NoPostsFoundError,
    UnableToSavePostsError,
    UnableToTransformPostError,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class SpiderManager():
    def __init__(self):
        pass

    def run_standard(self, domain):
        """Run Standard.

        Run Standard, pulling from specified domain.

        Arguments:
        domain -- The domain to pull from e.g sports, politics
        """
        try:
            standard = Standard()
            urls = standard.DOMAINS[domain]
            entries = standard.extract(urls[0])
            posts = standard.transform_bulk(entries)
            standard.load_bulk(posts)
            pending_posts = standard.get_pending_posts(source=Post.STANDARD)
            telegram_posts = standard.to_telegram_posts(pending_posts)

            telegram = Telegram()
            domain_channel = {
                standard.SPORTS: telegram.SPORTS_KENYA,
                "test": telegram.TEST_CHANNEL
            }
            telegram.send_posts(telegram_posts, domain_channel[domain])
        except NoPendingPostsError:
            logger.warning("No pending posts from standard")

    def run_star(self, domain):
        """Run The Star. 

        Run The Star, pulling from specified domain.

        Arguments:
        domain -- The domain to pull from e.g sports, politics
        """
        try:
            star = Star()
            urls = star.DOMAINS[domain]
            entries = star.extract_bulk(urls)
            posts = star.transform_bulk(entries)
            star.load_bulk(posts)
            pending_posts = star.get_pending_posts(source=Post.STAR)
            telegram_posts = star.to_telegram_posts(pending_posts)

            telegram = Telegram()
            domain_channel = {
                star.POLITICS: telegram.KENYAN_POLITICS,
                star.SPORTS: telegram.SPORTS_KENYA,
                "test": telegram.TEST_CHANNEL,
            }
            telegram.send_posts(telegram_posts, domain_channel[domain])
        except NoPendingPostsError:
            logger.warning("No pending posts from star")

    def run(self):
        """Run spider manager.

        Run spider manager by calling a source method and a domain.
        """
        self.run_standard('sports')
        self.run_star('sports')
        self.run_star('politics')

    def run_forever(self):
        """Run spider manager forever.

        Run spider manager forever by calling a source method and a domain
        in an infinite loop with random sleep times.
        """
        logger.info("Running in forever mode.")
        while True:
            self.run()
            logger.info(
                "Done fetching and sharing posts. Going to sleep for a while.")
            time.sleep(random.randint(600, 3600))

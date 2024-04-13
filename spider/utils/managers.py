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

    def run_standard(self):
        logger.info("Spider Manager running The Standard.")
        standard = Standard()
        entries = standard.get_entries()
        posts = standard.get_posts(entries)
        standard.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False, source=Post.STANDARD)

        if not pending_posts:
            logger.warning("There are no pending posts from The Standard.")
            return
        
        telegram = Telegram()
        for post in pending_posts:
            message = standard.transform_standard_telegram(post)
            result = telegram.send_message(message, Telegram.SPORTS_KENYA)
            if result:
                post.mark_as_posted()
            time.sleep(random.randint(5, 10))
        logger.info("Done posting posts from The Standard.")
        return

    def run_star(self, domain):
        try:
            star = Star()
            urls = star.DOMAINS[domain]
            entries = star.extract_bulk_v2(urls)
            posts = star.transform_bulk_v2(entries)
            star.load_bulk(posts)
            pending_posts = star.get_pending_posts()
            telegram_posts = star.to_telegram_posts(pending_posts)
            
            telegram = Telegram()
            domain_channel = {
                star.POLITICS: telegram.KENYAN_POLITICS,
                star.SPORTS: telegram.SPORTS_KENYA
            }
            sent_posts = telegram.send_posts(telegram_posts, domain_channel[domain])
            star.acknowledge_posts(sent_posts)
        except NoPendingPostsError:
            logger.warning("No pending posts")

    def run(self):
        self.run_standard()
        time.sleep(random.randint(15, 20))
        self.run_star('sports')
        time.sleep(random.randint(15, 20))
        self.run_star('politics')

    def run_forever(self):
        logger.info("Running in forever mode.")
        while True:
            self.run()
            logger.info("Done fetching and sharing posts. Going to sleep for a while.")
            time.sleep(random.randint(600, 3600))


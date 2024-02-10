import time
import random
import logging
from spider.models import Post
from spider.utils.standard import Standard
from spider.utils.star import Star
from spider.utils.telegram import Telegram

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

class SpiderManager():
    def __init__(self):
        pass

    def run_standard(self):
        logging.info("Spider Manager running The Standard.")
        standard = Standard()
        entries = standard.get_entries()
        posts = standard.get_posts(entries)
        standard.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False, source=Post.STANDARD)

        if not pending_posts:
            logging.warning("There are no pending posts from The Standard.")
            return
        
        telegram = Telegram()
        for post in pending_posts:
            message = standard.transform_standard_telegram(post)
            result = telegram.send_message(message)
            if result:
                post.mark_as_posted()
            time.sleep(random.randint(5, 10))

    def run_star(self):
        star = Star()
        entries = star.get_entries()
        posts = star.get_posts(entries)
        star.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False, source=Post.STAR)

        if not pending_posts:
            logging.warning("There are no pending posts from The Star")
            return
        
        telegram = Telegram()
        for post in pending_posts:
            message = star.transform_star_telegram(post)
            result = telegram.send_message(message)
            if result:
                post.mark_as_posted()
            time.sleep(random.randint(5, 10))
        return

    def run(self):
        self.run_standard()
        time.sleep(random.randint(15, 20))
        self.run_star()

    def run_forever(self):
        logging.info("Running in forever mode.")
        while True:
            self.run()
            time.sleep(random.randint(60, 21600))

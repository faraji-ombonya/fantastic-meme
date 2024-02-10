import time
import random
from spider.models import Post
from spider.utils.standard import Standard
from spider.utils.star import Star
from spider.utils.telegram import Telegram


class SpiderManager():
    def __init__(self):
        pass

    def run_standard(self):
        standard = Standard()
        posts = standard.get_posts()
        standard.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False, source=Post.STANDARD)

        for post in pending_posts:
            telegram = Telegram()
            message = standard.transform_standard_telegram(post)
            result = telegram.send_message(message)
            if result:
                post.mark_as_posted()
            time.sleep(2)

    def run_star(self):
        star = Star()
        entries = star.get_entries()
        posts = star.get_posts(entries)
        star.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False, source=Post.STAR)

        for post in pending_posts:
            telegram = Telegram()
            message = star.transform_star_telegram(post)
            result = telegram.send_message(message)
            if result:
                post.mark_as_posted()
            time.sleep(2)

    def run(self):
        self.run_standard()
        time.sleep(random.randint(5, 10))
        self.run_star()

    def run_forever(self):
        while True:
            self.run()
            time.sleep(random.randint(60, 21600))

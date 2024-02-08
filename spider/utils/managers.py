import time
from spider.models import Post
from spider.utils.standard import Standard
from spider.utils.telegram import Telegram


class SpiderManager():
    def __init__(self):
        pass

    def run(self):
        standard = Standard()
        posts = standard.get_posts()
        standard.save_posts(posts)

        pending_posts = Post.objects.filter(is_posted=False)

        for post in pending_posts:
            telegram = Telegram()
            message = standard.transform_standard_telegram(post)
            result = telegram.send_message(message)
            if result:
                post.mark_as_posted()
            post.save()
            time.sleep(2)

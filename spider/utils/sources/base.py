from spider.models import Post

class BaseSource():
    def __init__(self) -> None:
        pass

    def load(self, post):
        Post.objects.create(post)

    def load_bulk(self, posts):
        Post.objects.bulk_create(
            [Post(**post) for post in posts], ignore_conflicts=True)
        
    def get_pending_posts(self, source):
        return Post.objects.filter(source=source, is_posted=False)
    
    def acknowledge_post(self, telegram_post):
        slug = telegram_post.get("slug")
        post = Post.objects.get(slug=slug)
        post.mark_as_posted()
        return
    
    def acknowledge_posts(self, telegram_posts):
        for telegram_post in telegram_posts:
            self.acknowledge_post(telegram_post)
        return


class NoPendingPostsError(Exception):
    pass


class UnableToTransformPostError(Exception):
    pass


class NoPostsFoundError(Exception):
    pass


class UnableToSavePostsError(Exception):
    pass

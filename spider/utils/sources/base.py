from abc import ABC, abstractmethod
from spider.models import Post


class BaseSource(ABC):
    def __init__(self) -> None:
        pass

    def load(self, post):
        """Create a Post."""
        Post.objects.create(post)

    def load_bulk(self, posts):
        """Create Posts in bulk."""
        Post.objects.bulk_create(
            [Post(**post) for post in posts], ignore_conflicts=True)

    def get_pending_posts(self, source):
        """Get all pending posts."""
        return Post.objects.filter(source=source, is_posted=False)

    def to_telegram_post(self, post):
        """Convert a generic post to a telegram post."""
        content = post.content
        title = content.get('title')
        link = content.get('link')

        telegram_post = {
            "message": f"{title}\n{link}",
            "slug": post.slug
        }

        return telegram_post

    def to_telegram_posts(self, posts):
        """Convert generic posts to telegram posts."""
        telegram_posts = []
        for post in posts:
            telegram_post = self.to_telegram_post(post)
            telegram_posts.append(telegram_post)
        return telegram_posts

    @abstractmethod
    def transform(self, entry):
        pass

    def transform_bulk(self, entries):
        posts = []
        for entry in entries:
            post = self.transform(entry)
            posts.insert(0, post)
        return posts
    
    @abstractmethod
    def extract(self, url):
        pass

    def extract_bulk(self, urls):
        bulk_entries = []
        for url in urls:
            entries = self.extract(url)
            bulk_entries.extend(entries)
        return bulk_entries


class NoPendingPostsError(Exception):
    pass


class UnableToTransformPostError(Exception):
    pass


class NoPostsFoundError(Exception):
    pass


class UnableToSavePostsError(Exception):
    pass

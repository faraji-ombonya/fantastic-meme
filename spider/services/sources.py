from abc import ABC, abstractmethod

from ..models import Post


class BaseSource(ABC):
    def __init__(self) -> None:
        pass

    def load(self, post) -> None:
        """Create a Post."""
        return Post.objects.create(**post)

    def load_bulk(self, posts) -> None:
        """Create Posts in bulk."""
        return Post.objects.bulk_create(
            [Post(**post) for post in posts], ignore_conflicts=True
        )

    def get_pending_posts(self, source: str) -> list[Post]:
        """Get all pending posts from the specified source."""
        return Post.get_pending_posts(source=source)

    def to_telegram_post(self, post: Post) -> TelegramPost:
        """Convert a generic post to a telegram post.

        Arguments:
            post (Post): A generic post.

        Returns:
            telegram_post (TelegramPost): A telegram post.
        """
        content = post.content
        title = content.get("title")
        link = content.get("link")

        post = {"message": f"{title}\n{link}", "slug": post.slug}

        telegram_post = TelegramPost(**post)

        return telegram_post

    def to_telegram_posts(self, posts: list[Post]) -> list[TelegramPost]:
        """Convert generic posts to telegram posts.

        Arguments:
            posts (list[Post]): A list of generic posts.

        Returns:
            telegram_posts (list[TelegramPost]): A list of telegram posts.
        """
        telegram_posts = [self.to_telegram_post(post) for post in posts]
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

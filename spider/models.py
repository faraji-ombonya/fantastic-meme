import uuid

from django.db import models

from .lib.extractors import Extractor
from .lib.transformers import Transformer, TransformedEntry


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()
    content = models.JSONField()
    source = models.CharField(max_length=255)
    is_posted = models.BooleanField(default=False)

    extractor = Extractor

    transformer = Transformer

    def __str__(self):
        return self.slug

    def mark_as_posted(self):
        self.is_posted = True
        self.save()
        return self

    def send(self):
        pass

    def to_telegram_post(self):
        title = self.content.get("title")
        link = self.content.get("link")
        return {"message": f"{title}\n{link}", "slug": self.slug}

    @classmethod
    def extract(cls):
        return cls.extractor.extract()

    @classmethod
    def extract_bulk(cls, entry):
        pass

    @classmethod
    def transform(cls, entry):
        return cls.transformer.transform(entry)

    @classmethod
    def bulk_transform(cls, entries):
        transformed_posts = []
        for entry in entries:
            transformed_post = cls.transform(entry)
            transformed_posts.append(transformed_post)
        return transformed_posts

    @classmethod
    def load(cls, transformed_entry: TransformedEntry):
        return cls.objects.create(**transformed_entry)

    @classmethod
    def bulk_load(cls, transformed_entries: list[TransformedEntry]):
        return cls.objects.bulk_create([cls(**entry) for entry in transformed_entries])

    @classmethod
    def get_pending_posts(cls, source: str):
        posts = cls.objects.filter(is_posted=False)
        if source:
            posts = posts.filter(source=source)
        return posts.all()

    @classmethod
    def to_telegram_posts(cls, posts: list["Post"]):
        return [post.to_telegram_post() for post in posts]

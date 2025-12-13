import uuid

from django.db import models


from .extractors import Extractor
from .transformers import Transformer, TransformedEntry
from .senders import Sender


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()
    content = models.JSONField()
    source = models.CharField(max_length=255)
    is_posted = models.BooleanField(default=False)

    extractor: Extractor
    transformer: Transformer
    sender: Sender

    def __str__(self):
        return self.slug

    def mark_as_posted(self):
        self.is_posted = True
        self.save()
        return self

    @classmethod
    def load(cls, transformed_entry: TransformedEntry):
        return cls.objects.create(
            slug=transformed_entry.slug,
            content=transformed_entry.content,
            source=transformed_entry.source,
        )

    @classmethod
    def bulk_load(cls, transformed_entries: list[TransformedEntry]):
        for entry in transformed_entries:
            cls.load(entry)

    @classmethod
    def get_pending_posts(cls, source: str | None = None):
        posts = cls.objects.filter(is_posted=False)
        if source:
            posts = posts.filter(source=source)
        return posts.all()

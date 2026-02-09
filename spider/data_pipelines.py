from abc import ABC
import uuid

from .extractors import Extractor
from .transformers import Transformer
from .senders import Sender
from .models import Post


class DataPipeline(ABC):
    def __init__(self, transformer: Transformer, extractor: Extractor, sender: Sender):
        self.transformer = transformer
        self.extractor = extractor
        self.sender = sender

    def execute(self):
        entries = self.extractor.extract()
        transformed_entries = self.transformer.bulk_transform(entries)
        Post.bulk_load(transformed_entries)
        pending_posts = Post.get_pending_posts()
        for post in pending_posts:
            self.sender.send(post)


class DataPipelineBuilder:
    def set_transformer(self, transformer: Transformer):
        self.transformer = transformer
        return self

    def set_extractor(self, extractor: Extractor):
        self.extractor = extractor
        return self

    def set_sender(self, sender: Sender):
        self.sender = sender
        return self

    def build(self) -> DataPipeline:
        return DataPipeline(
            transformer=self.transformer, extractor=self.extractor, sender=self.sender
        )

from django.core.management.base import BaseCommand, CommandError

from ...models import Post
from services.extractors import TheStandardExtractor, TheStarExtractor
from services.transformers import TheStandardTransformer, TheStarTransformer


class Command(BaseCommand):
    help = "Run spider"

    et_classes = [
        (TheStandardExtractor, TheStandardTransformer),
        (TheStarExtractor, TheStarTransformer),
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            action="store_true",
            help="Choose which mode to run in, either test or live",
        )

    def handle(self, *args, **options):
        self.stdout.write("Running spider")

        for extractor_cls, transformer_cls in self.et_classes:
            Post.set_extractor(extractor_cls)
            Post.set_transformer(transformer_cls)

            entries = Post.bulk_extract()
            transformed_entries = Post.bulk_transform(entries)

            Post.bulk_load(transformed_entries)

        for post in Post.objects.filter(is_sent=False).all():
            post.send()

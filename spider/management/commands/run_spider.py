from django.core.management.base import BaseCommand, CommandError

from ...models import Post
from lib.extractors import TheStandardExtractor, TheStarExtractor
from lib.transformers import TheStandardTransformer, TheStarTransformer


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

        pending_posts = Post.get_pending_posts()
        for post in pending_posts:
            post: Post
            post.to_telegram_post()

        for post in Post.objects.filter(is_sent=False).all():
            post.to_telegram_post()
            post.send()

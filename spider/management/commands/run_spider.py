from django.core.management.base import BaseCommand, CommandError

from ...models import Post
from ...services.extractors import TheStandardExtractor, TheStarExtractor
from ...services.transformers import TheStandardTransformer, TheStarTransformer
from ...services.senders import TelegramSender


class Command(BaseCommand):
    help = "Run spider"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            action="store_true",
            help="Choose which mode to run in, either test or live",
        )

    def handle(self, *args, **options):
        self.stdout.write("Running spider")

        # Standard sports
        standard_extractor = TheStandardExtractor(domain="sports")
        standard_transfomer = TheStandardTransformer()
        entries = standard_extractor.extract()
        transformed_entries = standard_transfomer.bulk_transform(entries)
        Post.bulk_load(transformed_entries)
        pending_posts = Post.get_pending_posts()
        sender = TelegramSender()
        for post in pending_posts:
            sender.send(post)

from django.core.management.base import BaseCommand, CommandError


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

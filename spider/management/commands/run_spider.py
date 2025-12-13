from django.core.management.base import BaseCommand, CommandError

from ...models import Post
from ...extractors import TheStandardExtractor, TheStarExtractor
from ...transformers import TheStandardTransformer, TheStarTransformer
from ...senders import TelegramSender
from ...data_pipelines import DataPipeline, DataPipelineBuilder


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
        pipe_lines: list[DataPipeline] = []

        standard_sports_extractor = TheStandardExtractor(domain="sports")
        standard_politics_extractor = TheStandardExtractor(domain="politics")

        star_sports_extractor = TheStarExtractor(domain="sports")
        star_politics_extractor = TheStarExtractor(doman="politics")

        standard_transfomer = TheStandardTransformer()
        star_transformer = TheStarTransformer()

        test_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.TEST_CHANNEL
        )
        politics_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.KENYAN_POLITICS
        )
        sports_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.SPORTS_KENYA
        )

        # sports
        pipe_line_builder = DataPipelineBuilder()
        pipe_line_builder.set_sender(sports_channel_sender)

        standard_sports_pipeline = (
            pipe_line_builder.set_extractor(standard_sports_extractor)
            .set_transformer(standard_transfomer)
            .build()
        )
        pipe_lines.append(standard_sports_pipeline)

        star_sports_pipeline = (
            pipe_line_builder.set_extractor(star_sports_extractor)
            .set_transformer(star_transformer)
            .build()
        )
        pipe_lines.append(star_sports_pipeline)

        # politics
        

        for pipe_line in pipe_lines:
            pipe_line.execute()

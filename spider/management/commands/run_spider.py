from django.core.management.base import BaseCommand

from ...extractors import Extractor, TheStandardExtractor
from ...transformers import TheStandardTransformer
from ...senders import TelegramSender
from ...data_pipelines import DataPipeline, DataPipelineBuilder


class Command(BaseCommand):
    help = "Run spider"

    def add_arguments(self, parser):
        parser.add_argument(
            "--live",
            action="store_true",
            help="Run in live env",
        )

        parser.add_argument(
            "--test",
            action="store_true",
            help="Run in test env",
        )

    def handle(self, *args, **options):
        self.stdout.write("Running spider")
        pipe_lines: list[DataPipeline] = []

        # Create extractors
        self.stdout.write("Creating transformers")
        standard_sports_ext = TheStandardExtractor(domain=Extractor.DOMAIN.SPORTS)
        standard_politics_ext = TheStandardExtractor(domain=Extractor.DOMAIN.POLITICS)

        # Create transformers
        self.stdout.write("Creating transformers")
        standard_transfomer = TheStandardTransformer()

        # Create senders
        self.stdout.write("Creating senders")
        test_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.TEST_CHANNEL
        )
        politics_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.KENYAN_POLITICS
        )
        sports_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.SPORTS_KENYA
        )

        if options["test"]:
            politics_channel_sender = test_channel_sender
            sports_channel_sender = test_channel_sender

        # sports
        standard_sports_pipeline = (
            DataPipelineBuilder()
            .set_extractor(standard_sports_ext)
            .set_transformer(standard_transfomer)
            .set_sender(sports_channel_sender)
            .build()
        )
        pipe_lines.append(standard_sports_pipeline)

        # politics
        standard_politics_pipeline = (
            DataPipelineBuilder()
            .set_extractor(standard_politics_ext)
            .set_transformer(standard_transfomer)
            .set_sender(politics_channel_sender)
            .build()
        )
        pipe_lines.append(standard_politics_pipeline)

        for pipe_line in pipe_lines:
            pipe_line.execute()

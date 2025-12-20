from django.core.management.base import BaseCommand, CommandError

from ...extractors import Extractor, TheStandardExtractor, TheStarExtractor
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
        # logger.error("hello world")
        pipe_lines: list[DataPipeline] = []

        # Create extractors
        self.stdout.write("Creating transformers")
        standard_sports_ext = TheStandardExtractor(domain=Extractor.DOMAIN.SPORTS)
        standard_politics_ext = TheStandardExtractor(domain=Extractor.DOMAIN.POLITICS)
        star_sports_ext = TheStarExtractor(domain=Extractor.DOMAIN.SPORTS)
        star_politics_ext = TheStarExtractor(domain=Extractor.DOMAIN.POLITICS)

        # Create transformers
        self.stdout.write("Creating transformers")
        standard_transfomer = TheStandardTransformer()
        star_transformer = TheStarTransformer()

        # Create senders
        self.stdout.write("Creating senders")
        test_channel_sender = TelegramSender(
            channel=TelegramSender.CHANNEL.TEST_CHANNEL
        )
        # politics_channel_sender = TelegramSender(
        #     channel=TelegramSender.CHANNEL.KENYAN_POLITICS
        # )
        # sports_channel_sender = TelegramSender(
        #     channel=TelegramSender.CHANNEL.SPORTS_KENYA
        # )

        # sports
        standard_sports_pipeline = (
            DataPipelineBuilder()
            .set_extractor(star_sports_ext)
            .set_transformer(star_transformer)
            .set_sender(test_channel_sender)
            .set_name("standard_sports_pipeline")
            .build()
        )
        pipe_lines.append(standard_sports_pipeline)

        star_sports_pipeline = (
            DataPipelineBuilder()
            .set_sender(test_channel_sender)
            .set_extractor(standard_sports_ext)
            .set_transformer(standard_transfomer)
            .set_name("star_sports_pipeline")
            .build()
        )
        pipe_lines.append(star_sports_pipeline)

        # politics
        standard_politics_pipeline = (
            DataPipelineBuilder()
            .set_extractor(standard_politics_ext)
            .set_transformer(standard_transfomer)
            .set_sender(test_channel_sender)
            .set_name("standard_politics_pipeline")
            .build()
        )
        pipe_lines.append(standard_politics_pipeline)

        star_politics_pipeline = (
            DataPipelineBuilder()
            .set_extractor(star_politics_ext)
            .set_transformer(star_transformer)
            .set_sender(test_channel_sender)
            .set_name("star_politics_pipeline")
            .build()
        )
        pipe_lines.append(star_politics_pipeline)

        for pipe_line in pipe_lines:
            self.stdout.write(f"Executing: {pipe_line}")
            pipe_line.execute()

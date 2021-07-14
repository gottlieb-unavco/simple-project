from django.core.management.base import BaseCommand
from kafka_example.kafka.consumer import ExampleConsumer
from logging import getLogger

LOGGER = getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the consumer'

    def handle(self, **options):
        consumer = ExampleConsumer()
        consumer.run()


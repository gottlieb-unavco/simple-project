import kafka_interface as kafka
import logging
from kafka_test.models import ExampleValue

LOGGER = logging.getLogger(__name__)


class ExampleConsumer(object):

    def consume(self, message):
        """
        Consume one message
        """
        LOGGER.debug("Message: %s", message)
        ExampleValue.objects.create(**(message.get('value')))

    def run(self):
        """
        Consume messages
        """
        topic = 'example'
        consumer = kafka.kafka_consumer(topic)

        while True:
            message = consumer.consume()
            self.consume(message)

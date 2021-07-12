import kafka_interface as kafka
import logging
from kafka_test.models import ExampleValue

LOGGER = logging.getLogger(__name__)


class ExampleConsumer(object):
    """
    Just consumes from the topic
    """

    def consume(self, message):
        """
        Consume one message
        """
        LOGGER.info("Message: %s", message)
        value = message.get('value', {})
        ExampleValue.objects.create(**value)

    def run(self):
        """
        Consume messages
        """
        topic = 'example'
        consumer = kafka.kafka_consumer(topic)
        LOGGER.info("Starting consumer")

        try:
            while True:
                message = consumer.consume()
                self.consume(message)
        except Exception as e:
            LOGGER.error("Failed with %s", e)
            raise

        

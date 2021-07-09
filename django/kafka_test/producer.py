import kafka_interface as kafka
import uuid
import datetime
import logging

LOGGER = logging.getLogger("producer")


def produce_example_message(value):
    """
    Produce one message
    """
    topic = 'example'
    producer = kafka.kafka_producer(topic)

    key = {
        'key': str(uuid.uuid4()),
    }
    message = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'value': value,
    }
    producer.produce(key, message)
    producer.flush()

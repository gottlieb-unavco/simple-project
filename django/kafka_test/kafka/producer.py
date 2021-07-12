import kafka_interface as kafka
import uuid
import datetime
import logging

LOGGER = logging.getLogger(__name__)


class ProducerSingleton:
    """
    Create just one producer
    """
    instance = None

    @classmethod
    def singleton(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = cls.create(*args, **kwargs)
        return cls.instance

    @classmethod
    def create(cls, topic):
        return kafka.kafka_producer(topic)


def produce_example_message(value):
    """
    Produce one message
    """
    topic = 'example'
    producer = ProducerSingleton.singleton(topic)

    key = {
        'key': str(uuid.uuid4()),
    }
    message = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'value': value,
    }
    producer.produce(key, message)
    producer.flush()

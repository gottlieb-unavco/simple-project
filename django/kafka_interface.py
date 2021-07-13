import sys, os, logging
import requests
import json
from confluent_kafka import SerializingProducer, DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.error import ValueDeserializationError, KeyDeserializationError

import avro.schema

LOGGER = logging.getLogger(__name__)

# Environment variables
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "broker:29092")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
AVRO_SCHEMAS_ROOT = os.getenv("AVRO_SCHEMAS_ROOT", "/avro_schemas")


class kafka_producer(object):
    """
    A kafka producer configured for a given topic
    """
    def __init__(self, topic, value_schema_file=False, key_schema_file=False):

        LOGGER.info("Initializing Producer")
        self.topic = topic

        schema_reg_config = {'url': SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_reg_config)

        # load value schema from file if specified, use default file name if not specified
        # last check registry for latest version
        if key_schema_file:
            self.key_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                key_schema_file,
            )
        else:
            self.key_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                "%s-key.avsc" % topic,
            )

        LOGGER.info("Reading key schema file: %s", self.key_schema_file)
        if os.path.exists(self.key_schema_file):
            with open(self.key_schema_file, "rb") as f:
                self.key_schema_str = str(avro.schema.parse(f.read()))
        else:
            LOGGER.info("No local key schema file, checking registry")
            key_schema_url = (
                SCHEMA_REGISTRY_URL + '/subjects/' + self.topic + '-key/versions/latest'
            )
            r = requests.get(key_schema_url)
            self.key_schema_str = json.dumps(r.json()['schema'])

        self.key_avro_serializer = AvroSerializer(
            schema_registry_client, self.key_schema_str
        )

        # load value schema from file if specified, use default file name if not specified
        # last check registry for latest version
        if value_schema_file:
            self.value_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                value_schema_file,
            )
        else:
            self.value_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                "%s-value.avsc" % topic,
            )

        LOGGER.info("Reading value schema file: %s", self.value_schema_file)
        if os.path.exists(self.value_schema_file):
            with open(self.value_schema_file, "rb") as f:
                self.value_schema_str = str(avro.schema.parse(f.read()))
        else:
            LOGGER.info("No local value schema file, checking registry")
            value_schema_url = (
                SCHEMA_REGISTRY_URL + '/subjects/' + self.topic + '-value/versions/latest'
            )
            r = requests.get(value_schema_url)
            self.value_schema_str = json.dumps(r.json()['schema'])

        self.value_avro_serializer = AvroSerializer(
            schema_registry_client, self.value_schema_str
        )

        producer_config = {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'key.serializer': self.key_avro_serializer,
            'value.serializer': self.value_avro_serializer,
            'linger.ms': 5,
            'enable.idempotence': True,
        }

        self.producer = SerializingProducer(producer_config)

    def produce(self, key, message):
        self.producer.produce(self.topic, key, message)

    def flush(self):
        self.producer.flush()

    def produce_and_flush(self, key, message):
        self.producer.produce(self.topic, key, message)
        self.producer.flush()


class kafka_consumer(object):
    """
    A kafka consumer configured for a given topic.
    """
    def __init__(self, topic, value_schema_file=False, key_schema_file=False, consumer_group=False):

        self.topic = topic

        schema_reg_config = {'url': SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_reg_config)

        # load key schema from file if specified, use default file name if not specified
        # last check registry for latest version
        if key_schema_file:
            self.key_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                key_schema_file,
            )
        else:
            self.key_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                "%s-key.avsc" % topic,
            )

        LOGGER.info("Reading key schema file: %s", self.key_schema_file)
        if os.path.exists(self.key_schema_file):
            with open(self.key_schema_file, "rb") as f:
                self.key_schema_str = str(avro.schema.parse(f.read()))
        else:
            LOGGER.info("No local key schema file, checking registry")
            key_schema_url = (
                SCHEMA_REGISTRY_URL + '/subjects/' + self.topic + '-key/versions/latest'
            )
            r = requests.get(key_schema_url)
            self.key_schema_str = r.json()['schema']

        self.key_avro_deserializer = AvroDeserializer(
            schema_registry_client, self.key_schema_str
        )

        # load value schema from file if specified, use default file name if not specified
        # last check registry for latest version
        if value_schema_file:
            self.value_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                value_schema_file,
            )
        else:
            self.value_schema_file = os.path.join(
                AVRO_SCHEMAS_ROOT,
                "%s-value.avsc" % topic,
            )

        LOGGER.info("Reading value schema file: %s", self.value_schema_file)
        if os.path.exists(self.value_schema_file):
            with open(self.value_schema_file, "rb") as f:
                self.value_schema_str = str(avro.schema.parse(f.read()))
        else:
            LOGGER.info("No local value schema file, checking registry")
            value_schema_url = (
                SCHEMA_REGISTRY_URL + '/subjects/' + self.topic + '-value/versions/latest'
            )
            r = requests.get(value_schema_url)
            self.value_schema_str = r.json()['schema']

        self.value_avro_deserializer = AvroDeserializer(
            schema_registry_client, self.value_schema_str
        )

        # use consumer group name if given, otherwise default to using topic name
        if consumer_group:
            self.consumer_group = consumer_group
        else:
            self.consumer_group = self.topic

        consumer_config = {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'key.deserializer': self.key_avro_deserializer,
            'group.id': self.consumer_group,
            'value.deserializer': self.value_avro_deserializer,
            'session.timeout.ms': 6000,
            'heartbeat.interval.ms': 2000,
            'auto.offset.reset': 'earliest',
        }

        self.consumer = DeserializingConsumer(consumer_config)
        self.consumer.subscribe([self.topic])
        LOGGER.info("Consumer subscribed to topic: %s", self.topic)
        LOGGER.info("Consumer group id: %s", self.consumer_group)

    def consume(self):
        while True:
            try:
                # poll for 1 second at a time
                poll = self.consumer.poll(1)
                if poll:
                    return {"offset": poll.offset(), "key": poll.key(), "value": poll.value()}
            except KeyDeserializationError:
                LOGGER.error('KeyDeserializationError')
                continue
            except ValueDeserializationError:
                LOGGER.error('ValueDeserializationError')
                continue
            except KeyboardInterrupt:
                LOGGER.error('Stopping via keyboardInterrupt')
                # sys.exit()
                raise

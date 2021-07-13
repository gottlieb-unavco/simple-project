import os
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
import logging

LOGGER = logging.getLogger(__name__)


BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "broker:29092")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
AVRO_SCHEMAS_ROOT = os.getenv("AVRO_SCHEMAS_ROOT", "/avro_schemas")


class AdminClientSingleton:
    """
    Create just one client
    """
    instance = None

    @classmethod
    def singleton(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = cls.create(*args, **kwargs)
        return cls.instance

    @classmethod
    def create(cls):
        return AdminClient({
            "bootstrap.servers": BOOTSTRAP_SERVERS,
        })


def get_admin_client():
    return AdminClientSingleton.singleton()


def topic_metadata(topic):
    """Checks if the given topic exists"""
    topics_metadata = get_admin_client().list_topics(timeout=5)
    for t in topics_metadata.topics.values():
        if t.topic == topic:
            print(repr(t))
    return False


def list_all_topics():
    """Lists all the available topics"""
    topic_metadata = get_admin_client().list_topics(timeout=5)
    for t in topic_metadata.topics.values():
        print(t.topic)


def create_topic(topic, partitions=1, replication=1):
    """Creates the topic with the given topic name"""

    futures = get_admin_client().create_topics(
        [
            NewTopic(
                topic=topic,
                num_partitions=partitions,
                replication_factor=replication,
                config={
                    "cleanup.policy": "delete",
                    "compression.type": "lz4",
                    "delete.retention.ms": "2000",
                    "file.delete.delay.ms": "2000",
                },
            )
        ]
    )

    for topic2, future in futures.items():
        try:
            future.result()
            print("Topic created")
        except Exception as e:
            print(f"failed to create topic {topic}: {e}")


def delete_topic(topic):
    """ Deletes the topic with a given name """
    print("Deleting topic: " + topic)
    get_admin_client().delete_topics([topic])


def describe_configs():
    print("Configs:")
    print(get_admin_client().describe_configs([
        ConfigResource(ConfigResource.Type.TOPIC, 'example'),
    ]))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Get schema string from schema registry')
    parser.add_argument("-t", "--topic", help="Topic of schema")
    parser.add_argument("-s", "--servers", help="Bootstrap_servers for kafka ")
    parser.add_argument("-d", "--delete",  action="store_true", help="Delete topic")
    parser.add_argument("-c", "--create",  action="store_true", help="Create topic")
    parser.add_argument("-p", "--partitions", help="When creating, add partitions to a topic")
    parser.add_argument("-r", "--replication", help="When creating, determine number of replications")

    args = parser.parse_args()

    if args.servers:
        BOOTSTRAP_SERVERS = args.servers

    if not args.topic:
        list_all_topics()
        describe_configs()
    elif args.delete:
        delete_topic(args.topic)
    elif args.create:
        if not args.partitions:
            args.partitions = 1
        if not args.replication:
            args.replication = 1
        create_topic(args.topic, partitions=int(args.partitions), replication=int(args.replication))
    else:
        topic_metadata(args.topic)

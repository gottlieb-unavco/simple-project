# simple-project

A simple development-oriented project

See [docs](docs/) for general documentation.

## Base Framework Components

These should provide a standardized environment compatible with the real deployment. There usually shouldn't be any local customization here.

### Kafka

The critical components of kafka: `router`, `zookeeper`, and `schema-registry`.

### Storage systems

Just `postgres` for now.

## Local Components

These are more like example code implementing some use cases.

### avro_schemas

Put AVRO schemas here.

### nginx

This is the web front end, it should mainly be used as a proxy for other services.

### django

A Python web application framework, includes WebSocket support
This can also be deployed as a Kafka topic consumer.


# simple-project

A simple development-oriented project skeleton

See [docs](docs/) for general documentation.

## Running in Docker Compose

From the root of this project run:

    docker compose up -d

## Base Framework Components

These attempt to provide a "standard" set of services matching the deployment environment. For the most part, all these components and configuration should be kept in sync.

### Kafka

The critical components of kafka: `router`, `zookeeper`, and `schema-registry`.

### Storage systems

Has `postgres` and `redis` but they aren't configured at all.

## Local Components

These are more like example code implementing some common use cases.

### avro_schemas

A shared area for AVRO schemas. Presumably the way these are shared will change over time, but this is a quick and simple way.

This path typically gets passed to components like:

    volumes:
      - ./avro_schemas:/avro_schemas:ro
    environment:
      - AVRO_SCHEMAS_ROOT=/avro_schemas

### nginx

This is the web front end, it should mainly be used as a proxy for other services.

### example_django

An example project implementing a basic data path -- collection, archiving, and distribution.
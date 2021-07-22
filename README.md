# es-simple-cluster

A multi-container cluster using docker-compose, including the basic services that are part of the EarthScope environment.

See [docs](docs/) for general documentation.

## Running in Docker Compose

From the root of this project run:

    docker compose up -d

See [Installation](docs/Installation.md) for more.

## Components

Ideally, every available service should be included here, but anything unrelated to a particular bit of work should usually be commented out for size and speed.

- **broker** (core)
  - Kafka broker
- **zookeeper** (core)
  - Kafka zookeeper
- **schema-registry** (core)
  - Kafka schema registry
- **nginx** (core)
  - external web interface
- **postgres**
  - postgres database
- **redis**
  - redis key/value store
- **prometheus**
  - metrics backend
- **grafana**
  - metrics front end

## Volumes

For the most part, you only need volumes when you want **persistent** data. In some cases, it will be easier to disconnect these.

- **web-static**
  - Static web content produced by Django, surfaced by nginx
- **kafka-data**
  - Data backend for the broker
  - _Disable_ to avoid kafka errors
- **postgres-data**
  - Storage for postgres
- **prometheus**
  - Storage for prometheus
- **grafana**
  - Storage for grafana

## /avro_schemas

For now, AVRO schemas are shared through a file mount.

This path typically gets passed to components like:

    volumes:
      - ./avro_schemas:/avro_schemas:ro
    environment:
      - AVRO_SCHEMAS_ROOT=/avro_schemas


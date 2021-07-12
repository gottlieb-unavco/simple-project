# About this project

This is intended to be a starting point for work on a container.

It contains a Kafka subsystem, nginx front end, and various storage layers.

Add/configure your container in `docker-compose.yml`. You can reference a built image or develop one locally (see [django]`).

## Installation

From the base directory, run

    docker compose up -d

Check that the web front-end is running at http://localhost:8888/

## Components

### Kafka stack

A minimal Confluent Kafka stack (`broker`, `zookeeper`, and `schema-registry`).

The [avro_schemas] subpath is mounted as `/avro_schemas` -- containers should use that.

### Web front end

An `nginx` server intended to operate as a proxy for other web-facing containers.

### Django server

For basic web applications.

### Storage layers

Postgres
# base-project

A base project for development, containing a docker-compose recipe and various components.

## Installation

From the base directory, run

    docker compose up -d

Check that the web front-end is running at http://localhost:8888/

## Components

### Kafka stack

A minimal Confluent Kafka stack (`broker`, `zookeeper`, and `schema-registry`).

Includes a path for storing AVRO schema definitions.

### Web front end

An `nginx` server intended to operate as a proxy for other web-facing containers.

### Django server

For basic web applications.

### Storage layers

TBD
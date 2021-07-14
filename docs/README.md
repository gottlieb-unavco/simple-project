# About this project

This is a Django system that implements an example "round-trip" app implementing 3 basic steps of our data path:

- **Collection** ![collection](django-collection.png)
  - HTTP and [WebSocket](WebSockets.md) interfaces
  - Data is put into a Kafka queue
- **Archive** ![archive](django-archive.png)
  - Picks up message from Kafka
  - Saves in a storage layer
- **Distribution** ![distribution](django-distribution.png)
  - Pulls data from the database
  - HTTP and [WebSocket](WebSockets.md) interfaces
  
## Components

- **Docker** : recipe for building the django image
- **kafka_example** : example application
- **www** : project definition
  - **www/settings.py** : main settings
  - **www/urls.py** : top-level routing table
- **requirements.txt** : python environment definition

This runs on a local sqlite3 database stored in the project root.

Static files are expected to be in `/django-static`.

## Running the local server

Install the dependencies (preferably in a dedicated environment):

    pip install -r requirements.txt

Set up the database:

    python manage.py migrate

Run the dev server:

    python manage.py runserver 0.0.0.0:8000

## Running in a container

After making a code change, run (from the main project directory):

    docker compose build
    docker compose up -d

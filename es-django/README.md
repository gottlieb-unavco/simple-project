# Django server

This is a Django server for doing web application work.

Test

## Overview

- __Docker__ : recipe for building the django image
- __kafka_example__ : example application
- __www__ : project definition
  - __www/settings.py__ : server settings
  - __www/urls.py__ : top-level routing table
- __requirements.txt__ : python environment definition

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


# Installation

Run `docker compose up -d` to bootstrap everything:

    % docker compose up -d
    [+] Building 2.0s (14/18)
    => [es-simple-project_django_archiver internal] load build definition from Dockerfile
    => => transferring dockerfile: 32B
    => [es-simple-project_django internal] load build definition from Dockerfile
    => => transferring dockerfile: 32B
    => [es-simple-project_django_archiver internal] load .dockerignore
    => => transferring context: 2B
    => [es-simple-project_django internal] load .dockerignore
    => => transferring context: 2B
    => [es-simple-project_django_archiver internal] load metadata for docker.io/library/python:3
    => [es-simple-project_django internal] load build context
    => => transferring context: 160.44kB
    => [es-simple-project_django_archiver 1/6] FROM docker.io/library/python:3@sha256:5992fd05009aa023212dddab8d588615d8002f8d752e6fdda259e409c393b
    => => resolve docker.io/library/python:3@sha256:5992fd05009aa023212dddab8d588615d8002f8d752e6fdda259e409c393b6ad
    => [es-simple-project_django_archiver internal] load build context
    => => transferring context: 160.44kB
    => CACHED [es-simple-project_django 2/6] WORKDIR /django
    => CACHED [es-simple-project_django 3/6] COPY requirements.txt .
    => CACHED [es-simple-project_django 4/6] RUN pip install -r requirements.txt
    => [es-simple-project_django 5/6] COPY . ./
    => [es-simple-project_django 6/6] RUN python manage.py migrate
    => [es-simple-project_django_archiver] exporting to image
    => => exporting layers
    => => writing image sha256:7e7b668559c9b971210db4e4d980c2795ff9c94a0a6372f20d8b01108a802cb5
    => => naming to docker.io/library/es-simple-project_django
    => => naming to docker.io/library/es-simple-project_django_archiver

    Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
    [+] Running 10/10
    ⠿ Network es-simple-project_default              Created
    ⠿ Volume "es-simple-project_kafka-data"          Created
    ⠿ Volume "es-simple-project_postgres-data"       Created
    ⠿ Container es-simple-project_django_1           Started
    ⠿ Container es-simple-project_zookeeper_1        Started
    ⠿ Container es-simple-project_postgres_1         Started
    ⠿ Container es-simple-project_nginx_1            Started
    ⠿ Container es-simple-project_broker_1           Started
    ⠿ Container es-simple-project_schema-registry_1  Started
    ⠿ Container es-simple-project_django_archiver_1  Started

Check http://localhost:8888/example/


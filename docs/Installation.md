# Installation

Run `docker compose up -d` to bootstrap everything:

It should finish with a launch report:

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

If everything works, you should be able to get to the example webapp at http://localhost:8080/example/.

If something goes wrong, you can also check:
- http://localhost:8080/ (the main nginx server)
- http://localhost:8888/ (a "safe" nginx server)
- http://localhost:9090/ (django server directly)

So for example if :8080 works but :9090 throws an error, then nginx is fine but django is down.

## Known issues

Especially when running the first time, there are many things that might need intervention.

- **nginx 404**
  - If you http://localhost:8200/example/ works but http://localhost:8080/example/ returns 404 errors, try restarting nginx
- **example-archiver**
  - It may fail with an error like "Subscribed topic not available: example: Broker: Unknown topic or partition"
  - You need to send a message (to get the type into the topic) then restart this part
- **broker**
  - Sometimes fails saying that the broker id is bad
  - Clear the `kafka-data` volume, or disconnect the broker from it

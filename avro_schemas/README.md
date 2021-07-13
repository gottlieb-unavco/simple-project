# AVRO Schemes

AVRO schemas can be put here and referenced from containers.

A typical docker-compose config would include:

```
    volumes:
      - ./avro_schemas:/avro_schemas:ro
    environment:
      - AVRO_SCHEMAS_ROOT=/avro_schemas
```

Then the application uses `$AVRO_SCHEMAS_ROOT` to find schemas.

## Naming convention

As implemented in the python libs, by default the schema is based on the topic it's used for, eg. the `example` topic uses:

- `example-key.avsc` for its key definition, and
- `example-value.avsc` for its value definition.


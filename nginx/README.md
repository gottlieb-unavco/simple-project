# nginx web server

Public-facing services should usually be proxied behind this, assuming they will be similarly proxied in production.

- __conf.d/default.conf__ runs on port 80 (8080 in the docker-compose), and proxies various other services
- __conf.d/gunicorn.conf__ is a super simple server running on port 8888, and should generally be left alone
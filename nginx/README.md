# nginx web server

Public-facing services should usually be proxied behind this, assuming they will be similarly proxied in production.

- __conf.d/default.conf__ is a super simple server running on port 8888, and should generally be left alone
- __conf.d/gunicorn.conf__ runs on port 80 (8080 in the docker-compose), and proxies a the gunicorn server at django:9090
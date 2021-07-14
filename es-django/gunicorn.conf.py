bind = "0.0.0.0:9090"
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'  # 'gevent'
threads = 4
loglevel = "debug"
# chdir = "/django"
wsgi_app = "www.asgi"
reload = True

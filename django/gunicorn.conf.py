bind = "0.0.0.0:9090"
workers = 4
worker_class = 'gevent'
threads = 4
loglevel = "debug"
# chdir = "/django"
wsgi_app = "www.wsgi"
reload = True

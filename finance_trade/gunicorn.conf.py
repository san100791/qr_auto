import os


WORKERS = int(os.getenv("WORKERS", "5"))
AUTO_RELOAD = os.getenv("AUTO_RELOAD", "0").lower() in ["1", "true"]


bind = "0.0.0.0:8080"
workers = WORKERS
reload = AUTO_RELOAD
user = "uwsgi"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(B)s bytes %(L)s secs'
limit_request_line = 8190
limit_request_field_size = 0
timeout = 60

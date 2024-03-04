# Gunicorn config variables
loglevel = "info"
errorlog = "stderr"
accesslog = "stdout"
worker_tmp_dir = "/tmp"
graceful_timeout = 120
timeout = 120
keepalive = 5
threads = 3
access_log_format = "{'remote_ip':'%(h)s','request_id':'%({X-Request-Id}i)s','response_code':'%(s)s','request_method':'%(m)s','request_path':'%(U)s','request_querystring':'%(q)s','request_timetaken':'%(D)s','response_length':'%(B)s'}"

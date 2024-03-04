#!/bin/bash
pkill -f gunicorn
export AUTHLIB_INSECURE_TRANSPORT=1
export PYTHONUNBUFFERED=TRUE
DEBUG=0 authbind  gunicorn --conf myapp/gunicorn.py myapp.wsgi:application --daemon --capture-output --log-level debug
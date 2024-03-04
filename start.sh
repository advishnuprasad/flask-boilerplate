#!/bin/bash
DEBUG=0 authbind  gunicorn --conf myapp/gunicorn.py myapp.wsgi:application --daemon
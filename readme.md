### Run locally ###
```
pyenv install 3.10.0
pyenv virtualenv 3.10.0 myapp-api-3.10.0
pyenv local myapp-api-3.10.0
pip install -r requirements.txt
pip install -e .
flask run
```

### Setup DB : Onetime###
```
docker-compose up
psql -h localhost -U postgres
Password: pwd

CREATE USER myapp with encrypted password 'pwd';
CREATE DATABASE myapp_dev;
GRANT ALL PRIVILEGES ON DATABASE myapp_dev to myapp;
```

### Flask alembic migration commands ###
```
flask db init
flask db migrate
flask db upgrade
flask init
```

```
DEBUG=0 authbind gunicorn -b 0.0.0.0:80  app.wsgi:application --daemon
```

### Run celery ###
```
celery -A myapp.celery worker --loglevel=info
```

### Run celery with  beat scheduler ###
```
celery -A myapp.celery worker -B --loglevel=info
```
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








https://www.talentlms.com/pages/docs/TalentLMS-API-Documentation.pdf
https://github.com/govex/talentpy/blob/master/talentpy/talentpy.py
https://github.com/ib1984/py-talentlms/blob/master/talentlms/talentlms.py
https://github.com/jhnferraris/talentlms-php-api
https://github.com/tylermercier/talentlms

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
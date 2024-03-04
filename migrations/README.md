### Flask alembic migration commands ###
```
flask db init
flask db migrate
flask db upgrade
flask init
```

### Postgres Setup ###
```
CREATE USER myapp with encrypted password 'pwd';
CREATE DATABASE myapp_dev;
GRANT ALL PRIVILEGES ON DATABASE myapp_dev to myapp;
```
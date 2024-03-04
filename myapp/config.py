"""Default configuration

Use env var to override
"""
import datetime
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = "dummy"
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or "sqlite:///app.db"
SQLALCHEMY_DATABASE_URI = (
    os.getenv("DATABASE_URI") or "postgresql://myapp:pwd@localhost:5432/myapp_dev"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL") or "redis://localhost:6379/2",
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL")
    or "redis://localhost:6379/2",
}

AWS_ACCESS_KEY_ID = "dummy"
AWS_SECRET_ACCESS_KEY = "dummy+oP7f3LySVKVa"

OAUTH2_REFRESH_TOKEN_GENERATOR = True
PORTAL_URL = os.getenv("PORTAL_URL") or "https://staging.myapp.in"

PASSWORD_POLICY = {
    "min_length": 8,
    "max_length": 20,
    "upper_case": True,
    "lower_case": True,
    "digit": True,
    "blacklist": ["Test@123", "Hello@123"],
}

"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from celery import Celery
from flask_authorize import Authorize
from flask_jwt_extended import JWTManager, get_current_user
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
authorize = Authorize(current_user=get_current_user)

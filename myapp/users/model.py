import json
import secrets
import uuid
from datetime import datetime, timedelta
from enum import Enum
from random import randint

from flask_authorize import AllowancesMixin, RestrictionsMixin
from sqlalchemy.ext.hybrid import hybrid_property

from myapp.extensions import db, pwd_context

UserGroup = db.Table(
    "user_group",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
)


UserRole = db.Table(
    "user_role",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    UNVERIFIED = "UNVERIFIED"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
    ARCHIVED = "ARCHIVED"
    INVITED = "INVITED"


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    lms_user_id = db.Column(db.Integer)
    otp = db.Column(db.Integer)
    otp_token = db.Column(db.String(32))
    verification_token = db.Column(db.String(1024))
    verification_token_valid_until = db.Column(db.DateTime())
    otp_valid_until = db.Column(db.DateTime())
    status = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(20))
    nationality = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    roles = db.relationship("Role", secondary=UserRole)
    groups = db.relationship("Group", secondary=UserGroup)

    @hybrid_property
    def password(self):
        return self._password

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def update_password(self, password: str):
        self._password = pwd_context.hash(password)

        self.clear_verification_token()

    def __repr__(self):
        return "<User %s>" % self.username

    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe()
        self.verification_token_valid_until = datetime.utcnow() + timedelta(weeks=10)

    @property
    def has_valid_verification_token(self):
        if self.verification_token_valid_until:
            return datetime.utcnow() < self.verification_token_valid_until

        return False

    def has_valid_otp(self):
        if self.otp_valid_until:
            return datetime.utcnow() < self.otp_valid_until

        return False

    def generate_otp(self):
        self.otp = randint(100000, 999999)

        self.otp_token = uuid.uuid4().hex
        self.otp_valid_until = datetime.utcnow() + timedelta(minutes=10)

    def is_unverified(self):
        return self.status == UserStatus.UNVERIFIED.value

    def is_active(self):
        return self.status == UserStatus.ACTIVE.value

    def mark_verified(self):
        self.activate()

    def clear_verification_token(self):
        self.verification_token = None
        self.verification_token_valid_until = None

    def activate(self):
        self.status = UserStatus.ACTIVE.value
        self.clear_verification_token()

    def authenticate(self, password: str):
        return pwd_context.verify(password, self.password)


class Group(db.Model, RestrictionsMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class UserDeviceToken(db.Model):
    """Basic device token model"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User")
    token = db.Column(db.String(255))
    device_info = db.Column(db.JSON())
    created_at = db.Column(db.DateTime())
    status = db.Column(db.String(15))

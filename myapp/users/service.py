from datetime import datetime

from marshmallow import ValidationError

from myapp import config
from myapp.commons.service import EmailService
from myapp.extensions import db

from .model import User, UserDeviceToken, UserStatus
from .util import PasswordHandler


class UserService:
    @classmethod
    def fetch(cls, q):
        if q:
            return (
                db.session.query(User)
                .filter(
                    User.first_name.ilike(f"%{q}%")
                    | User.last_name.ilike(f"%{q}%")
                    | User.email.ilike(f"%{q}%")
                    | User.username.ilike(f"%{q}%")
                )
                .order_by(User.id.desc())
            )
        else:
            return User.query.order_by(User.id.desc())

    @classmethod
    def create(cls, schema, data):
        user = User.query.filter(
            (User.email == data["email"])
            | (User.mobile_number == data["mobile_number"])
            | (User.username == data["username"])
        ).first()

        if not user:
            password_config = config.PASSWORD_POLICY
            valid_password, message = PasswordHandler(password_config).validate(
                data["password"]
            )

            if not valid_password:
                raise ValidationError(message)

            user = schema.load(data)
            user.status = UserStatus.UNVERIFIED.value
            user.generate_verification_token()

            db.session.add(user)
            db.session.commit()

            complete_registration_link = (
                f"{config.PORTAL_URL}/verify/{user.verification_token}"
            )
            EmailService.send_verification_mail(user.email, complete_registration_link)

            return user
        else:
            if User.query.filter_by(email=data["email"]).first():
                raise ValidationError("Email address already present")
            elif User.query.filter_by(mobile_number=data["mobile_number"]).first():
                raise ValidationError("Mobile number already taken")
            else:
                raise ValidationError("User name already taken")

    @classmethod
    def verify(cls, token):
        user = User.query.filter_by(verification_token=token).first()
        if user:
            user.activate()
            db.session.add(user)
            db.session.commit()
        else:
            raise ValidationError("Invalid or expired token")

    @classmethod
    def get(cls, user_id):
        return User.query.get_or_404(user_id)

    @classmethod
    def put(cls, schema, user_id, data):
        user = User.query.get_or_404(user_id)
        user = schema.load(data, instance=user)

        db.session.commit()

        return user

    @classmethod
    def delete(cls, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def generate_otp(cls, user):
        if not user.has_valid_otp():
            user.generate_otp()
            db.session.add(user)
            db.session.commit()

        EmailService.send_otp_mail(user.email, user.otp)

        return user.otp_token

    @classmethod
    def verify_otp(cls, token, otp):
        user = User.query.filter_by(otp_token=token).first()
        if user is not None and user.otp == otp:
            return user

        return None

    @classmethod
    def add_device_token(cls, user_id, device_info):
        token = device_info["token"]
        info = device_info["device_config"]

        device = UserDeviceToken(
            user_id=user_id,
            token=token,
            device_info=info,
            created_at=str(datetime.utcnow()),
            status="ACTIVE",
        )

        db.session.add(device)
        db.session.commit()

        return device

    @classmethod
    def initiate_reset_password(cls, email):
        user = User.query.filter_by(email=email).first()

        if user:
            user.generate_verification_token()
            db.session.add(user)
            db.session.commit()

            reset_link = f"{config.PORTAL_URL}/reset_password/{user.verification_token}"
            EmailService.send_reset_password_email(user.email, reset_link)

    @classmethod
    def verify_reset_token(cls, token):
        user = User.query.filter_by(verification_token=token).first()

        if user is None:
            raise ValidationError("Invalid token")

        if not user.has_valid_verification_token:
            raise ValidationError("Expired token")

    @classmethod
    def reset_my_password(cls, **kwargs):
        user = User.query.filter_by(verification_token=kwargs["token"]).first()

        if user is None:
            raise ValidationError("Invalid token")

        if user.has_valid_verification_token:
            password_config = config.PASSWORD_POLICY
            valid_password, message = PasswordHandler(password_config).validate(
                kwargs["new_password"]
            )

            if not valid_password:
                raise ValidationError(message)

            user.update_password(kwargs["new_password"])

            if user.is_unverified():
                user.mark_verified()

            db.session.add(user)
            db.session.commit()

        else:
            raise ValidationError("Invalid token")

    @classmethod
    def change_password(cls, user_id, **kwargs):

        user = User.query.get_or_404(user_id)

        if user is not None:
            # Call a factory method to authenticate user with given password
            valid = user.authenticate(kwargs["current_password"])

            password_config = config.PASSWORD_POLICY
            valid_password, message = PasswordHandler(password_config).validate(
                kwargs["new_password"]
            )

            if not valid_password:
                raise ValidationError(message)

            if valid:
                user.update_password(kwargs["new_password"])

                db.session.add(user)
                db.session.commit()
                return

        raise ValidationError("Invalid current password")

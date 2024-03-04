from myapp.extensions import db, ma
from myapp.users.model import User


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)


class BriefRoleSchema(ma.SQLAlchemyAutoSchema):
    name = ma.String()


class ShowUserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    roles = ma.Method("get_roles")

    def get_roles(self, user):
        roles = []
        for role in user.roles:
            roles.append(role.name)

        return roles

    class Meta:
        model = User
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = (
            "_password",
            "verification_token",
            "verification_token_valid_until",
            "otp",
            "otp_token",
            "active",
        )


class BriefUserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int()
    email = ma.String()
    first_name = ma.String()
    last_name = ma.String()


class SignupSchema(ma.SQLAlchemyAutoSchema):

    username = ma.String(required=True)
    email = ma.String(required=True)
    password = ma.String(required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    mobile_number = ma.String(required=True)
    gender = ma.String()
    date_of_birth = ma.String()
    nationality = ma.String()

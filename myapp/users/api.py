from authlib.integrations.flask_oauth2 import current_token
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from myapp.auth.oauth2 import require_oauth
from myapp.commons.pagination import paginate
from myapp.extensions import authorize

from .schema import ShowUserSchema, SignupSchema
from .service import UserService

users_api = Blueprint("users_api", __name__)


@users_api.route("/users", methods=["GET"])
@jwt_required()
@authorize.has_role("PORTAL_ADMIN")
def get_users():
    schema = ShowUserSchema(many=True)
    users = UserService.fetch(request.args.get("q", None))
    return paginate(users, schema)


@users_api.route("/users", methods=["POST"])
def create():
    data = request.json
    SignupSchema().load(data)
    schema = ShowUserSchema()
    user = UserService.create(schema, data)
    return (
        jsonify(
            msg="user created",
            user=schema.dump(user),
        ),
        201,
    )


@users_api.route("/users/verify/<token>", methods=["POST"])
def verify(token):
    UserService.verify(token)
    return (
        jsonify(
            msg="user verified",
        ),
        200,
    )


@users_api.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get(user_id):
    schema = ShowUserSchema()
    user = UserService.get(user_id)
    return (
        jsonify(
            user=schema.dump(user),
        ),
        200,
    )


@users_api.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def put(user_id):
    schema = ShowUserSchema(partial=True)
    user = UserService.put(schema, user_id, data=request.json)

    return (
        jsonify(
            msg="user updated",
            user=schema.dump(user),
        ),
        200,
    )


@users_api.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete(user_id):
    UserService.delete(user_id)

    return (
        jsonify(msg="user deleted"),
        204,
    )


# For SSO Users
@users_api.route("/users/current", methods=["GET"])
@require_oauth()
def current():
    user = current_token.user
    schema = ShowUserSchema()
    return (
        jsonify(schema.dump(user)),
        200,
    )


# For JWT Users
@users_api.route("/users/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = UserService.get(user_id)
    schema = ShowUserSchema()
    return (
        jsonify({"user": schema.dump(user)}),
        200,
    )


@users_api.route("/users/reset-password", methods=["POST"])
def initiate_reset_password():
    data = request.json

    UserService.initiate_reset_password(data.get("email"))
    return (
        jsonify(msg="success"),
        200,
    )


@users_api.route("/users/verify-reset-token/<string:token>", methods=["GET"])
def verify_reset_token(token):

    UserService.verify_reset_token(token)
    return (
        jsonify(msg="success"),
        200,
    )


@users_api.route("/users/reset-password/<string:token>", methods=["POST"])
def reset_password(token):
    data = request.json

    command = {"new_password": data.get("new_password"), "token": token}

    UserService.reset_my_password(**command)
    return (
        jsonify(msg="success"),
        204,
    )


@users_api.route("/users/me/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    data = request.json
    user_id = get_jwt_identity()

    UserService.change_password(user_id, **data)
    return (
        jsonify(msg="success"),
        200,
    )


@users_api.route("/users/me/register_token", methods=["POST"])
@jwt_required()
def add_device_token():
    data = request.json
    user_id = get_jwt_identity()
    UserService.add_device_token(user_id, data)
    return "", 202


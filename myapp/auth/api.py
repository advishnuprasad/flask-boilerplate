import logging

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, render_template, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from myapp.auth.helpers import (
    add_token_to_database,
    is_token_revoked,
    revoke_token,
    verify_client_info,
)
from myapp.extensions import jwt, pwd_context
from myapp.users.model import User
from myapp.users.service import UserService

from .oauth2 import authorization

logger = logging.getLogger("app")

auth_api = Blueprint("auth", __name__, url_prefix="/auth")


def current_user():
    user_id = get_jwt_identity()
    return User.query.get_or_404(user_id)


@auth_api.route("/login", methods=["POST"])
def login():
    """Authenticate user and return tokens"""

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter(
        (User.email == username) | (User.username == username)
    ).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Invalid username or password"}), 400

    if user is not None and not user.is_active():
        return jsonify({"msg": "Please verify your email to login"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}

    return jsonify(ret), 200


@auth_api.route("/verify_password", methods=["POST"])
def verify_password():
    """Authenticate user and return tokens"""
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter(
        (User.email == username) | (User.username == username)
    ).first()

    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Invalid username or password"}), 400

    if user is not None and not user.is_active():
        return jsonify({"msg": "Please verify your email to login"}), 400

    token = UserService.generate_otp(user)

    return jsonify({"token": token}), 200


@auth_api.route("/login_with_otp", methods=["POST"])
def login_with_otp():
    token = request.json.get("token", None)
    otp = request.json.get("otp", None)
    user = UserService.verify_otp(token, otp)

    if user is None:
        return jsonify({"msg": "Wrong Token"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    return jsonify(ret), 200


@auth_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token"""
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), 200


@auth_api.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token"""
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@auth_api.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout"""
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@auth_api.route("/sso/authorize", methods=["POST"])
def authorize_sso():
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    client_id = request.form.get("client_id", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), 400

    if not verify_client_info(client_id):
        return jsonify({"error": "invalid_client"}), 400

    return authorization.create_authorization_response(grant_user=user)


@auth_api.route("/sso/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@auth_api.route("/sso/login", methods=["GET"])
def identify_auth():
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    scope = request.args.get("scope")
    response_type = request.args.get("response_type")
    state = request.args.get("state")

    # return jsonify(ret), 200
    return render_template(
        "login.html",
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        response_type=response_type,
        state=state,
    )

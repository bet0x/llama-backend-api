import bcrypt
from flask import jsonify

from app.models.database_models import User
from app.models.request_models import SignupRequest, LoginRequest, LogoutRequest
from app.models.response_models import SignupResponse, ErrorResponse, LoginResponse, LogoutResponse
from app.repository.user_repository import save_user, get_user_by_email
from app.services.token_service import generate_token, invalidate_token


def login(request: LoginRequest):

    print('Received login request:', request)
    email: str = request.email
    password: str = request.password

    print("going to fetch user by email:", email)
    user: User = get_user_by_email(email)
    print("user fetched:", user)

    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        error_resp = ErrorResponse(message="Invalid credentials", status=401)
        return jsonify(error_resp.__dict__), error_resp.status

    auth_token = generate_token(user)
    resp = LoginResponse(user_id=user.user_id.__str__(), auth_token=auth_token, name=user.name.__str__())
    return jsonify(resp.__dict__), 200


def register(request: SignupRequest):
    request.password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    user = User(name=request.name, email=request.email, password=request.password)
    insert_result = save_user(user)

    if not insert_result[0]:
        error_resp = ErrorResponse(message=insert_result[1], status=insert_result[2])
        return jsonify(error_resp.__dict__), error_resp.status
    else:
        resp = SignupResponse(user_id=insert_result[1], message="User registered successfully", status=201)
        return jsonify(resp.__dict__), resp.status


def logout(request: LogoutRequest):
    result = invalidate_token(request.user_id, request.auth_token)
    resp = LogoutResponse(
        message="Logged out successfully" if result else "Logout failed",
        status=200 if result else 401)
    return jsonify(resp.__dict__), resp.status


def forgot_password():
    return

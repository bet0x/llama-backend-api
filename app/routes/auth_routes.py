from flask import Blueprint, request

from app.middlewares.auth_request_middlewares import auth_requests_middleware
from app.models.request_models import LoginRequest, SignupRequest, LogoutRequest
from app.services import auth_service

auth_routes = Blueprint('auth_routes', __name__)

auth_routes.before_request(auth_requests_middleware)


@auth_routes.route('/auth/register', methods=['POST'])
def register():
    print("req landed on register route")
    req: SignupRequest = request.signupRequest
    resp = auth_service.register(req)
    print(resp)
    return resp


@auth_routes.route('/auth/login', methods=['POST'])
def login():
    req: LoginRequest = request.loginRequest
    return auth_service.login(req)


@auth_routes.route('/auth/logout', methods=['POST'])
def logout():
    req: LogoutRequest = request.logoutRequest
    return auth_service.logout(req)


@auth_routes.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    return auth_service.forgot_password()

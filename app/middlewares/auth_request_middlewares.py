from flask import request, abort

from app.models.request_models import LoginRequest, SignupRequest, LogoutRequest


def auth_requests_middleware():
    url_called = request.url_rule.__str__().strip()

    if url_called == "/auth/register":
        _signup_request_middleware()
    elif url_called == "/auth/login":
        _login_request_middleware()
    elif url_called == "/auth/logout":
        _logout_request_middleware()
    elif url_called == "/auth/forgot-password":
        _forgot_password_request_middleware()
    else:
        abort(404, "Requested endpoint  '" + request.url + "' not found")


def _signup_request_middleware():
    _content_type_check()
    request_body = _get_request_body()

    req = SignupRequest(**request_body)
    validation_result = req.validate()

    if validation_result[0] is False:
        abort(400, validation_result[1])

    request.signupRequest = req


def _login_request_middleware():
    _content_type_check()
    request_body = _get_request_body()

    req = LoginRequest(**request_body)
    validation_result = req.validate()

    if validation_result[0] is False:
        abort(400, validation_result[1])

    request.loginRequest = req


def _logout_request_middleware():
    _content_type_check()
    request_body = _get_request_body()

    req = LogoutRequest(**request_body)
    validation_result = req.validate()

    if validation_result[0] is False:
        abort(400, validation_result[1])

    request.logoutRequest = req


def _forgot_password_request_middleware():
    _content_type_check()


def _content_type_check():
    content_type = request.content_type
    if "application/json" not in content_type:
        abort(400,
              "Invalid Content-Type" if content_type is None else "Content-Type '" + content_type + "' not supported")


def _get_request_body():
    request_body = request.get_json(force=True)
    if not request_body:
        abort(400, "Invalid request body")
    return request_body

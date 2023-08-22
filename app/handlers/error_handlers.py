from flask import jsonify
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from app.models.response_models import ErrorResponse


def bad_request(error):
    if isinstance(error, BadRequest):
        error_json = jsonify(ErrorResponse(message=error.description, status=400).__dict__)
    else:
        error_json = jsonify(ErrorResponse(message=str(error), status=400).__dict__)
    return error_json, 400


def not_found(error):
    if isinstance(error, NotFound):
        error_json = jsonify(ErrorResponse(message=error.description, status=404).__dict__)
    else:
        error_json = jsonify(ErrorResponse(message="Requested resource not found", status=404).__dict__)
    return error_json, 404


def internal_server_error(error):
    error_json = jsonify(ErrorResponse(message="Internal server error", status=500).__dict__)
    return error_json, 500

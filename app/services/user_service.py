from flask import jsonify

from app.models.database_models import User
from app.models.response_models import ErrorResponse
from app.repository.user_repository import get_user_by_id
from app.logger import get_logger


logger = get_logger(__name__)


def get_user_profile(user_id: str):
    if user_id is None or user_id == '':
        error_resp = ErrorResponse(message='Please provide user id', status=400)
        return jsonify(error_resp.__dict__), error_resp.status

    user: User = get_user_by_id(user_id)
    print("user is: ", user)
    logger.info(f"user is:: {user}")

    if user is None:
        error_resp = ErrorResponse(message='User not found with id: ' + user_id, status=404)
        return jsonify(error_resp.__dict__), error_resp.status

    return jsonify(user.__repr__()), 200

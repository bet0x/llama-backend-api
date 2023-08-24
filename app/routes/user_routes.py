from flask import Blueprint, request

from app.middlewares.profile_request_middlewares import profile_requests_middleware
from app.services import user_service
from app.logger import get_logger


logger = get_logger(__name__)

user_routes = Blueprint('user_routes', __name__)

user_routes.before_request(profile_requests_middleware)


@user_routes.route('/user/profile', methods=['GET'])
def user_profile():
    user_id = request.args.get('user_id')
    return user_service.get_user_profile(user_id)

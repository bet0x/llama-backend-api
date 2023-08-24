from flask import Blueprint

from app.services import avatar_service

avatar_routes = Blueprint('avatar_routes', __name__)


@avatar_routes.route('/bots', methods=['GET'])
def get_avatars():
    return avatar_service.get_avatars()

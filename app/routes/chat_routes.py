from flask import Blueprint, request

from app.middlewares.chat_request_middlewares import chat_request_middlewares
from app.models.database_models import ChatMessage
from app.services import chat_service

chat_routes = Blueprint('chat_routes', __name__)

chat_routes.before_request(chat_request_middlewares)


@chat_routes.route('/chat', methods=['POST'])
def chat():
    chat_message: ChatMessage = getattr(request, "chat_message")
    print(f"chat message --> {chat_message}")
    return chat_service.chat(chat_message)


@chat_routes.route('/chat/history', methods=['GET'])
def chat_history():
    return chat_service.chat_history(request.args)


@chat_routes.route('/chat/session-history', methods=['GET'])
def session_history():
    bot_id = request.args.get("bot_id", None)
    user_id = request.args.get("user_id", None)
    session_id = request.args.get("session_id", None)
    return chat_service.chat_session_history(bot_id, user_id, session_id)


@chat_routes.route('/chat', methods=['DELETE'])
def delete_chat():
    request.args.get("bot_id", None)
    return chat_service.delete_chat("None", "None")


@chat_routes.route('/upload-image', methods=['POST'])
def upload_image():
    return chat_service.upload_image()


@chat_routes.route('/download', methods=['GET'])
def download():
    return chat_service.download()

from flask import request, abort

from app.models.database_models import ChatMessage


def chat_request_middlewares():
    url_called = request.url_rule.__str__().strip()

    if url_called == "/chat":
        _chat_request_middleware()
    elif url_called.startswith("/chat/history"):
        _chat_history_middleware()


def _chat_request_middleware():
    if request.method != "POST":
        return
    _content_type_check()
    request_body = _get_request_body()
    req = ChatMessage(**request_body)

    validation_result = req.validate()

    if validation_result[0] is False:
        abort(400, validation_result[1])

    request.__setattr__("chat_message", req)


def _chat_history_middleware():
    print("chat_history_middleware")


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

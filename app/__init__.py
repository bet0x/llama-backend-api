from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.handlers.cors_handler import cors_handler
from app.handlers.error_handlers import not_found, internal_server_error, bad_request
from app.logger import __init__ as init_logger
from app.processing import profile
from app.repository import __init__ as db_init
from app.routes.auth_routes import auth_routes
from app.routes.avatar_routes import avatar_routes
from app.routes.chat_routes import chat_routes
from app.routes.user_routes import user_routes
from app.vector_database import vector_db

load_dotenv()
init_logger()
app = Flask(__name__)
CORS(app)
db_init()

app.before_request(cors_handler)

app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(avatar_routes)
app.register_blueprint(chat_routes)

app.register_error_handler(400, bad_request)
app.register_error_handler(404, not_found)
app.register_error_handler(500, internal_server_error)

vector_db.upload_bot_profile_dir("", 97832)


@app.route("/ping", methods=["GET"])
def index():
    return "PONG"

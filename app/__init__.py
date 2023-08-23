from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant

from app.handlers.cors_handler import cors_handler
from app.handlers.error_handlers import not_found, internal_server_error, bad_request
from app.processing import profile
from app.repository import __init__ as db_init
from app.routes.auth_routes import auth_routes
from app.routes.avatar_routes import avatar_routes
from app.routes.chat_routes import chat_routes
from app.routes.user_routes import user_routes
from app.vector_database import vector_db

load_dotenv()
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

# vector_db.upload_bot_profile_dir("", 101)
# qdarnt = profile.load_profiles()

embeddings = OpenAIEmbeddings()


def load_sentences_from_files():
    loader = TextLoader("/data/vikas/Profile/life/Profile.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs


docs = load_sentences_from_files()

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    path="/tmp/docs",
    collection_name="Profile",
)

load_sentences_from_files()


@app.route("/ping", methods=["GET"])
def index():
    return "PONG"

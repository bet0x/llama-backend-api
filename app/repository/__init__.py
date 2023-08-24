import os

import pymongo

user_collection_name = "users"
chat_history_collection_name = "chat_history"
chat_message_collection_name = "chat_messages"


def __init__():
    db = pymongo.MongoClient(os.environ.get("MONGO_URI")).get_database("llama_ai")
    existing_collections = db.list_collection_names()
    print("Existing collections:", existing_collections)
    init_users_collection(db, existing_collections)
    init_chat_history_collection(db, existing_collections)
    init_chat_message_collection(db, existing_collections)


def init_users_collection(db, existing_collections):
    print("initializing collection:", user_collection_name)
    if user_collection_name not in existing_collections:
        print("Creating collection", user_collection_name)
        user_collection = db.create_collection(user_collection_name)
        user_collection.create_index("email", unique=True)


def init_chat_history_collection(db, existing_collections):
    print("initializing collection:", chat_history_collection_name)
    if chat_history_collection_name not in existing_collections:
        print("Creating collection", chat_history_collection_name)
        chat_history_collection = db.create_collection(chat_history_collection_name)
        chat_history_collection.create_index("bot_id")
        chat_history_collection.create_index("user_id")


def init_chat_message_collection(db, existing_collections):
    print("initializing collection:", chat_message_collection_name)
    if chat_history_collection_name not in existing_collections:
        print("Creating collection", chat_message_collection_name)
        chat_history_collection = db.create_collection(chat_message_collection_name)
        chat_history_collection.create_index("bot_id")
        chat_history_collection.create_index("user_id")
        chat_history_collection.create_index("session_id")

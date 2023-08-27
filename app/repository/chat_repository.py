import os

import pymongo
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult
from app.logger import get_logger
from app.models.database_models import ChatMessage
from app.repository.__init__ import chat_history_collection_name, chat_message_collection_name

mongodb = pymongo.MongoClient(os.environ.get("MONGO_URI")).get_database("llama_docker")
chat_history_collection = mongodb.get_collection(chat_history_collection_name)
chat_message_collection = mongodb.get_collection(chat_message_collection_name)

logger = get_logger(__name__)


def save_chat_message(chat_message: ChatMessage):
    try:
        insert_result: InsertOneResult = chat_message_collection.insert_one(chat_message.__dict__)
        return True, str(insert_result.inserted_id)
    except Exception as e:
        print(e)
        return False, e.__dict__


def get_chat_history_by_bot_id_and_user_id(bot_id: str, user_id: str, limit: int = 10, offset: int = 0):
    try:
        chat_filter = {"bot_id": bot_id, "user_id": user_id, "is_deleted": False}
        chat_messages_cursor: Cursor[ChatMessage] = chat_message_collection.find(filter=chat_filter).sort("timestamp",
                                                                                                          pymongo.DESCENDING).limit(
            limit)
        chat_messages = []

        for message in list(chat_messages_cursor):
            message.pop("_id")
            message.pop("is_deleted")
            chat_messages.append(message)

        return chat_messages
    except Exception as e:
        print(e)
        return None


def get_chat_history_by_bot_id_and_user_id_timestamp(bot_id: str, user_id: str, limit: int = 10, timestamp: int = None,
                                                     mode: str = "before"):
    try:
        chat_filter = {"bot_id": bot_id, "user_id": user_id, "is_deleted": False}

        if timestamp:
            if mode == "before":
                chat_filter["timestamp"] = {"$lt": timestamp}
            elif mode == "after":
                chat_filter["timestamp"] = {"$gt": timestamp}
            else:
                raise ValueError("Invalid mode provided. Expected 'before' or 'after'.")

        chat_messages_cursor: Cursor[ChatMessage] = chat_message_collection.find(filter=chat_filter).sort("timestamp",
                                                                                                          pymongo.DESCENDING).limit(
            limit)
        chat_messages = []

        for message in list(chat_messages_cursor):
            message.pop("_id")
            message.pop("is_deleted")
            chat_messages.append(message)

        return chat_messages
    except Exception as e:
        print(e)
        return None


def get_session_chat_history(bot_id: str, user_id: str, session_id: str):
    try:
        chat_filter = {"bot_id": bot_id, "user_id": user_id, "session_id": session_id, "is_deleted": False}
        chat_messages_cursor: Cursor[ChatMessage] = chat_message_collection.find(filter=chat_filter).sort("timestamp",
                                                                                                          pymongo.DESCENDING)
        chat_messages = []

        for message in list(chat_messages_cursor):
            message.pop("_id")
            message.pop("is_deleted")
            chat_messages.append(message)

        return chat_messages
    except Exception as e:
        print(e)
        return None


def delete_chat_history(bot_id: str, user_id: str):
    try:
        chats_filter = {"bot_id": bot_id, "user_id": user_id}
        result = chat_message_collection.update_many(filter=chats_filter, update={"$set": {"is_deleted": True}})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(e)
        return False

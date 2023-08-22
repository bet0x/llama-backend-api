import os

import pymongo
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.models.database_models import User
from app.repository.__init__ import user_collection_name
from app.utils.mongo_utils import extract_duplicate_key_value_from_exception

mongodb = pymongo.MongoClient(os.environ.get("MONGO_URI")).get_database("llama_ai")
user_collection = mongodb.get_collection(user_collection_name)


def save_user(user: User):
    try:
        result = user_collection.insert_one(user.__dict__())
        return result.acknowledged, str(result.inserted_id), 201
    except Exception as e:
        if isinstance(e, DuplicateKeyError):
            key, value = extract_duplicate_key_value_from_exception(e)
            return False, key + " '" + value + "' already registered", 409
        return False, "Internal Server Error", 500


def get_user_by_email(email: str):
    try:
        user = user_collection.find_one({"email": email})

        if user is None:
            return None

        return User(
            name=user.get("name"),
            email=user.get("email"),
            password=user.get("password"),
            deleted=user.get("deleted"),
            created_at=user.get("created_at"),
            user_id=user.get("_id")
        )
    except Exception as e:
        print(e)
        return None


def get_user_by_id(user_id: str):
    try:
        _id = ObjectId(user_id)
        user = user_collection.find_one({"_id": _id})

        if user is None:
            return None

        return User(
            name=user.get("name"),
            email=user.get("email"),
            password=user.get("password"),
            deleted=user.get("deleted"),
            created_at=user.get("created_at"),
            user_id=user.get("_id")
        )
    except Exception as e:
        print(e)
        return None

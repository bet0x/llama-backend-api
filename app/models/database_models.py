from datetime import datetime


class User:
    def __init__(self, name: str, email: str, password: bytes, deleted=False, user_id=None,
                 created_at=(int(datetime.now().timestamp()) * 1000)):
        self.name: str = name
        self.email: str = email
        self.password: bytes = password
        self.deleted = deleted
        self.created_at = created_at
        self.user_id = user_id

    def __dict__(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "deleted": self.deleted,
            "created_at": self.created_at
        }

    def __repr__(self):
        return {
            "user_id": str(self.user_id),
            "name": self.name,
            "email": self.email,
            "deleted": self.deleted,
            "created_at": self.created_at
        }

    def __str__(self):
        return f"User(user_id={str(self.user_id)}, name={self.name}, email={self.email}, created_at={self.created_at}, deleted={self.deleted})"


from datetime import datetime

class ChatMessage:
    def __init__(self, message=None, user_id=None, bot_id="9327", session_id=None, is_user_message=True, query_type=None,
                 is_deleted=False, name="Pixy"):
        self.message = message
        self.user_id = user_id
        self.bot_id = bot_id
        self.query_type = query_type
        self.session_id = session_id
        self.is_user_message = is_user_message
        self.is_deleted = is_deleted
        self.timestamp = (int(datetime.now().timestamp()) * 1000)

        # Assign the name based on the value of is_user_message
        if self.is_user_message:
            self.name = name  # User's name
        else:
            self.name = self.get_bot_name()

    def get_bot_name(self):
        # Check the bot_id and return the respective name
        bot_names = {
            "9327": "Pixy",
            "9328": "Bruce",
            "9329": "CVM Expert"
        }
        return bot_names.get(self.bot_id, "Unknown Bot")

    def validate(self):
        if self.query_type is None or self.query_type == "":
            return False, "query_type cannot be empty"
        if self.query_type == "message" and (self.message is None or self.message == ""):
            return False, "message cannot be empty"
        if self.user_id is None or self.user_id == "":
            return False, "user_id cannot be empty"
        if self.bot_id is None or self.bot_id == "":
            return False, "bot_id cannot be empty"
        if not self.is_user_message and self.bot_id not in ["9327", "9328", "9329"]:
            return False, "The bot does not exist"
        if self.session_id is None or self.session_id == "":
            return False, "session_id cannot be empty"
        return True, "OK"

    def __str__(self):
        return f"ChatMessage(message={self.message}, user_id={self.user_id}, bot_id={self.bot_id}, timestamp={self.timestamp})"



# commented ChatMessage
# class ChatMessage:
#     def __init__(self, message=None, user_id=None, bot_id="97832", session_id=None, is_user_message=True, query_type=None,
#                  is_deleted=False, name="Pixy"):
#         self.message = message
#         self.user_id = user_id
#         self.bot_id = bot_id
#         self.name = name
#         self.query_type = query_type
#         self.session_id = session_id
#         self.is_user_message = is_user_message
#         self.is_deleted = is_deleted
#         self.timestamp = (int(datetime.now().timestamp()) * 1000)

#     def validate(self):
#         if self.query_type is None or self.query_type == "":
#             return False, "query_type cannot be empty"
#         if self.query_type == "message" and self.message is None or self.message == "":
#             return False, "message cannot be empty"
#         if self.user_id is None or self.user_id == "":
#             return False, "user_id cannot be empty"
#         if self.bot_id is None or self.bot_id == "":
#             return False, "bot_id cannot be empty"
#         if self.session_id is None or self.session_id == "":
#             return False, "session_id cannot be empty"
#         return True, "OK"

#     def __str__(self):
#         return f"ChatMessage(message={self.message}, user_id={self.user_id}, bot_id={self.bot_id}, timestamp={self.timestamp})"


class ChatHistory:
    def __init__(self, user_id, bot_id, messages=None, history_id=None):
        self.user_id = user_id
        self.bot_id = bot_id
        self.messages = messages if messages else []
        self.history_id = history_id
        self.created_at = int(datetime.now().timestamp()) * 1000

    def add_message(self, message, is_user_message):
        self.messages.append({"message": message, "is_user_message": is_user_message, "timestamp": self.created_at})

    def __str__(self):
        return f"ChatHistory(user_id={self.user_id}, bot_id={self.bot_id}, messages={self.messages}, history_id={self.history_id}, created_at={self.created_at})"

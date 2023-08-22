from datetime import datetime


class LoginRequest:
    def __init__(self, email="", password=""):
        self.email: str = email
        self.password: str = password

    def validate(self):
        if not self.email or self.email == "":
            return False, "Email is required"
        if not self.password or self.password == "":
            return False, "Password is required"
        return True, "Validation successful"

    def __str__(self):
        return "Email: " + self.email + ", Password: " + str(self.password)


class SignupRequest:
    def __init__(self, name=None, password=None, email=None):
        self.name: str = name
        self.password: str = password
        self.email: str = email

    def __str__(self):
        return "Name: " + self.name + ", Email: " + self.email + ", Password: " + str(self.password)

    def validate(self):
        if not self.name or self.name == "":
            return False, "Name is required"
        if not self.password or self.password == "":
            return False, "Password is required"
        if not self.email or self.email == "":
            return False, "Email is required"
        return True, "Validation successful"


class LogoutRequest:
    def __init__(self, user_id="", auth_token=""):
        self.user_id: str = user_id
        self.auth_token: str = auth_token

    def __str__(self):
        return "User ID: " + self.user_id + ", Auth Token: " + self.auth_token

    def validate(self):
        if not self.user_id or self.user_id == "":
            return False, "user_id is required"
        if not self.auth_token or self.auth_token == "":
            return False, "auth_token is required"
        return True, "Validation successful"


class Chat:
    def __init__(self, bot_id: str = "", user_id: str = "", message: str = ""):
        self.bot_id: str = bot_id
        self.user_id: str = user_id
        self.message: str = message
        self.timestamp = (int(datetime.now().timestamp()) * 1000)

class LoginResponse:
    def __init__(self, auth_token: str, user_id: str):
        self.auth_token: str = auth_token
        self.user_id: str = user_id


class SignupResponse:
    def __init__(self, user_id: str, message: str, status: int):
        self.user_id: str = user_id
        self.message: str = message
        self.status: int = status

    def __str__(self):
        return "User id: " + self.user_id + " message: " + self.message + " status: " + self.status


class LogoutResponse:
    def __init__(self, message: str, status: int):
        self.message: str = message
        self.status: int = status


class ErrorResponse:
    def __init__(self, message: str, status: int):
        self.message: str = message
        self.status: int = status

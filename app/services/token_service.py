import uuid

from app.models.database_models import User

generated_tokens = {}


def generate_token(user: User):
    token = uuid.uuid4().__str__()
    generated_tokens[token] = user.user_id.__str__()
    return token


def get_details_from_token(auth_token: str):
    for token, data in generated_tokens.items():
        if token == auth_token:
            return data
    return None


def invalidate_token(user_id: str, auth_token: str):
    result = generated_tokens.pop(auth_token, None)
    return result == user_id

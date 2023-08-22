from pymongo.errors import DuplicateKeyError


def extract_duplicate_key_value_from_exception(e: DuplicateKeyError):
    kv = e.details.get("keyValue")

    if isinstance(kv, dict):
        for key, value in kv.items():
            return key, value
    else:
        return None, None

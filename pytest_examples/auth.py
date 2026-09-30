"""Fake authentication, used by test_data_driven_parametrize.py."""

USERS = {"alice": "correct_pw", "bob": "secret"}


def validate_credentials(username: str, password: str) -> int:
    if not username or not password:
        return 400
    if USERS.get(username) == password:
        return 200
    return 401

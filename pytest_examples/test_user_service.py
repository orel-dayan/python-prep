"""Fixtures: dependency injection, fixture that uses another fixture, yield.

Run: pytest test_user_service.py -v
"""

import pytest


class UserService:
    def __init__(self, storage: dict):
        self._storage = storage

    def create_user(self, username: str, email: str) -> dict:
        if username in self._storage:
            raise ValueError(f"Username '{username}' is already taken")
        user = {"username": username, "email": email, "active": True}
        self._storage[username] = user
        return user

    def get_user(self, username: str) -> dict | None:
        return self._storage.get(username)

    def deactivate_user(self, username: str) -> None:
        if username not in self._storage:
            raise KeyError(f"User '{username}' not found")
        self._storage[username]["active"] = False


@pytest.fixture
def user_service():
    # Function scope (default): every test gets a brand new storage
    return UserService(storage={})


@pytest.fixture
def user_service_with_existing_user(user_service):
    # A fixture can request another fixture
    user_service.create_user(username="alice", email="alice@example.com")
    yield user_service
    # Code after yield is teardown: it runs after the test, even if it failed


def test_create_user_succeeds(user_service):
    new_user = user_service.create_user(username="bob", email="bob@example.com")
    assert new_user["username"] == "bob"
    assert new_user["active"] is True


def test_create_duplicate_user_raises_error(user_service_with_existing_user):
    with pytest.raises(ValueError, match="already taken"):
        user_service_with_existing_user.create_user(
            username="alice", email="alice2@example.com"
        )


def test_deactivate_user_sets_active_to_false(user_service_with_existing_user):
    user_service_with_existing_user.deactivate_user(username="alice")
    alice = user_service_with_existing_user.get_user(username="alice")
    assert alice["active"] is False


def test_deactivate_nonexistent_user_raises_key_error(user_service):
    with pytest.raises(KeyError):
        user_service.deactivate_user(username="ghost_user")

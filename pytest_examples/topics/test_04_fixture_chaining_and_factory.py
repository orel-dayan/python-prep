"""
Topic: fixture chaining + factory fixtures

Chaining: a fixture can request other fixtures as parameters, so setup
builds up in layers instead of one fixture doing everything.

Factory: instead of returning one fixed value, a fixture can return a
function the test calls multiple times with different arguments.

Run:
    python -m pytest pytest_examples/topics/test_04_fixture_chaining_and_factory.py -v

Example run:
    2 tests should PASS.
"""
import pytest


# --- chaining ---
@pytest.fixture
def db_connection():
    return {"connected": True}


@pytest.fixture
def user_repo(db_connection):
    return {"db": db_connection, "users": ["orel"]}


def test_find_user(user_repo):
    assert "orel" in user_repo["users"]


# --- factory ---
@pytest.fixture
def make_user():
    def _make_user(name="default", age=30):
        return {"name": name, "age": age}
    return _make_user


def test_user_creation(make_user):
    user = make_user(name="Orel")
    assert user["name"] == "Orel"

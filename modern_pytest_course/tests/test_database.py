import pytest
from app.database import FakeDatabase

# Apply database marker to all tests in this module
pytestmark = pytest.mark.database


@pytest.fixture(scope="module")
def db():
    return FakeDatabase()


def test_database_is_not_empty(db):
    assert db.user_count() == 3


def test_user_1_exists(db):
    assert db.get_user(1) == "Alice"


def test_user_3_exists(db):
    assert db.get_user(3) == "Charlie"


def test_unknown_user_returns_none(db):
    assert db.get_user(999) is None

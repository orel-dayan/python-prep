import secrets
from pathlib import Path

import pytest
from app.file_db import FakeFileDatabase


@pytest.fixture(scope="module")
def db():
    # create file in same folder as this test file
    file_path = Path(__file__).parent / f"{secrets.token_hex(4)}.json"
    db = FakeFileDatabase(file_path)
    
    yield db 
    
    print("Cleaning up fake file database...")
    
    if file_path.exists():
        file_path.unlink()


def test_get_existing_user(db):
    assert db.get_user("1") == "Alice"


def test_unknown_user_returns_none(db):
    assert db.get_user("999") is None

"""Shared fixtures. Every test in this folder can use them without import."""

import pytest


@pytest.fixture(autouse=True)
def set_environment(monkeypatch):
    # autouse: applied to every test in this folder, even if not requested
    monkeypatch.setenv("APP_ENV", "testing")


@pytest.fixture(scope="session")
def db_config():
    # Session scope is OK here: this data is never modified by the tests
    return {
        "host": "localhost",
        "port": 5432,
        "database": "testdb",
        "user": "test_user",
    }


@pytest.fixture(params=["sqlite", "postgres", "mysql"], ids=["sqlite", "pg", "mysql"])
def db_type(request):
    # A parametrized fixture: every test that uses it runs once per param
    return request.param

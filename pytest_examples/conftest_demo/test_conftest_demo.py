"""Uses the fixtures from conftest.py in the same folder.

Run: pytest conftest_demo -v
"""

import os


def test_autouse_fixture_sets_env_var():
    # Note: this test does not request set_environment, autouse did it
    assert os.environ["APP_ENV"] == "testing"


def test_db_config_from_conftest(db_config):
    assert db_config["port"] == 5432


def test_db_connection(db_type):
    # Runs 3 times: sqlite, pg, mysql
    assert db_type in ["sqlite", "postgres", "mysql"]

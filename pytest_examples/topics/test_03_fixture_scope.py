"""
Topic: fixture scope

Scope controls how often a fixture is (re)created: `function` (default),
`class`, `module`, `package`, or `session`. A `module`-scoped fixture is
created once and shared by every test in this file.

Run:
    python -m pytest pytest_examples/topics/test_03_fixture_scope.py -v -s

Example run:
    2 tests should PASS. With -s, "[setup] creating config once for the
    whole module" prints only ONCE, even though two tests use the fixture.
"""
import pytest


@pytest.fixture(scope="module")
def shared_config():
    print("\n[setup] creating config once for the whole module")
    return {"env": "test"}


def test_config_a(shared_config):
    assert shared_config["env"] == "test"


def test_config_b(shared_config):
    # Same dict object as in test_config_a - the fixture only ran once.
    assert shared_config["env"] == "test"

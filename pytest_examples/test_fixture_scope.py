"""The SAFE way to handle mutable data and session scope.

The broken version (that fails on purpose) is in traps/trap_shared_state.py.
Run: pytest test_fixture_scope.py -v --setup-show
"""

from types import MappingProxyType

import pytest


@pytest.fixture
def user_ids():
    # Function scope: a fresh list for every test, no leaking between tests
    return [1, 2, 3]


@pytest.fixture(scope="session")
def _user_ids_template():
    # Session scope is fine for IMMUTABLE data (a tuple cannot be changed)
    return (1, 2, 3)


@pytest.fixture
def user_ids_from_template(_user_ids_template):
    # Expensive data cached once, but every test gets its own mutable copy
    return list(_user_ids_template)


@pytest.fixture(scope="session")
def settings():
    # Read-only mapping: any attempt to change it raises TypeError
    return MappingProxyType({"db_host": "localhost", "retries": 3})


def test_first_test_mutates_its_own_copy(user_ids):
    user_ids.append(4)
    assert len(user_ids) == 4


def test_second_test_still_sees_three(user_ids):
    # Passes in any order, because the previous test changed a different list
    assert len(user_ids) == 3


def test_copy_from_session_template(user_ids_from_template):
    user_ids_from_template.append(99)
    assert user_ids_from_template == [1, 2, 3, 99]


def test_template_was_not_changed(user_ids_from_template):
    assert user_ids_from_template == [1, 2, 3]


def test_session_settings_are_read_only(settings):
    with pytest.raises(TypeError):
        settings["retries"] = 5

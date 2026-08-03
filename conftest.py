"""
Shared fixtures and pytest configuration for the whole test suite.
Fixtures defined here are available to every test file in this directory
and below, without needing to import them.
"""
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False,
        help="run tests marked as slow"
    )


def pytest_collection_modifyitems(config, items):
    # By default, skip tests marked @pytest.mark.slow unless --runslow is passed.
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def client():
    # Example of a project-wide fixture, e.g. a fake API client.
    class FakeClient:
        def get(self, path):
            return {"status_code": 200, "path": path}
    return FakeClient()

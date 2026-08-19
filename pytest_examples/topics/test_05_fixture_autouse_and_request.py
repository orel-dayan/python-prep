"""
Topic: `autouse` fixtures + the built-in `request` fixture

`autouse=True` makes a fixture run for every test in its scope automatically,
without any test needing to name it as a parameter.

The `request` fixture gives a fixture access to metadata about the currently
running test, e.g. its name and markers - used here to log the test name and
detect the `@pytest.mark.slow` marker.

Run:
    python -m pytest pytest_examples/topics/test_05_fixture_autouse_and_request.py -v -s

Example run:
    test_resource_fast PASSes; test_resource_slow is SKIPPED by default (the
    repo root conftest.py auto-skips @pytest.mark.slow tests unless
    --runslow is passed - add it to see "This is a slow test" print). With
    -s you'll see "[setup] starting test" / "[teardown] finished test"
    printed around every test that does run.
"""
import pytest


@pytest.fixture(autouse=True)
def log_test_boundaries():
    print("\n[setup] starting test")
    yield
    print("[teardown] finished test")


@pytest.fixture
def resource(request):
    print(f"Running: {request.node.name}")
    marker = request.node.get_closest_marker("slow")
    if marker:
        print("This is a slow test")
    yield "data"


def test_resource_fast(resource):
    assert resource == "data"


@pytest.mark.slow
def test_resource_slow(resource):
    assert resource == "data"

"""
Topic: `parametrize(..., indirect=True)`

Normally parametrize passes a raw value straight to the test. With
`indirect=True`, the value is passed through a fixture first (the fixture
receives it via `request.param`) - useful when the "parameter" needs setup
logic before the test can use it.

Run:
    python -m pytest pytest_examples/topics/test_08_parametrize_indirect.py -v

Example run:
    3 tests should PASS, shown as test_sized_list[3], test_sized_list[5],
    test_sized_list[10].
"""
import pytest


@pytest.fixture
def sized_list(request):
    size = request.param
    return list(range(size))


@pytest.mark.parametrize("sized_list", [3, 5, 10], indirect=True)
def test_sized_list(sized_list):
    assert len(sized_list) in (3, 5, 10)

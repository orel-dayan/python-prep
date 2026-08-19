"""
Topic: `@pytest.fixture(params=...)` — a parametrized fixture

Different from topic 07 (`@pytest.mark.parametrize` on the test itself) and
topic 08 (`indirect=True`, one test opting a fixture into one specific
parameter list). Here the fixture is parametrized directly: EVERY test that
requests it runs once per param value, with no `@pytest.mark.parametrize`
on any of them.

Run:
    python -m pytest pytest_examples/topics/test_16_fixture_params.py -v

Example run:
    6 tests total: test_len_matches_param and test_is_list, each running once
    per param (3, 5, 10) - 3 + 3 = 6, with no parametrize decorator in sight.
"""
import pytest


@pytest.fixture(params=[3, 5, 10])
def sized_list(request):
    return list(range(request.param))


def test_len_matches_param(sized_list):
    assert len(sized_list) in (3, 5, 10)


def test_is_list(sized_list):
    assert isinstance(sized_list, list)

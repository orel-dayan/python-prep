"""skip, skipif, xfail and custom markers.

Run: pytest test_marks_demo.py -v
     pytest test_marks_demo.py -v -m "not slow"
"""

import sys
import time

import pytest


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    raise AssertionError("never runs")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python_version_dependent():
    assert sys.version_info >= (3, 8)


@pytest.mark.xfail(reason="Bug #123: discount rounding off by 1 cent")
def test_known_bug():
    # Expected to fail. If it ever passes, pytest reports XPASS.
    assert 1 + 1 == 3


@pytest.mark.slow
def test_heavy_computation():
    time.sleep(1)
    assert sum(range(1000)) == 499500


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Needs 3.9")
@pytest.mark.slow
def test_combined():
    # Two marks on one test: skipif and slow
    pass

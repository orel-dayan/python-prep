"""
Topic: pytest-cov — measuring which lines your tests actually exercise

A test suite that passes doesn't mean every line ran. `classify()` below has
an error branch this file's single test never triggers; coverage makes that
visible instead of leaving it to be found by an incident.

Run:
    python -m pytest pytest_examples/topics/test_19_coverage_pytest_cov.py \
        --cov=test_19_coverage_pytest_cov --cov-report=term-missing

(the --cov target is the bare module name, not a dotted package path -
pytest_examples/topics has no __init__.py, so pytest imports this file as a
top-level module named test_19_coverage_pytest_cov, not a package member)

Example run:
    1 test PASSES. The coverage table shows this file at 83%, with the
    "Missing" column pointing at line 25, the `raise ValueError` - proof
    that line never ran during the test.

Other useful flags:
    --cov-report=html          writes an interactive htmlcov/index.html
    --cov-fail-under=90        exit non-zero if total coverage drops below 90%
"""


def classify(n: int) -> str:
    if n < 0:
        raise ValueError("negative numbers are not classifiable")  # never hit below
    return "even" if n % 2 == 0 else "odd"


def test_classify_positive_even():
    assert classify(4) == "even"

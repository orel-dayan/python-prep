"""
Topic: class-based tests with setup_method / teardown_method

Grouping related tests in a class (no `__init__`, methods start with
`test_`) shares structure. `setup_method`/`teardown_method` run before/after
EACH test method in the class (roughly equivalent to a function-scoped
fixture applied to every method).

Run:
    python -m pytest pytest_examples/topics/test_14_class_based_tests.py -v

Example run:
    2 tests should PASS: TestCalculator::test_add, TestCalculator::test_subtract.
"""


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def teardown_method(self):
        self.calc = None

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(5, 2) == 3

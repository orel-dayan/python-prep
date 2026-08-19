"""
Topic: Failure (F) vs Error (E)

- Failure: an `assert` inside the test evaluated to False. Test logic ran;
  the result was wrong.
- Error: an unexpected exception occurred outside of an assertion (e.g. a
  bug/typo, or a fixture that raised). Pytest reports it separately (E vs F
  in the short summary) so you can tell "my code is wrong" apart from
  "my test/fixture setup is broken".

Run:
    python -m pytest pytest_examples/topics/test_15_failure_vs_error.py -v

Example run:
    Both tests PASS as written. Change `add(1, 1) == 2` to `== 3` to see an
    "F"; uncomment `1 / 0` in the second test to see an "E" instead.
"""


def add(a, b):
    return a + b


def test_this_is_a_failure_example():
    # An assert that does not hold is reported as "F".
    # Flip to add(1, 1) == 3 to see a real failure.
    assert add(1, 1) == 2


def test_this_is_an_error_example():
    # An unexpected exception is reported as "E", not "F".
    # Uncomment the line below to see it in action:
    # result = 1 / 0
    assert True

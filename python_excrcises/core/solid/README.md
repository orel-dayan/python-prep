# SOLID Principles

Each of the five SOLID principles as its own runnable file: a BAD example that
violates the principle, followed by the GOOD version that fixes it.

## Files

| File | Principle |
|---|---|
| `single_responsibility.py` | S — a class should have one reason to change |
| `open_closed.py` | O — open for extension, closed for modification |
| `liskov_substitution.py` | L — a subclass must honor its parent's contract |
| `interface_segregation.py` | I — many small interfaces beat one big one |
| `dependency_inversion.py` | D — depend on an abstraction, not a concrete class |

## Running

```bash
python core/solid/single_responsibility.py
```

Dependency inversion is also the principle that makes code testable: if a
function is hard to unit test, that is usually a design problem, not a
testing problem (see `../../pytest_examples/PYTEST_TUTORIAL.md` section 8 —
mocking works best when the code under test already depends on an
abstraction, not a concrete implementation it constructs itself).

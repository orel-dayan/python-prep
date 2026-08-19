# test_fixtures_examples.py

import pytest

# -----------------------------------------------------------------------------
# 1. By Scope
# -----------------------------------------------------------------------------

# 1.1 function (default) — Runs once per test function
@pytest.fixture
def function_fixture():
    """Function-scoped (default) fixture."""
    return "function"

# 1.2 class — Runs once per TestClass, shared by all methods in that class
@pytest.fixture(scope="class")
def class_fixture():
    """Class-scoped fixture."""
    print("→ setup class_fixture")
    yield "class"
    print("→ teardown class_fixture")

# 1.3 module — Runs once per test file (module)
@pytest.fixture(scope="module")
def module_fixture():
    """Module-scoped fixture."""
    return "module"

# 1.4 package — Runs once per package (dir with __init__.py)
@pytest.fixture(scope="package")
def package_fixture():
    """Package-scoped fixture."""
    return "package"

# 1.5 session — Runs once for the entire test session
@pytest.fixture(scope="session")
def session_fixture():
    """Session-scoped fixture."""
    return "session"

def test_function_scope(function_fixture):
    assert function_fixture == "function"

class TestClassScope:
    def test_class_scope_1(self, class_fixture):
        assert class_fixture == "class"

    def test_class_scope_2(self, class_fixture):
        assert class_fixture == "class"

def test_module_scope(module_fixture):
    assert module_fixture == "module"

def test_package_scope(package_fixture):
    assert package_fixture == "package"

def test_session_scope(session_fixture):
    assert session_fixture == "session"


# -----------------------------------------------------------------------------
# 2. By Usage
# -----------------------------------------------------------------------------

# 2.1 Explicit — You opt in by naming the fixture in your test signature
def test_explicit(function_fixture):
    """Explicitly requests function_fixture."""
    assert function_fixture == "function"

# 2.2 Autouse — Runs for every test (in its scope) without naming it
@pytest.fixture(autouse=True)
def autouse_fixture():
    """Autouse fixture: setup → yield → teardown for every test."""
    print("\n[autouse setup]")
    yield
    print("\n[autouse teardown]")

def test_autouse_effect():
    """autouse_fixture ran before and after this test automatically."""
    assert True


# -----------------------------------------------------------------------------
# 3. Parameterized Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture(params=[("a", 1), ("b", 2), ("c", 3)])
def param_fixture(request):
    """Runs the test three times with different params."""
    return request.param

def test_parametrized(param_fixture):
    key, val = param_fixture
    assert isinstance(key, str) and isinstance(val, int)


# -----------------------------------------------------------------------------
# 4. Setup/Teardown Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def setup_teardown_fixture():
    """Setup before yield; teardown after."""
    # --- setup code ---
    resource = {"status": "initialized"}
    yield resource
    # --- teardown code ---
    resource["status"] = "teardown"

def test_setup_teardown(setup_teardown_fixture):
    assert setup_teardown_fixture["status"] == "initialized"
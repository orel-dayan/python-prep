import pytest
from result_store import ResultStore


@pytest.fixture(scope="function")
def store(tmp_path):
    print("SETUP\n")
    path = tmp_path / "results.json"
    store_obj = ResultStore(path)
    store_obj.open()
    yield store_obj
    store_obj.close()
    
@pytest.fixture
def populated_store(store):
    store.add_result("test_1", True)
    store.add_result("test_2", False)
    store.add_result("test_3", True)
    return store
    
import pytest
from result_store import ResultStore


@pytest.mark.parametrize("passed", [True, False])
def test_add_and_get_result(store, passed):
    store.add_result("test_login", passed)
    assert store.get_result("test_login") is passed
    
def test_count_is_zero_for_new_store(store):
    assert store.count() == 0
    
def test_count_increases_with_results(store):
    store.add_result("test_1",False)
    store.add_result("test_2",True)
    assert store.count() == 2
    
def test_get_result_raises_on_unknown_name(store):
    with pytest.raises(KeyError):
        store.get_result("non_existing_test")
    
def test_pass_rate_with_mixed_results(populated_store):
    assert populated_store.pass_rate() == pytest.approx(2/3, rel=1e-2)
    
def test_count_of_populated_store(populated_store):
    assert populated_store.count() == 3
    
# def test_pass_rate_of_empty_store(store):
#     # Add a check for empty store pass rate
#     # This should raise a ZeroDivisionError since there are no results to calculate the pass rate.
#     with pytest.raises(ZeroDivisionError):
#         store.pass_rate()

@pytest.mark.xfail(reason="BUG-01: pass_rate leaks ZeroDivisionError on empty store")
def test_pass_rate_on_empty_store_returns_zero(store):
    assert store.pass_rate() == 0.0
        
def test_add_result_raises_when_store_is_closed(tmp_path):
    path = tmp_path / "results.json"
    store = ResultStore(path)
    store.open()
    store.close()
    
    with pytest.raises(RuntimeError):
        store.add_result("test_closed", True)
        

@pytest.mark.xfail(reason="BUG-02: count does not require an open store")
def test_count_raises_after_close(store):
    store.close()
    with pytest.raises(RuntimeError):
        store.count()
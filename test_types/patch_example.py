from unittest.mock import patch
from xmlrpc import client

def do_work():
    pass
# 1. Context manager - explicit scope
def test_something():
    with patch("my_module.time.sleep") as mock_sleep:
        do_work()
    assert mock_sleep.call_count == 3


# 2. Decorator - the mock arrives as a parameter
@patch("my_module.time.sleep")
def test_something(mock_sleep):
    do_work()
    assert mock_sleep.call_count == 3


# 3. patch.object - when you have the object itself
with patch.object(client, "connect") as mock_connect:
    do_work()
    assert mock_connect.call_count == 3
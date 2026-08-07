class SerialTransport:
    def __enter__(self):
        self._port.open()
        return self                     # this is what 'as' binds to

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._port.close()              # runs even on exception
        return False                    # False = do not swallow the exception
    
from contextlib import contextmanager
from sqlite3 import connect

@contextmanager
def open_device(ip: str):
    conn = connect(ip)
    try:
        yield conn                      # everything before yield is setup
    finally:
        conn.close()                    # finally guarantees teardown
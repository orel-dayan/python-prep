import sys

import pytest
from app.http_status import get_status_message


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only feature")
def test_windows_registry_access():
    import winreg

    key = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    assert key is not None


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="match statement requires Python 3.10+"
)
def test_404_is_not_found():
    assert get_status_message(404) == "Not Found"

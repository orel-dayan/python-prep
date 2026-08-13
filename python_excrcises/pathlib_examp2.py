import os
import tempfile
from pathlib import Path


def get_data_dir(app_name: str) -> Path:
    """Return the per-user data directory for this app."""
    if os.name == "nt":
        base = Path(os.environ["LOCALAPPDATA"])
    else:
        # XDG spec on Linux, with a sane fallback
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    path = base / app_name
    path.mkdir(parents=True, exist_ok=True)
    return path


PROJECT_ROOT = Path(__file__).resolve().parent
TEMP_ROOT = Path(tempfile.gettempdir())

import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as td:
    work = Path(td)
    (work / "data.txt").write_text("hello", encoding="utf-8")

    print((work / "data.txt").exists())   # True
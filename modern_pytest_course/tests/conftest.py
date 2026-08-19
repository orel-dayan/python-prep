import sys
from pathlib import Path

# Make `app` importable regardless of where pytest is invoked from (repo root or this folder).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

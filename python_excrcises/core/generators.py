"""Generator function vs. generator expression.

A generator produces values one at a time instead of building a full list in
memory — useful for large or streamed data (log files, API pages).
"""

from collections.abc import Iterator
from pathlib import Path


def read_error_lines(path: Path) -> Iterator[str]:
    """Yield ERROR lines from a log file, one at a time (generator function)."""
    with path.open(encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()


def count_errors(path: Path) -> int:
    """Same idea as a generator expression, fed straight into sum()."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if "ERROR" in line)


if __name__ == "__main__":
    log = Path(__file__).with_name("_sample.log")
    log.write_text("INFO ok\nERROR disk full\nERROR timeout\nINFO done\n", encoding="utf-8")

    try:
        for line in read_error_lines(log):
            print(line)
        print("total errors:", count_errors(log))
    finally:
        log.unlink()

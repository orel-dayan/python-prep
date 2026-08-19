"""logging with two handlers at different levels — console gets INFO+,
the file gets everything, which is the usual split for a CLI tool.
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_file: Path, verbose: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()  # avoid duplicate handlers if called more than once

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))

    root.addHandler(file_handler)
    root.addHandler(console_handler)


if __name__ == "__main__":
    log_file = Path(__file__).with_name("_sample.log")
    setup_logging(log_file, verbose=True)

    logger = logging.getLogger(__name__)
    logger.debug("debug goes to the file only")
    logger.info("info goes to both")

    try:
        _ = 1 / 0
    except ZeroDivisionError:
        logger.exception("full traceback goes to the file")

    for handler in logging.getLogger().handlers:
        handler.close()  # release the file lock before cleanup, esp. on Windows
    log_file.unlink()

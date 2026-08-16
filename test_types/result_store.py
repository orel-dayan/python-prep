"""Stores test results in a JSON file."""

import json


class ResultStore:
    def __init__(self, path):
        self.path = path
        self._results = {}
        self._is_open = False

    def open(self):
        """Load existing results from disk, or start empty."""
        if self.path.exists():
            self._results = json.loads(self.path.read_text())
        self._is_open = True

    def close(self):
        """Write results to disk and mark the store as closed."""
        self.path.write_text(json.dumps(self._results))
        self._is_open = False

    def add_result(self, name, passed):
        """Record a single test result."""
        if not self._is_open:
            raise RuntimeError("store is not open")
        self._results[name] = passed

    def get_result(self, name):
        """Return the recorded result for a test name."""
        if not self._is_open:
            raise RuntimeError("store is not open")
        if name not in self._results:
            raise KeyError(name)
        return self._results[name]

    def count(self):
        """Return the number of recorded results."""
        return len(self._results)

    def pass_rate(self):
        """Return the fraction of results that passed."""
        # if not self._results:
        #     raise ZeroDivisionError("No results to calculate pass rate")
        return sum(self._results.values()) / len(self._results)
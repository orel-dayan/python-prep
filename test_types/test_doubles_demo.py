"""
Self-contained demo: Mock vs Stub vs Fake vs Simulator.
Everything needed is defined in this file, so it runs as-is.

Run:  python test_doubles_demo.py
"""

from enum import Enum
from unittest.mock import Mock

# ---------------------------------------------------------------------------
# The REAL production code we want to test: a gate controller.
# It depends on a "database" object that has a .query(tag_id) method.
# ---------------------------------------------------------------------------

class GateController:
    """Decides what to do when a tag is swiped, based on the DB answer."""

    def __init__(self, database):
        self.database = database

    def handle_tag(self, tag_id):
        answer = self.database.query(tag_id)
        if answer == "found":
            return "GATE_OPEN"
        return "ALARM"


# ===========================================================================
# 1. MOCK — canned answers + verifies it was called correctly
# ===========================================================================

def demo_mock():
    print("== MOCK ==")

    # Authorized tag
    mock_db = Mock()
    mock_db.query.return_value = "found"          # canned response
    controller = GateController(database=mock_db)

    result = controller.handle_tag("12345")
    assert result == "GATE_OPEN", result
    # Mock's extra power: verify the DB was called correctly
    mock_db.query.assert_called_once_with("12345")

    # Unauthorized tag
    mock_db2 = Mock()
    mock_db2.query.return_value = "not_found"
    controller2 = GateController(database=mock_db2)

    result2 = controller2.handle_tag("99999")
    assert result2 == "ALARM", result2
    mock_db2.query.assert_called_once_with("99999")

    print("  authorized -> GATE_OPEN, unauthorized -> ALARM, calls verified. OK")


# ===========================================================================
# 2. STUB — canned answers only, NO verification
# ===========================================================================

class StubDatabase:
    """Always returns the same answer. Ignores the actual id."""

    def query(self, tag_id):
        return "found"


def demo_stub():
    print("== STUB ==")

    stub_db = StubDatabase()
    controller = GateController(database=stub_db)

    result = controller.handle_tag("12345")
    assert result == "GATE_OPEN", result
    # Note: we do NOT check whether query() was called.
    # A stub only feeds data into the test — that's the difference from a mock.

    print("  stub always returns 'found' -> GATE_OPEN. OK")


# ===========================================================================
# 3. FAKE — real working logic, just simplified (in-memory instead of SQL)
# ===========================================================================

class FakeDatabase:
    """An in-memory DB. Real lookup logic, no network or disk."""

    def __init__(self):
        self._employees = set()

    def add_employee(self, tag_id):
        self._employees.add(tag_id)

    def query(self, tag_id):
        # Actually checks — real logic, unlike a stub or mock
        return "found" if tag_id in self._employees else "not_found"


def demo_fake():
    print("== FAKE ==")

    fake_db = FakeDatabase()
    fake_db.add_employee("12345")                 # set up real data

    controller = GateController(database=fake_db)

    # This really searches the in-memory store
    assert controller.handle_tag("12345") == "GATE_OPEN"
    assert controller.handle_tag("99999") == "ALARM"

    print("  fake really searches: known -> GATE_OPEN, unknown -> ALARM. OK")


# ===========================================================================
# 4. SIMULATOR — mimics full behavior: states, movement, faults
#    (time is modeled as discrete ticks so the test runs instantly)
# ===========================================================================

class GateState(Enum):
    CLOSED = "closed"
    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"
    FAULT = "fault"


class GateFaultError(Exception):
    """Raised by the simulator when it mimics a hardware failure."""


class GateSimulator:
    """
    Simulates the real electric gate: it transitions through states and
    moves gradually, instead of just returning 'open'. Time is modeled
    as ticks (no real sleeping), so tests are fast and deterministic.
    """

    def __init__(self, ticks_to_open=10, simulate_fault=False):
        self.state = GateState.CLOSED
        self.ticks_to_open = ticks_to_open
        self.simulate_fault = simulate_fault
        self.position = 0                          # 0=closed, 100=fully open

    def open(self):
        if self.simulate_fault:
            self.state = GateState.FAULT
            raise GateFaultError("Gate motor did not respond")

        self.state = GateState.OPENING
        # Model the physical opening as gradual movement
        for i in range(self.ticks_to_open):
            self.position = int((i + 1) / self.ticks_to_open * 100)
        self.state = GateState.OPEN

    def car_passed_then_close(self):
        # Mimics the vehicle sensor firing, then the auto-close cycle
        if self.state != GateState.OPEN:
            return
        self.state = GateState.CLOSING
        self.position = 0
        self.state = GateState.CLOSED


def demo_simulator():
    print("== SIMULATOR ==")

    # Full happy-path cycle
    gate = GateSimulator(ticks_to_open=10)
    assert gate.state == GateState.CLOSED

    gate.open()
    assert gate.state == GateState.OPEN
    assert gate.position == 100                    # really moved to fully open

    gate.car_passed_then_close()
    assert gate.state == GateState.CLOSED          # completed the whole cycle
    print("  full cycle CLOSED -> OPENING -> OPEN -> CLOSING -> CLOSED. OK")

    # Fault injection: the simulator can mimic a hardware failure
    faulty = GateSimulator(simulate_fault=True)
    try:
        faulty.open()
        raise AssertionError("Expected a GateFaultError")
    except GateFaultError:
        assert faulty.state == GateState.FAULT
    print("  fault injection -> state FAULT, error raised. OK")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_mock()
    demo_stub()
    demo_fake()
    demo_simulator()
    print("\nAll demos passed.")

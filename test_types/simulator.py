import time
from enum import Enum


class GateState(Enum):
    CLOSED = "closed"
    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"
    FAULT = "fault"

class GateFaultError(Exception):
    """Raised by the simulator when it mimics a hardware failure."""
    
    
class GateSimulator:
    """Simulates the real electric gate: timing, states, and faults."""

    def __init__(self, open_duration=2.0, simulate_fault=False):
        self.state = GateState.CLOSED
        self.open_duration = open_duration      # seconds to open
        self.simulate_fault = simulate_fault
        self.position = 0                        # 0=closed, 100=fully open

    def open(self):
        # Unlike a mock, the gate really transitions through states
        if self.simulate_fault:
            self.state = GateState.FAULT
            raise GateFaultError("Gate motor did not respond")

        self.state = GateState.OPENING
        # Simulate the physical opening time
        steps = 10
        for i in range(steps):
            time.sleep(self.open_duration / steps)
            self.position = int((i + 1) / steps * 100)  # gradual movement

        self.state = GateState.OPEN

    def sensor_car_passed(self):
        # Simulates the vehicle sensor reporting, then auto-close after 2s
        if self.state != GateState.OPEN:
            return
        time.sleep(2.0)
        self.state = GateState.CLOSING
        self.position = 0
        self.state = GateState.CLOSED


def test_gate_simulator_full_cycle():
    gate = GateSimulator(open_duration=0.5)  # faster for the test

    gate.open()
    assert gate.state == GateState.OPEN
    assert gate.position == 100          # really moved to fully open

    gate.sensor_car_passed()
    assert gate.state == GateState.CLOSED  # completed the whole cycle


def test_gate_simulator_fault():
    # The simulator can mimic a hardware failure
    gate = GateSimulator(simulate_fault=True)

    try:
        gate.open()
        assert False, "Expected a fault"
    except GateFaultError:
        assert gate.state == GateState.FAULT
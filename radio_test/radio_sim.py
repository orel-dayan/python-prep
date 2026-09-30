"""Minimal UDP simulator of a radio management interface.

Stands in for real hardware so the test suite can run on a laptop.

Wire protocol: one JSON object per datagram.
  request : {"seq": <int>, "cmd": <str>, "args": {...}}
  response: {"seq": <int>, "status": "ok" | "error", "data": {...}}
"""

from __future__ import annotations

import json
import random
import socket
import threading
import time
from typing import Self

MIN_TX_POWER_DBM = 0
MAX_TX_POWER_DBM = 30


class FaultProfile:
    """Controlled misbehaviour, so negative tests stay reproducible."""

    def __init__(
        self,
        drop_rate: float = 0.0,
        extra_delay: float = 0.0,
        malformed: bool = False,
        seq_offset: int = 0,
        seed: int | None = None,
    ) -> None:
        self.drop_rate = drop_rate
        self.extra_delay = extra_delay
        self.malformed = malformed
        self.seq_offset = seq_offset
        self.seed = seed


class RadioSimulator:
    """Fake radio answering management requests over UDP."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,
        faults: FaultProfile | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.faults = faults or FaultProfile()
        self._rng = random.Random(self.faults.seed)
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._running = False
        self.requests_seen = 0
        self.state: dict = {
            "node_id": 7,
            "link_state": "up",
            "tx_power_dbm": 20,
            "neighbors": [
                {"node_id": 8, "snr_db": 21},
                {"node_id": 9, "snr_db": 14},
            ],
        }

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self.host, self.port))
        self._sock.settimeout(0.2)
        self.port = self._sock.getsockname()[1]
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self._sock is not None:
            self._sock.close()

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.stop()

    # -- serving -----------------------------------------------------------

    def _serve(self) -> None:
        while self._running:
            try:
                raw, addr = self._sock.recvfrom(4096)
            except TimeoutError:
                continue
            except OSError:
                break
            self.requests_seen += 1
            if self._rng.random() < self.faults.drop_rate:
                continue  # silent drop, exactly like a lost datagram
            if self.faults.extra_delay:
                time.sleep(self.faults.extra_delay)
            try:
                self._sock.sendto(self._build_reply(raw), addr)
            except OSError:
                break

    def _build_reply(self, raw: bytes) -> bytes:
        if self.faults.malformed:
            return b"{ this is not json"
        try:
            request = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return self._error(-1, "bad_request")
        seq = request.get("seq", -1)
        cmd = request.get("cmd", "")
        if cmd == "GET_STATUS":
            data = {k: v for k, v in self.state.items() if k != "neighbors"}
            return self._ok(seq, data)
        if cmd == "GET_NEIGHBORS":
            return self._ok(seq, {"neighbors": self.state["neighbors"]})
        if cmd == "SET_CONFIG":
            return self._set_config(seq, request.get("args", {}))
        return self._error(seq, "unknown_command")

    def _set_config(self, seq: int, args: dict) -> bytes:
        power = args.get("tx_power_dbm")
        if not isinstance(power, int) or isinstance(power, bool):
            return self._error(seq, "invalid_type")
        if not MIN_TX_POWER_DBM <= power <= MAX_TX_POWER_DBM:
            return self._error(seq, "out_of_range")
        self.state["tx_power_dbm"] = power
        return self._ok(seq, {"tx_power_dbm": power})

    # -- helpers -----------------------------------------------------------

    def _ok(self, seq: int, data: dict) -> bytes:
        payload = {"seq": seq + self.faults.seq_offset, "status": "ok", "data": data}
        return json.dumps(payload).encode()

    def _error(self, seq: int, reason: str) -> bytes:
        payload = {
            "seq": seq + self.faults.seq_offset,
            "status": "error",
            "data": {"reason": reason},
        }
        return json.dumps(payload).encode()

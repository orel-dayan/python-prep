"""Device abstraction layer for the radio management interface.

Tests never open a socket themselves: they call radio.get_status().
When the protocol changes, only this file changes.
"""

from __future__ import annotations

import json
import socket
from typing import Self


class RadioError(Exception):
    """Base error for every failure of the radio interface."""


class RadioTimeout(RadioError):
    """No answer arrived within timeout, after all retries."""


class RadioProtocolError(RadioError):
    """The answer could not be parsed or did not match the request."""


class RadioCommandError(RadioError):
    """The radio answered, but rejected the command."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class RadioClient:
    """UDP client for the radio management interface."""

    def __init__(
        self,
        host: str,
        port: int,
        timeout: float = 0.5,
        retries: int = 2,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self._seq = 0
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

    def close(self) -> None:
        self._sock.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    # -- public API --------------------------------------------------------

    def get_status(self) -> dict:
        return self._request("GET_STATUS")

    def get_neighbors(self) -> list[dict]:
        return self._request("GET_NEIGHBORS")["neighbors"]

    def set_tx_power(self, dbm: int) -> dict:
        return self._request("SET_CONFIG", {"tx_power_dbm": dbm})

    # -- transport ---------------------------------------------------------

    def _request(self, cmd: str, args: dict | None = None) -> dict:
        self._seq += 1
        seq = self._seq
        payload = json.dumps({"seq": seq, "cmd": cmd, "args": args or {}})
        last_error: Exception = RadioTimeout(f"{cmd}: no reply")
        for _attempt in range(self.retries + 1):
            try:
                self._sock.sendto(payload.encode(), (self.host, self.port))
                raw, _addr = self._sock.recvfrom(65535)
            except TimeoutError:
                continue
            return self._parse(raw, seq)
        raise last_error

    @staticmethod
    def _parse(raw: bytes, seq: int) -> dict:
        try:
            reply = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RadioProtocolError(f"undecodable reply: {raw!r}") from exc
        if reply.get("seq") != seq:
            raise RadioProtocolError(
                f"sequence mismatch: sent {seq}, got {reply.get('seq')}"
            )
        if reply.get("status") == "error":
            raise RadioCommandError(reply.get("data", {}).get("reason", "unknown"))
        if reply.get("status") != "ok":
            raise RadioProtocolError(f"unexpected status: {reply.get('status')}")
        return reply.get("data", {})

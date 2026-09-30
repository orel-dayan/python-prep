"""Test suite for the radio management client.

Layers covered here:
  functional  - the happy path of every command
  boundary    - min / max / just-outside values
  negative    - malformed replies, unknown commands, wrong types
  resilience  - packet loss, slow answers, retries, recovery
"""
from __future__ import annotations

import time

import pytest
from radio_client import (
    RadioClient,
    RadioCommandError,
    RadioProtocolError,
    RadioTimeout,
)
from radio_sim import RadioSimulator

# --------------------------------------------------------------------------
# functional
# --------------------------------------------------------------------------


def test_get_status_returns_expected_fields(client):
    status = client.get_status()
    assert status["node_id"] == 7 
    assert status["link_state"] == "up"
    assert "tx_power_dbm" in status


def test_get_neighbors_returns_the_neighbor_table(client):
    neighbors = client.get_neighbors()
    assert [n["node_id"] for n in neighbors] == [8, 9]


def test_set_tx_power_is_persisted_on_the_device(client):
    client.set_tx_power(12)
    assert client.get_status()["tx_power_dbm"] == 12


# --------------------------------------------------------------------------
# boundary
# --------------------------------------------------------------------------


@pytest.mark.parametrize("dbm", range(0, 31))
def test_tx_power_inside_range_is_accepted(client, dbm):
    assert client.set_tx_power(dbm)["tx_power_dbm"] == dbm
    assert client.get_status()["tx_power_dbm"] == dbm


@pytest.mark.parametrize("dbm", [-1000, -100, -2, -1, 31, 32, 100, 1000])
def test_tx_power_outside_range_is_rejected(client, dbm):
    with pytest.raises(RadioCommandError) as err:
        client.set_tx_power(dbm)
    assert err.value.reason == "out_of_range"


@pytest.mark.parametrize("initial_dbm", [0, 15, 30])
@pytest.mark.parametrize("rejected_dbm", [-1, 31, 1000])
def test_rejected_value_does_not_change_device_state(
    client, initial_dbm, rejected_dbm
):
    client.set_tx_power(initial_dbm)
    with pytest.raises(RadioCommandError):
        client.set_tx_power(rejected_dbm)
    assert client.get_status()["tx_power_dbm"] == initial_dbm


# --------------------------------------------------------------------------
# negative
# --------------------------------------------------------------------------


def test_wrong_argument_type_is_rejected(client):
    with pytest.raises(RadioCommandError) as err:
        client.set_tx_power("high")
    assert err.value.reason == "invalid_type"


def test_unknown_command_is_reported_not_crashed(client):
    with pytest.raises(RadioCommandError) as err:
        client._request("REBOOT_EVERYTHING")
    assert err.value.reason == "unknown_command"


def test_malformed_reply_raises_protocol_error(radio_factory, client_factory):
    sim = radio_factory(malformed=True)
    client = client_factory(sim)
    with pytest.raises(RadioProtocolError):
        client.get_status()


def test_stale_reply_is_not_accepted_as_the_answer(radio_factory, client_factory):
    """A reply carrying a foreign sequence number must never be trusted."""
    sim = radio_factory(seq_offset=-1)  # answers as if to the previous request
    client = client_factory(sim, timeout=0.1, retries=0)
    with pytest.raises(RadioProtocolError):
        client.get_status()


# --------------------------------------------------------------------------
# resilience
# --------------------------------------------------------------------------


def test_total_loss_raises_timeout_and_not_a_hang(radio_factory, client_factory):
    sim = radio_factory(drop_rate=1.0)
    client = client_factory(sim, timeout=0.1, retries=2)
    started = time.monotonic()
    with pytest.raises(RadioTimeout):
        client.get_status()
    elapsed = time.monotonic() - started
    assert elapsed < 1.0, "client must give up quickly, not block the caller"
    assert sim.requests_seen == 3, "one initial attempt plus two retries"


def test_partial_loss_is_survived_by_retries(radio_factory, client_factory):
    sim = radio_factory(drop_rate=0.5, seed=1)
    client = client_factory(sim, timeout=0.2, retries=5)
    assert client.get_status()["node_id"] == 7


def test_slow_radio_exceeding_timeout_is_reported(radio_factory, client_factory):
    sim = radio_factory(extra_delay=0.4)
    client = client_factory(sim, timeout=0.1, retries=0)
    with pytest.raises(RadioTimeout):
        client.get_status()


def test_client_recovers_after_the_radio_comes_back(radio_factory, client_factory):
    sim = radio_factory()
    client = client_factory(sim, timeout=0.1, retries=0)
    sim.stop()
    with pytest.raises(RadioTimeout):
        client.get_status()
    recovered = RadioSimulator(host=sim.host, port=sim.port)
    recovered.start()
    try:
        assert client.get_status()["node_id"] == 7
    finally:
        recovered.stop()


# --------------------------------------------------------------------------
# contract
# --------------------------------------------------------------------------


def test_unreachable_port_does_not_leak_a_blocking_socket():
    client = RadioClient("127.0.0.1", 9, timeout=0.05, retries=0)
    try:
        with pytest.raises(RadioTimeout):
            client.get_status()
    finally:
        client.close()

"""Shared fixtures: every test gets a clean simulator and a clean client."""

from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from radio_client import RadioClient
from radio_sim import FaultProfile, RadioSimulator


@pytest.fixture
def radio_factory() -> Iterator[Callable[..., RadioSimulator]]:
    """Start a simulator with a chosen fault profile; always tear it down."""
    started: list[RadioSimulator] = []

    def _make(**fault_kwargs: object) -> RadioSimulator:
        sim = RadioSimulator(faults=FaultProfile(**fault_kwargs))
        sim.start()
        started.append(sim)
        return sim

    yield _make
    for sim in started:
        sim.stop()


@pytest.fixture
def radio(radio_factory: Callable[..., RadioSimulator]) -> RadioSimulator:
    """A healthy radio, no faults injected."""
    return radio_factory()


@pytest.fixture
def client(
    radio: RadioSimulator,
    client_factory: Callable[..., RadioClient],
) -> RadioClient:
    """A client connected to the healthy radio for this test."""
    return client_factory(radio)


@pytest.fixture
def client_factory() -> Iterator[Callable[..., RadioClient]]:
    """Build clients against a given simulator and close them afterwards."""
    opened: list[RadioClient] = []

    def _make(sim: RadioSimulator, **kwargs: object) -> RadioClient:
        client = RadioClient(sim.host, sim.port, **kwargs)
        opened.append(client)
        return client

    yield _make
    for client in opened:
        client.close()

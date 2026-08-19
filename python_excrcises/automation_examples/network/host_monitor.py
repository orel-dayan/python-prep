"""
Async network host discovery and HTTP service monitoring.

Demonstrates asyncio for high-concurrency I/O work. Where the thread-based
scanner uses OS threads, this runs everything in a single thread using
cooperative multitasking - lower overhead, scales to thousands of targets.

Usage:
    python host_monitor.py --subnet 192.168.1 --check-http
"""

import argparse
import asyncio
import ipaddress
from dataclasses import dataclass, field
from datetime import datetime

import httpx


@dataclass
class HostStatus:
    address: str
    is_reachable: bool
    open_ports: list[int] = field(default_factory=list)
    http_status: int | None = None
    response_time_ms: float | None = None
    checked_at: datetime = field(default_factory=datetime.now)


async def check_tcp_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Attempt a TCP connection without blocking the event loop."""
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, OSError):
        return False


async def scan_host(host: str, ports: list[int], timeout: float = 1.0) -> HostStatus:
    """Check which of the given ports are open on one host."""
    tasks = [check_tcp_port(host, port, timeout) for port in ports]
    results = await asyncio.gather(*tasks)

    open_ports = [port for port, is_open in zip(ports, results) if is_open]
    return HostStatus(
        address=host,
        is_reachable=bool(open_ports),
        open_ports=open_ports,
    )


async def check_http_service(
    host: str,
    client: httpx.AsyncClient,
    port: int = 80,
    timeout: float = 5.0,
) -> tuple[int | None, float | None]:
    """Check an HTTP endpoint and measure response time."""
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{host}:{port}/"

    start = asyncio.get_event_loop().time()
    try:
        response = await client.get(url, timeout=timeout)
        elapsed_ms = (asyncio.get_event_loop().time() - start) * 1000
        return response.status_code, round(elapsed_ms, 2)
    except (httpx.RequestError, httpx.TimeoutException):
        return None, None


async def scan_subnet(
    subnet: str,
    ports: list[int],
    max_concurrent: int = 50,
    check_http: bool = False,
) -> list[HostStatus]:
    """Scan an entire /24 subnet with bounded concurrency.

    The semaphore prevents opening thousands of sockets at once, which would
    exhaust file descriptors and likely trigger rate limiting or IDS alerts.
    """
    network = ipaddress.ip_network(f"{subnet}.0/24", strict=False)
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_scan(host: str) -> HostStatus:
        async with semaphore:
            return await scan_host(host, ports)

    hosts = [str(ip) for ip in network.hosts()]
    results = await asyncio.gather(*[bounded_scan(h) for h in hosts])
    reachable = [r for r in results if r.is_reachable]

    if check_http:
        async with httpx.AsyncClient(verify=True, follow_redirects=True) as client:
            for status in reachable:
                if 80 in status.open_ports:
                    code, elapsed = await check_http_service(status.address, client, 80)
                    status.http_status = code
                    status.response_time_ms = elapsed

    return reachable


async def main() -> None:
    parser = argparse.ArgumentParser(description="Async subnet scanner")
    parser.add_argument("--subnet", default="192.168.1", help="Subnet prefix, e.g. 192.168.1")
    parser.add_argument("--ports", type=int, nargs="+", default=[22, 80, 443])
    parser.add_argument("--concurrent", type=int, default=50)
    parser.add_argument("--check-http", action="store_true")

    args = parser.parse_args()

    print(f"Scanning {args.subnet}.0/24 on ports {args.ports}")
    results = await scan_subnet(
        args.subnet,
        args.ports,
        max_concurrent=args.concurrent,
        check_http=args.check_http,
    )

    if not results:
        print("No reachable hosts found")
        return

    print(f"\nFound {len(results)} reachable hosts:\n")
    for host in results:
        ports_str = ", ".join(str(p) for p in host.open_ports)
        line = f"  {host.address:<16} ports: {ports_str}"
        if host.http_status is not None:
            line += f" | HTTP {host.http_status} ({host.response_time_ms}ms)"
        print(line)


if __name__ == "__main__":
    asyncio.run(main())

"""
Parallel TCP port scanner.

Port scanning is I/O-bound - each thread spends nearly all its time waiting
on network responses, during which the GIL is released. This makes threading
effective here despite the GIL.

Usage:
    python port_scanner.py 192.168.1.1 --start 1 --end 1024
    python port_scanner.py scanme.nmap.org --common
"""

import argparse
import concurrent.futures
import socket
from dataclasses import dataclass

COMMON_PORTS = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-ALT",
    27017: "MongoDB",
}


@dataclass
class ScanResult:
    port: int
    is_open: bool
    service: str | None = None


def scan_port(host: str, port: int, timeout: float = 0.5) -> ScanResult:
    """Check a single TCP port.

    connect_ex returns an error code instead of raising, which is far more
    convenient than exception handling when most ports will be closed.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        is_open = result == 0
        return ScanResult(port=port, is_open=is_open, service=COMMON_PORTS.get(port))
    finally:
        sock.close()


def scan_ports(
    host: str,
    ports: list[int],
    max_workers: int = 100,
    timeout: float = 0.5,
) -> list[ScanResult]:
    """Scan multiple ports in parallel using a thread pool."""
    open_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # executor.submit(func, *args, **kwargs) schedules func to be called with the given arguments and returns a Future object representing the execution of the function
        # . The futures dictionary maps each Future to its corresponding port number.
        # futures = {
        #     executor.submit(scan_port, host, port, timeout): port for port in ports
        # }
        futures ={
            executor.submit(scan_port , host, port, timeout): port for port in ports
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result.is_open:
                open_results.append(result)

    return sorted(open_results, key=lambda r: r.port)


def resolve_host(host: str) -> str | None:
    """Resolve a hostname to an IP address. Returns None on failure."""
    try:
        return socket.gethostbyname(host)
    except OSError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel TCP port scanner")
    parser.add_argument("host", help="Target host (IP or hostname)")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--common", action="store_true", help="Scan only common ports")
    parser.add_argument("--timeout", type=float, default=0.5, help="Per-port timeout")
    parser.add_argument("--workers", type=int, default=100, help="Thread pool size")

    args = parser.parse_args()

    ip = resolve_host(args.host)
    if ip is None:
        print(f"Could not resolve host: {args.host}")
        return

    ports = (
        sorted(COMMON_PORTS) if args.common else list(range(args.start, args.end + 1))
    )

    print(f"Scanning {args.host} ({ip}) - {len(ports)} ports")
    results = scan_ports(ip, ports, max_workers=args.workers, timeout=args.timeout)

    if not results:
        print("No open ports found")
        return

    print(f"\nFound {len(results)} open ports:")
    for r in results:
        service = f" ({r.service})" if r.service else ""
        print(f"  {r.port}/tcp open{service}")


if __name__ == "__main__":
    main()

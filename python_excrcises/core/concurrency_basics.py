"""Threads vs. processes: the GIL rule in one runnable comparison.

I/O-bound work (network, disk, subprocess) -> threads or asyncio.
CPU-bound work (parsing, hashing, math)     -> processes.
The GIL means threads never speed up CPU-bound Python code.
"""

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def fetch(host: str) -> str:
    """Stand-in for a network call — sleep releases the GIL like real I/O."""
    time.sleep(0.2)
    return f"{host}: ok"


def crunch(n: int) -> int:
    """Pure-Python CPU work — holds the GIL the whole time."""
    return sum(i * i for i in range(n))


if __name__ == "__main__":
    hosts = [f"web-{i:02d}" for i in range(1, 6)]

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(fetch, hosts))
    print(f"threaded I/O: {time.perf_counter() - start:.2f}s for {len(hosts)} hosts")

    workload = [1_000_000] * 4

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(crunch, workload))
    print(f"threads on CPU work : {time.perf_counter() - start:.2f}s (no speedup)")

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(crunch, workload))
    print(f"processes on CPU work: {time.perf_counter() - start:.2f}s (real parallelism)")

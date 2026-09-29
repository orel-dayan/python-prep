"""Open-loop TCP latency probe that avoids coordinated omission."""

import asyncio
import statistics
import time

TARGET_HOST = "192.168.1.50"
TARGET_PORT = 5000
RATE_PER_SEC = 200
DURATION_SEC = 30
TIMEOUT_SEC = 1.0


async def send_one(
    intended_start: float,
    results: list[float],
    errors: list[str],
) -> None:
    # Latency is measured from the intended send time, not the actual one
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(TARGET_HOST, TARGET_PORT),
            TIMEOUT_SEC,
        )
        writer.write(b"PING\n")
        await writer.drain()
        await asyncio.wait_for(reader.readline(), TIMEOUT_SEC)
        writer.close()
        await writer.wait_closed()
        results.append((time.perf_counter() - intended_start) * 1000.0)
    except (OSError, asyncio.TimeoutError) as exc:
        errors.append(type(exc).__name__)


def report(results: list[float], errors: list[str], total: int) -> None:
    if len(results) < 2:
        print(f"Not enough samples: ok={len(results)} errors={len(errors)}")
        return
    cuts = statistics.quantiles(results, n=1000, method="inclusive")
    print(f"sent={total} ok={len(results)} errors={len(errors)}")
    print(f"mean={statistics.fmean(results):.2f} ms")
    print(f"p50={cuts[499]:.2f} ms p95={cuts[949]:.2f} ms p99={cuts[989]:.2f} ms")
    print(f"max={max(results):.2f} ms")


async def main() -> None:
    results: list[float] = []
    errors: list[str] = []
    tasks = []
    interval = 1.0 / RATE_PER_SEC
    total = RATE_PER_SEC * DURATION_SEC
    start = time.perf_counter()
    for i in range(total):
        intended = start + i * interval
        delay = intended - time.perf_counter()
        if delay > 0:
            await asyncio.sleep(delay)
        # Fire on schedule without waiting for previous responses (open model)
        tasks.append(asyncio.create_task(send_one(intended, results, errors)))
    await asyncio.gather(*tasks)
    report(results, errors, total)


if __name__ == "__main__":
    asyncio.run(main())

"""
Reusable decorators for automation scripts.

Decorators are ideal for cross-cutting concerns in automation work - retrying
flaky network calls, timing slow operations, rate limiting API requests, and
logging failures. Each wraps a function without modifying its logic.
"""

import functools
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Log how long a function took.

    functools.wraps preserves the original function's name and docstring -
    without it, the decorated function would report itself as 'wrapper',
    which breaks introspection, debugging, and help().
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"{func.__name__} took {elapsed:.3f}s")

    return wrapper  # type: ignore[return-value]


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Retry a function on failure with exponential backoff.

    Exponential backoff matters for network operations: retrying immediately
    against an overloaded server makes the overload worse. Doubling the wait
    each time gives the remote side room to recover.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    logger.warning(
                        f"{func.__name__} attempt {attempt}/{max_attempts} "
                        f"failed: {e}. Retrying in {current_delay}s"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def rate_limit(calls: int, period: float) -> Callable[[F], F]:
    """Limit a function to N calls per time period.

    Essential when automating against an API - exceeding published rate limits
    typically gets the client IP blocked, which is worse than running slowly.
    """
    def decorator(func: F) -> F:
        timestamps: list[float] = []

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.monotonic()

            # drop timestamps outside the current window
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) >= calls:
                sleep_time = period - (now - timestamps[0])
                if sleep_time > 0:
                    logger.debug(f"Rate limit reached, sleeping {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                    timestamps[:] = [
                        t for t in timestamps if time.monotonic() - t < period
                    ]

            timestamps.append(time.monotonic())
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def max_calls(n: int) -> Callable[[F], F]:
    """Limit total calls to a function across the program's lifetime.

    Useful as a safety valve in destructive automation - a script that
    deletes or restarts things should have a hard ceiling.
    """
    def decorator(func: F) -> F:
        count = 0

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal count
            if count >= n:
                raise RuntimeError(f"{func.__name__} exceeded its limit of {n} calls")
            count += 1
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def log_exceptions(reraise: bool = True) -> Callable[[F], F]:
    """Log any exception with full context before it propagates."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    f"{func.__name__} raised {type(e).__name__}: {e}"
                )
                if reraise:
                    raise
                return None

        return wrapper  # type: ignore[return-value]

    return decorator


def cached(ttl: float | None = None) -> Callable[[F], F]:
    """Cache results, optionally expiring them after ttl seconds.

    Unlike functools.lru_cache, this supports time-based expiry, which matters
    when caching data that goes stale - DNS lookups, config fetches, tokens.
    """
    def decorator(func: F) -> F:
        cache: dict[tuple, tuple[Any, float]] = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in cache:
                value, cached_at = cache[key]
                if ttl is None or now - cached_at < ttl:
                    return value

            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator


# ── Usage examples ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    @timer
    @retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
    def flaky_network_call(fail_times: int = 2) -> str:
        if not hasattr(flaky_network_call, "_calls"):
            flaky_network_call._calls = 0  # type: ignore[attr-defined]
        flaky_network_call._calls += 1  # type: ignore[attr-defined]

        if flaky_network_call._calls <= fail_times:  # type: ignore[attr-defined]
            raise ConnectionError("connection refused")
        return "success"

    print(flaky_network_call())

    @rate_limit(calls=3, period=1.0)
    def api_request(endpoint: str) -> str:
        return f"GET {endpoint}"

    for i in range(5):
        print(api_request(f"/users/{i}"))

    @cached(ttl=2.0)
    def expensive_lookup(key: str) -> str:
        time.sleep(0.5)
        return f"value_for_{key}"

    start = time.perf_counter()
    expensive_lookup("a")
    expensive_lookup("a")  # served from cache, no sleep
    print(f"Two lookups took {time.perf_counter() - start:.2f}s")

# Python Course Summary

---

## 1. Generators & Iterators

A generator is a function that produces values one at a time instead of computing and returning them all at once. This is useful when working with large or infinite sequences, because it never holds the entire sequence in memory.

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
next(gen) # 0
next(gen) # 1
```

The `yield` keyword pauses the function and returns a value to the caller. The function's local state is preserved. On the next call to `next()`, execution resumes exactly where it left off, right after the `yield`.

A generator expression is a shorthand version of the same idea, written like a list comprehension but with parentheses instead of brackets:

```python
squares = (x * x for x in range(10)) # lazy, computed on demand
```

It's also possible to build a custom iterator manually by implementing `__iter__` and `__next__`. This is the lower-level mechanism that powers generators and `for` loops under the hood:

```python
class Counter:
    def __init__(self, limit):
        self._limit = limit
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= self._limit:
            raise StopIteration
        self._current += 1
        return self._current
```

The key rule to remember: a generator is created once and is consumed as it's iterated. If a generator needs to persist across multiple separate function calls (for example, a password generator in a web server that should continue from where it left off on every request), it must be created once and stored somewhere persistent, not recreated on every call.

---

## 2. Decorators

A decorator is a function that wraps another function to add behavior before or after it runs, without modifying the original function's code. This is useful for things like timing, logging, access control, or retry logic.

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.3f}s")
        return result
    return wrapper

@timer
def heavy_computation(n):
    return sum(range(n))
```

When `heavy_computation` is called, Python actually calls `wrapper`, which times the original function, calls it, and returns its result. The `@timer` syntax is just shorthand for `heavy_computation = timer(heavy_computation)`.

Decorators can also accept their own parameters by adding an extra layer of nesting:

```python
def max_calls(n):
    def decorator(func):
        count = 0
        def wrapper(*args, **kwargs):
            nonlocal count
            if count >= n:
                raise RuntimeError(f"{func.__name__} exceeded {n} calls")
            count += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

@max_calls(3)
def greet(name):
    print(f"Hello {name}")
```

Here `max_calls(3)` returns the actual decorator, which then wraps `greet`. The `nonlocal count` is needed because `count` belongs to the enclosing function's scope, not the innermost `wrapper`.

---

## 3. Context Managers

A context manager guarantees that setup and cleanup code run together, even if an exception happens in between. The most common use is the `with` statement, which is what makes file handling safe:

```python
class ManagedResource:
    def __enter__(self):
        print("Resource acquired")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Resource released")
        return False # don't suppress exceptions

with ManagedResource() as r:
    print("Using resource")
```

`__enter__` runs when entering the `with` block and its return value is bound to `r`. `__exit__` runs when leaving the block, whether the code inside succeeded or raised an exception. This is the same idea as RAII in C++ — tying cleanup to a defined scope so it can never be forgotten.

---

## 4. Threading and the GIL

The GIL (Global Interpreter Lock) is a mutex built into CPython that allows only one thread to execute Python bytecode at any given moment. It exists because CPython's memory management (reference counting) is not thread-safe by default, and locking every object individually would be far too slow. Instead, CPython uses one big lock around the whole interpreter.

The practical consequence: Python threads do not give true parallelism for CPU-heavy work. Even on a machine with eight cores, two CPU-bound Python threads will not run any faster than running them one after another, because they're always taking turns for the GIL.

However, the GIL is released during I/O operations — reading a file, waiting for a network response, or sleeping. This means threading is genuinely useful for I/O-bound work, where most of the time is spent waiting rather than computing.

```python
import threading

def task(name):
    print(f"{name} running")

t1 = threading.Thread(target=task, args=("A",))
t2 = threading.Thread(target=task, args=("B",))
t1.start(); t2.start()
t1.join(); t2.join()
```

When multiple threads share data, the same race condition risk that exists in C++ applies here too. Python's `threading.Lock` plays the same role as `std::mutex`:

```python
class SafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1
```

`threading.Condition` mirrors `std::condition_variable` for producer-consumer style coordination, where one thread waits until another signals that something is ready.

---

## 5. Multiprocessing

Where threading shares one interpreter and is bound by the GIL, multiprocessing spawns entirely separate operating system processes. Each process has its own interpreter, its own GIL, and its own memory space. This gives true parallelism — multiple processes really can run on different CPU cores at the same time. The cost is that processes are heavier to start than threads, and since they don't share memory, they need explicit mechanisms (queues, shared memory) to communicate.

```python
from multiprocessing import Pool

def heavy_computation(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__": # required guard, explained below
    with Pool(4) as pool:
        results = pool.map(heavy_computation, [10_000_000] * 4)
```

The `if __name__ == "__main__"` guard is required on Windows and macOS because those platforms create new processes by re-importing the script from scratch. Without the guard, that re-import would trigger the `Pool` creation again inside the new process, leading to infinite recursive process spawning.

Since processes don't share memory, sending data between them requires a `Queue` (similar in spirit to a thread-safe queue, but built on pipes and serialization) or explicit shared memory objects like `Value` and `Array`, which use a lock internally to stay safe.

---

## 6. Choosing Between threading, multiprocessing, and asyncio

The right tool depends on what the bottleneck actually is.

If the program spends most of its time waiting on I/O — network requests, disk reads, database queries — then `threading` or `asyncio` both work well, because the GIL is released during waiting anyway, so there's no real parallelism needed; the goal is just not to sit idle.

If the program spends most of its time doing actual computation — image processing, numeric work, ML training — only `multiprocessing` will speed it up, because it's the only model that gets around the GIL with real parallel execution.

`asyncio` differs from threading in how it achieves concurrency. Threads are managed by the operating system, which can interrupt and switch between them at any point — this is called preemptive multitasking. `asyncio` runs everything in a single thread and switches between tasks only at points the code explicitly marks with `await` — this is called cooperative multitasking. Because there's no OS-level thread switching involved, `asyncio` can scale to thousands of concurrent tasks with very little overhead, which is why it's the standard choice for things like web servers handling many simultaneous connections.

---

## 7. asyncio in Depth

A coroutine is a function defined with `async def`. Calling it does not run it immediately — it returns a coroutine object that represents a deferred computation. The function only actually runs once it's awaited.

```python
async def greet(name):
    return f"Hello {name}"

coro = greet("Alice")   # nothing has run yet
result = await coro     # now it runs
```

`asyncio.run()` is the standard entry point for running asyncio code — it creates an event loop, runs the given coroutine to completion, and shuts the loop down. It should typically be called once, at the very start of the program.

`asyncio.sleep()` is the asynchronous equivalent of `time.sleep()`. The key difference is that it doesn't block the entire program — it tells the event loop "I'm waiting, please go run something else in the meantime."

`asyncio.gather()` runs multiple coroutines concurrently and waits for all of them to finish, returning their results in the same order they were passed in (not necessarily the order they completed in):

```python
async def fetch(url, delay):
    await asyncio.sleep(delay)
    return f"data from {url}"

async def main():
    results = await asyncio.gather(
        fetch("a.com", 1),
        fetch("b.com", 2),
        fetch("c.com", 1),
    )
    # total time is about 2 seconds - the longest single task -
    # not 4 seconds, because they ran concurrently
```

`asyncio.create_task()` is different from `gather` in that it starts a coroutine running in the background immediately, without waiting for it right away. This is useful when you want to kick off some work and come back to collect its result later, while doing something else in between.

`asyncio.wait_for()` adds a timeout to a coroutine — if it doesn't finish in time, a `TimeoutError` is raised instead of waiting forever.

`asyncio.as_completed()` is useful when you have several coroutines running and want to process each result as soon as it's ready, rather than waiting for all of them together — unlike `gather`, which only returns once everything is done.

A very important pitfall: never call a regular blocking function (like `time.sleep()`, or synchronous file I/O) directly inside a coroutine. Since asyncio runs everything in one thread, a blocking call freezes the entire event loop — every other coroutine stalls until it returns. The fix is `asyncio.to_thread()`, which runs the blocking function in a separate worker thread and lets the event loop keep handling other coroutines while waiting for it:

```python
result = await asyncio.to_thread(blocking_function, arg1, arg2)
```

asyncio also provides synchronization primitives that mirror the threading module, but designed for coroutines instead of OS threads: `asyncio.Lock` for mutual exclusion, `asyncio.Semaphore` for limiting how many coroutines can run a section concurrently, `asyncio.Event` for simple signaling, and `asyncio.Queue` for passing data safely between producer and consumer coroutines.

---

## 8. concurrent.futures

This module provides a simpler, higher-level interface over both threading and multiprocessing, using the same API for both. `ThreadPoolExecutor` is meant for I/O-bound work, `ProcessPoolExecutor` for CPU-bound work — the calling code looks almost identical either way:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_io, urls))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute_cpu, values))
```

This is often the easiest entry point for adding concurrency to existing synchronous code, since it doesn't require rewriting functions as coroutines.

---

## 9. FastAPI

FastAPI is a web framework that turns ordinary Python functions into HTTP API endpoints through decorators. What makes it valuable is everything it handles automatically that would otherwise need to be written by hand.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{id}")
async def get_user(id: int) -> User:
    return User.load_from_file(id)
```

When a request comes in for `/users/3`, FastAPI matches the path to this function, extracts `3` from the URL, converts it to an `int` because of the type hint, calls the function, and then automatically converts whatever the function returns into a JSON response. If the URL parameter can't be converted to an `int` (say someone requests `/users/abc`), FastAPI returns a structured error automatically without any extra code.

Because file or database I/O inside a route is blocking, the same `asyncio.to_thread` pattern from earlier applies here too — wrapping blocking calls inside async routes keeps the server responsive to other requests while waiting on disk or network operations.

---

## 10. Pydantic

Pydantic models are regular Python classes that get automatic data validation and conversion based on type hints. A `BaseModel` subclass can be built directly from a JSON string, and can serialize itself back to JSON or to a plain dictionary:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    name: str
    email: str

user = User.model_validate_json(json_string)  # parse and validate JSON
json_str = user.model_dump_json(indent=2)     # serialize back to JSON
data_dict = user.model_dump()                 # convert to a plain dict
```

If the incoming JSON doesn't match the declared types — say `email` is missing or `id` is a string that can't convert to an int — Pydantic raises a clear validation error immediately rather than letting bad data silently propagate through the program. This is what FastAPI relies on internally to validate request bodies.

---

## 11. httpx

httpx is an HTTP client library that supports both synchronous and asynchronous usage with a very similar interface, which makes it easy to use inside both regular scripts and asyncio-based programs.

```python
import httpx

# synchronous
response = httpx.get("https://example.com/users/1")
data = response.json()

# asynchronous
async with httpx.AsyncClient(base_url="https://example.com") as client:
    response = await client.get("/users/1")
    data = response.json()
```

The async version is what unlocks concurrent requests. Instead of fetching several URLs one after another and adding up their wait times, multiple coroutines can be started together and awaited with `asyncio.gather`, so the total time is closer to the slowest single request rather than the sum of all of them.

---

## 12. argparse

argparse builds command-line interfaces by declaring what arguments a script accepts, then automatically parsing `sys.argv` into a clean object.

```python
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("action", choices=["fetch", "create", "load"])
parser.add_argument("--id", type=int, nargs="+")
parser.add_argument("--save", action="store_true")

args = parser.parse_args()
```

`nargs="+"` means the flag accepts one or more values, collected into a list. `action="store_true"` turns a flag into a simple boolean — present means `True`, absent means `False`, with no value needed after it. This is the mechanism behind commands like `python client.py fetch --id 1 2 3 --save`.

---

## 13. logging

The logging module provides structured, leveled messages instead of scattering `print()` statements through code. A logger can have multiple handlers (where messages go — console, file, etc.) and each message has a severity level, from least to most severe: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Setting a logger's level filters out anything less severe than that level.

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
```

This is preferable to `print()` in real applications because logs can be filtered by severity, routed to multiple destinations simultaneously, and timestamped consistently.

---

## 14. The `*` and `**` Operators

The single asterisk unpacks a sequence into individual positional arguments, and the double asterisk does the same for a dictionary into keyword arguments. This comes up constantly when passing a dynamically built list of items into a function that expects them as separate arguments rather than as one list:

```python
tasks = [coro1, coro2, coro3]
asyncio.gather(*tasks) # equivalent to gather(coro1, coro2, coro3)

data = {"name": "Alice", "age": 30}
greet(**data) # equivalent to greet(name="Alice", age=30)
```

The same syntax works in reverse when defining a function, where `*args` collects any number of positional arguments into a tuple, and `**kwargs` collects any number of keyword arguments into a dictionary — this is how functions like `print()` accept a flexible number of inputs.

---

## 15. The Python Import System and Common Problems

This is one of the most confusing parts of Python for newcomers, mostly because import behavior depends on how a script is run, not just on where the files physically live.

### How Python finds modules

When code says `import something`, Python searches a list of directories called `sys.path`, in this order: the directory containing the script that was run, the `PYTHONPATH` environment variable if set, the standard library, and finally any packages installed via pip.

The crucial detail that causes most confusion: "the directory containing the script that was run" is not the same as "the project root." It changes depending on which file you actually executed and from which folder.

### Absolute vs relative imports

An absolute import spells out the full path from the project's root package:

```python
from utils.helper import foo
```

A relative import uses dots to describe position relative to the current file, and only works inside a proper package:

```python
from .helper import foo      # same directory
from ..utils import helper   # one level up
```

In general, absolute imports are easier to read and less fragile, and are the recommended default.

### What `__init__.py` does

A file, often empty, placed in a directory to mark it as a Python package — this is what allows other code to import things from that directory using dotted notation. Since Python 3.3, "namespace packages" technically work without this file, but including it is still considered good practice because it makes the package boundary explicit.

### The classic "ModuleNotFoundError" scenario

Imagine this structure:

```
my_project/
├── main.py
└── utils/
    ├── __init__.py
    ├── helper.py
    └── parser.py
```

If `parser.py` tries `from helper import greet` and you run it directly with `python utils/parser.py`, it fails with `ModuleNotFoundError: No module named 'helper'`. The reason is that `sys.path` only includes `utils/` itself (since that's where the executed script lives), not `my_project/`, so Python has no idea `helper.py` is meant to be a sibling import target within a package context.

The fix is either to use a relative import (`from .helper import greet`) and then run the file as a module from the project root (`python -m utils.parser`), or to use an absolute import (`from utils.helper import greet`) and run it the same way. The deeper, more robust fix for larger projects is to install the project itself as an editable package with `pip install -e .`, after which imports work consistently regardless of the current working directory.

### Circular imports

This happens when two modules import from each other:

```python
# a.py
from b import bar
def foo(): bar()

# b.py
from a import foo
def bar(): foo()
```

This raises `ImportError: cannot import name 'foo' from partially initialized module 'a'`, because when Python starts loading `a.py`, it hits the import of `b.py` before `a.py` has finished defining `foo`, and `b.py` in turn tries to import that not-yet-defined name. A quick fix is moving the import inside the function body so it only resolves when actually called, by which point both modules have finished loading. The more durable fix is usually to recognize that a circular import is a sign the two modules are too tightly coupled, and to move the shared logic into a third module that both can depend on independently.

### `if __name__ == "__main__"`

Every Python file has a built-in `__name__` variable. When a file is run directly, `__name__` is set to `"__main__"`. When the same file is imported by another file, `__name__` is set to the module's actual name instead. This guard lets a file contain code that only runs when executed directly — useful for things like quick tests or command-line entry points — without that code also running every time the file gets imported elsewhere.

---

## 16. Project Structure and Tooling

A typical well-organized Python project separates source code, tests, and configuration clearly:

```
my_project/
├── .venv/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       └── utils/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

A virtual environment (`.venv`) is an isolated Python installation that belongs to a single project. Packages installed inside it don't affect or conflict with other projects' dependencies — this solves the common problem where two projects need different, incompatible versions of the same library.

`pyproject.toml` is the modern standard for declaring a project's dependencies and configuration in one file, replacing the older pattern of a separate `requirements.txt`.

### Ruff

Ruff is a linter and formatter, written in Rust for speed, that replaces several older tools (`flake8`, `black`, `isort`) with one fast tool. It catches unused imports, unused variables, inconsistent formatting, and unsorted imports, and can automatically fix most of these issues:

```bash
ruff check .          # report issues
ruff check --fix .    # auto-fix what it safely can
ruff format .         # reformat code consistently
```

The conventional import order that tools like Ruff enforce is: standard library imports first, then third-party packages, then local project imports, each group separated by a blank line.

---

## Quick Reference

```
threading          - I/O-bound work, shares memory, limited by the GIL
multiprocessing     - CPU-bound work, true parallelism, separate memory
asyncio             - I/O-bound work, single thread, scales to thousands of tasks
concurrent.futures  - simple high-level wrapper over both thread and process pools
```

```
Generators         - lazy evaluation, low memory use, custom iteration logic
Decorators         - reusable behavior wrapped around a function (timing, limits, logging)
Context managers   - guaranteed setup/cleanup pairing, even on exceptions
Pydantic           - automatic data validation and JSON conversion
FastAPI            - turns functions into HTTP endpoints, handles routing and validation
httpx              - HTTP client, works both synchronously and asynchronously
argparse           - turns command-line flags into a clean arguments object
logging            - leveled, structured application messages
```

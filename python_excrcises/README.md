# Python Exercises

Two things live here:

- `core/` — focused, single-topic language exercises (one concept, one small
  runnable example per file).
- `automation_examples/` — larger, realistic automation scripts grouped by
  domain (network, security, system, utils).

## core/

| File | Topic |
|---|---|
| `generators.py` | generator functions vs. generator expressions |
| `collections_and_itertools.py` | `Counter`, `itertools.groupby` |
| `concurrency_basics.py` | threads vs. processes and the GIL |
| `typing_basics.py` | modern type hint syntax, `Protocol` |
| `context_managers.py` | `@contextmanager`, guaranteed cleanup |
| `logging_basics.py` | multi-handler logging setup |
| `requests_basics.py` | sync HTTP calls with `requests` |
| `subprocess_basics.py` | portable `subprocess` calls (ping, service status) |
| `serial_communication.py` | `pyserial` wrapped in a context manager |
| `exceptions.py` | custom exception classes |
| `oop_dunder_methods.py` | `__repr__` / `__eq__` |
| `properties_and_validation.py` | `@property` setters |
| `scope_and_closures.py` | LEGB rule, `global`/`nonlocal`, closures |
| `mutable_defaults.py` | the mutable-default-argument pitfall |
| `pydantic_basics.py` | runtime data validation with `pydantic.BaseModel` |
| `solid/` | the five SOLID principles, one runnable file each — see `solid/README.md` |
| `dataclasses_guide.py` | full `dataclasses` reference (fields, `kw_only`, `frozen`, ...) |
| `dataclasses_practice.py` | shorter `dataclasses` practice |
| `pathlib_guide.py` | full `pathlib` reference (the canonical one for this repo) |
| `pathlib_practice.py` | shorter, hands-on `pathlib` practice |

Each file is self-contained and runnable directly:

```bash
python core/generators.py
```

## automation_examples/

```
automation_examples/
├── network/
│   ├── port_scanner.py      Threaded TCP port scanner
│   ├── host_monitor.py      Async subnet scanner + HTTP checks
│   └── api_client.py        Async REST client with retries + Pydantic
├── security/
│   ├── log_analyzer.py      Web log parsing + attack detection
│   └── integrity_monitor.py SHA-256 file integrity monitoring
├── system/
│   ├── health_monitor.py    Service/disk/memory/load checks via subprocess
│   └── ctypes_bridge.py     Calling a compiled C++ shared library from Python
└── utils/
    └── decorators.py        retry, rate_limit, timer, cached, log_exceptions
```

### Requirements

```bash
pip install httpx pydantic requests pyserial
```

### Running

```bash
# Threaded port scan
python automation_examples/network/port_scanner.py scanme.nmap.org --common

# Async subnet sweep
python automation_examples/network/host_monitor.py --subnet 192.168.1 --check-http

# Async API client
python automation_examples/network/api_client.py fetch --ids 1 2 3 --save

# Log analysis
python automation_examples/security/log_analyzer.py /var/log/nginx/access.log --threshold 10

# File integrity
python automation_examples/security/integrity_monitor.py baseline /etc --output baseline.json
python automation_examples/security/integrity_monitor.py check /etc --baseline baseline.json

# System health (JSON output for piping into monitoring)
python automation_examples/system/health_monitor.py --services nginx sshd --json

# Decorator demos
python automation_examples/utils/decorators.py
```

### Concepts demonstrated

| Concept | Where |
|---|---|
| `subprocess` without `shell=True` | system/health_monitor.py |
| `socket` + `connect_ex` | network/port_scanner.py |
| `ThreadPoolExecutor` for I/O-bound work | network/port_scanner.py |
| `asyncio.gather` + `Semaphore` | network/host_monitor.py, api_client.py |
| `asyncio.to_thread` for blocking I/O | network/api_client.py |
| Async context managers (`__aenter__`) | network/api_client.py |
| Regex with named groups | security/log_analyzer.py |
| Chunked hashing for large files | security/integrity_monitor.py |
| Decorators with parameters | utils/decorators.py |
| `functools.wraps` | utils/decorators.py |
| `argparse` subcommands | api_client.py, integrity_monitor.py |
| `logging` with multiple handlers | system/health_monitor.py |
| Pydantic models + validation | network/api_client.py |
| Dataclasses for structured results | most files |
| `ctypes` calling a C++ shared library | system/ctypes_bridge.py |

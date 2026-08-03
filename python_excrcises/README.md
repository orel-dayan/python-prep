# Python Automation Examples

Working code examples for automation engineering: system automation, network
programming, log analysis, and security tooling.

## Structure

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
│   └── health_monitor.py    Service/disk/memory/load checks via subprocess
└── utils/
    └── decorators.py        retry, rate_limit, timer, cached, log_exceptions
```

## Requirements

```bash
pip install httpx pydantic
```

## Running

```bash
# Threaded port scan
python network/port_scanner.py scanme.nmap.org --common

# Async subnet sweep
python network/host_monitor.py --subnet 192.168.1 --check-http

# Async API client
python network/api_client.py fetch --ids 1 2 3 --save

# Log analysis
python security/log_analyzer.py /var/log/nginx/access.log --threshold 10

# File integrity
python security/integrity_monitor.py baseline /etc --output baseline.json
python security/integrity_monitor.py check /etc --baseline baseline.json

# System health (JSON output for piping into monitoring)
python system/health_monitor.py --services nginx sshd --json

# Decorator demos
python utils/decorators.py
```

## Concepts demonstrated

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

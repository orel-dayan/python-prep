"""
System health monitor.

Checks systemd services, disk usage, memory, and load average, then reports
anything outside configured thresholds. Designed to run under cron.

Demonstrates safe subprocess usage - note that no call uses shell=True,
so no argument can ever be interpreted as a shell command.

Usage:
    python health_monitor.py --services nginx sshd docker
    python health_monitor.py --config health_config.json --json
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path


class Severity(Enum):
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class CheckResult:
    name: str
    severity: Severity
    message: str
    value: float | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


def setup_logging(log_file: Path | None, verbose: bool) -> logging.Logger:
    logger = logging.getLogger("health_monitor")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def run_command(command: list[str], timeout: int = 10) -> tuple[bool, str]:
    """Run a command safely.

    The list form means arguments go directly to the OS - no shell parses
    them, so shell metacharacters have no special meaning. The timeout
    prevents one hung command from blocking the whole check cycle.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    except FileNotFoundError:
        return False, f"command not found: {command[0]}"


def check_service(service: str) -> CheckResult:
    """Check whether a systemd service is active.

    is-active --quiet produces no output and communicates purely through
    its exit code, which is exactly what a script wants.
    """
    is_running, _ = run_command(["systemctl", "is-active", "--quiet", service])

    if is_running:
        return CheckResult(
            name=f"service:{service}",
            severity=Severity.OK,
            message=f"{service} is running",
        )
    return CheckResult(
        name=f"service:{service}",
        severity=Severity.CRITICAL,
        message=f"{service} is DOWN",
    )


def check_disk_usage(
    mount: str = "/",
    warning_pct: int = 80,
    critical_pct: int = 90,
) -> CheckResult:
    success, output = run_command(["df", "--output=pcent", mount])

    if not success or not output:
        return CheckResult(
            name=f"disk:{mount}",
            severity=Severity.WARNING,
            message=f"could not read disk usage for {mount}",
        )

    lines = output.splitlines()
    percent = int(lines[-1].strip().rstrip("%"))

    if percent >= critical_pct:
        severity = Severity.CRITICAL
    elif percent >= warning_pct:
        severity = Severity.WARNING
    else:
        severity = Severity.OK

    return CheckResult(
        name=f"disk:{mount}",
        severity=severity,
        message=f"{mount} at {percent}% capacity",
        value=float(percent),
    )


def check_memory(warning_pct: int = 85, critical_pct: int = 95) -> CheckResult:
    try:
        meminfo = Path("/proc/meminfo").read_text()
    except (FileNotFoundError, PermissionError):
        return CheckResult(
            name="memory",
            severity=Severity.WARNING,
            message="could not read /proc/meminfo",
        )

    values = {}
    for line in meminfo.splitlines():
        key, _, rest = line.partition(":")
        values[key] = int(rest.strip().split()[0])

    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", 0)

    if total == 0:
        return CheckResult(
            name="memory",
            severity=Severity.WARNING,
            message="could not determine total memory",
        )

    used_pct = round((total - available) / total * 100, 1)

    if used_pct >= critical_pct:
        severity = Severity.CRITICAL
    elif used_pct >= warning_pct:
        severity = Severity.WARNING
    else:
        severity = Severity.OK

    return CheckResult(
        name="memory",
        severity=severity,
        message=f"memory at {used_pct}% used",
        value=used_pct,
    )


def check_load_average(cpu_count: int | None = None) -> CheckResult:
    try:
        loadavg = Path("/proc/loadavg").read_text().split()
        load_1min = float(loadavg[0])
    except (FileNotFoundError, PermissionError, ValueError, IndexError):
        return CheckResult(
            name="load",
            severity=Severity.WARNING,
            message="could not read load average",
        )

    if cpu_count is None:
        import os
        cpu_count = os.cpu_count() or 1

    # load per core - above 1.0 means processes are waiting for CPU time
    load_per_core = load_1min / cpu_count

    if load_per_core >= 2.0:
        severity = Severity.CRITICAL
    elif load_per_core >= 1.0:
        severity = Severity.WARNING
    else:
        severity = Severity.OK

    return CheckResult(
        name="load",
        severity=severity,
        message=f"load {load_1min} across {cpu_count} cores ({load_per_core:.2f}/core)",
        value=load_per_core,
    )


def run_all_checks(services: list[str], mounts: list[str]) -> list[CheckResult]:
    results = [check_memory(), check_load_average()]
    results.extend(check_disk_usage(m) for m in mounts)
    results.extend(check_service(s) for s in services)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="System health monitor")
    parser.add_argument("--services", nargs="*", default=[], help="Services to check")
    parser.add_argument("--mounts", nargs="*", default=["/"], help="Mount points")
    parser.add_argument("--log-file", type=Path, help="Write logs to this file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit 1 if any check is critical (useful in CI/cron)",
    )

    args = parser.parse_args()

    results = run_all_checks(args.services, args.mounts)

    if args.json:
        output = {
            "checked_at": datetime.now().isoformat(),
            "results": [r.to_dict() for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        logger = setup_logging(args.log_file, args.verbose)
        for result in results:
            if result.severity is Severity.CRITICAL:
                logger.error(result.message)
            elif result.severity is Severity.WARNING:
                logger.warning(result.message)
            else:
                logger.info(result.message)

    if args.exit_code:
        has_critical = any(r.severity is Severity.CRITICAL for r in results)
        sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()

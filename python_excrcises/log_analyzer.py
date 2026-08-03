"""
Web server log analyzer with attack pattern detection.

Parses Apache/Nginx combined log format and detects common attack signatures:
brute-force login attempts, directory traversal, SQL injection probes,
scanner user agents, and traffic anomalies.

Usage:
    python log_analyzer.py /var/log/nginx/access.log
    python log_analyzer.py access.log --threshold 10 --window 5
"""

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'
    r'\s+\S+\s+\S+\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\w+)\s+(?P<path>\S+)[^"]*"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<size>\d+|-)'
    r'(?:\s+"[^"]*"\s+"(?P<user_agent>[^"]*)")?'
)

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

SUSPICIOUS_PATTERNS = {
    "directory_traversal": re.compile(r"\.\./|\.\.\\|%2e%2e", re.IGNORECASE),
    "sql_injection": re.compile(
        r"(\bunion\b.*\bselect\b|'\s*or\s*'1'\s*=\s*'1|--\s*$|;\s*drop\s+table)",
        re.IGNORECASE,
    ),
    "xss_attempt": re.compile(r"<script|javascript:|onerror\s*=", re.IGNORECASE),
    "command_injection": re.compile(r";\s*(cat|ls|wget|curl|nc)\s|\|\s*sh\b", re.IGNORECASE),
    "sensitive_file": re.compile(
        r"/(\.env|\.git/|wp-config\.php|etc/passwd|\.ssh/)", re.IGNORECASE
    ),
}

SCANNER_AGENTS = re.compile(
    r"(sqlmap|nikto|nmap|masscan|zgrab|dirbuster|gobuster|wpscan|acunetix)",
    re.IGNORECASE,
)


@dataclass
class LogEntry:
    ip: str
    timestamp: datetime | None
    method: str
    path: str
    status: int
    size: int
    user_agent: str


@dataclass
class Finding:
    category: str
    ip: str
    detail: str
    count: int = 1


class LogAnalyzer:
    def __init__(self, log_path: Path):
        self._log_path = log_path
        self._entries: list[LogEntry] = []
        self._malformed_lines = 0

    def parse(self) -> None:
        """Read the log line by line to keep memory constant on large files."""
        with open(self._log_path, errors="replace") as f:
            for line in f:
                entry = self._parse_line(line)
                if entry:
                    self._entries.append(entry)
                elif line.strip():
                    self._malformed_lines += 1

    def _parse_line(self, line: str) -> LogEntry | None:
        match = LOG_PATTERN.match(line)
        if not match:
            return None

        data = match.groupdict()
        try:
            timestamp = datetime.strptime(data["timestamp"], TIMESTAMP_FORMAT)
        except ValueError:
            timestamp = None

        size_raw = data["size"]
        return LogEntry(
            ip=data["ip"],
            timestamp=timestamp,
            method=data["method"],
            path=data["path"],
            status=int(data["status"]),
            size=0 if size_raw == "-" else int(size_raw),
            user_agent=data.get("user_agent") or "",
        )

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    @property
    def malformed_count(self) -> int:
        return self._malformed_lines

    def detect_brute_force(
        self, threshold: int = 5, window_minutes: int = 5
    ) -> list[Finding]:
        """Find IPs with many auth failures inside a sliding time window.

        A time window matters here - 50 failures spread over a week is a
        forgetful user, but 50 in five minutes is an attack.
        """
        failures: dict[str, list[datetime]] = defaultdict(list)

        for entry in self._entries:
            if entry.status in (401, 403) and entry.timestamp:
                failures[entry.ip].append(entry.timestamp)

        findings = []
        window = timedelta(minutes=window_minutes)

        for ip, times in failures.items():
            times.sort()
            for i, start in enumerate(times):
                in_window = sum(1 for t in times[i:] if t - start <= window)
                if in_window >= threshold:
                    findings.append(
                        Finding(
                            category="brute_force",
                            ip=ip,
                            detail=f"{in_window} auth failures in {window_minutes}min",
                            count=in_window,
                        )
                    )
                    break

        return sorted(findings, key=lambda f: f.count, reverse=True)

    def detect_attack_patterns(self) -> list[Finding]:
        """Match request paths against known attack signatures."""
        hits: dict[tuple[str, str], list[str]] = defaultdict(list)

        for entry in self._entries:
            for category, pattern in SUSPICIOUS_PATTERNS.items():
                if pattern.search(entry.path):
                    hits[(category, entry.ip)].append(entry.path)

        return [
            Finding(
                category=category,
                ip=ip,
                detail=f"e.g. {paths[0][:80]}",
                count=len(paths),
            )
            for (category, ip), paths in sorted(
                hits.items(), key=lambda kv: len(kv[1]), reverse=True
            )
        ]

    def detect_scanners(self) -> list[Finding]:
        """Identify automated scanning tools by user agent."""
        scanners: dict[str, Counter] = defaultdict(Counter)

        for entry in self._entries:
            match = SCANNER_AGENTS.search(entry.user_agent)
            if match:
                scanners[entry.ip][match.group(1).lower()] += 1

        return [
            Finding(
                category="scanner",
                ip=ip,
                detail=", ".join(f"{tool} ({n})" for tool, n in tools.most_common()),
                count=sum(tools.values()),
            )
            for ip, tools in scanners.items()
        ]

    def detect_enumeration(self, threshold: int = 20) -> list[Finding]:
        """Many 404s from one IP usually means directory/file enumeration."""
        not_found: Counter = Counter()

        for entry in self._entries:
            if entry.status == 404:
                not_found[entry.ip] += 1

        return [
            Finding(
                category="enumeration",
                ip=ip,
                detail=f"{count} requests returned 404",
                count=count,
            )
            for ip, count in not_found.most_common()
            if count >= threshold
        ]

    def top_requesting_ips(self, n: int = 10) -> list[tuple[str, int]]:
        return Counter(e.ip for e in self._entries).most_common(n)

    def error_rate(self) -> float:
        if not self._entries:
            return 0.0
        errors = sum(1 for e in self._entries if e.status >= 400)
        return errors / len(self._entries)

    def status_distribution(self) -> dict[int, int]:
        return dict(Counter(e.status for e in self._entries).most_common())


def print_findings(title: str, findings: list[Finding]) -> None:
    if not findings:
        return
    print(f"\n{title}")
    print("-" * len(title))
    for f in findings[:15]:
        print(f"  [{f.ip:<15}] {f.detail}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Web server log analyzer")
    parser.add_argument("logfile", type=Path, help="Path to access log")
    parser.add_argument("--threshold", type=int, default=5, help="Brute force threshold")
    parser.add_argument("--window", type=int, default=5, help="Time window in minutes")
    parser.add_argument("--enum-threshold", type=int, default=20, help="404 threshold")

    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"File not found: {args.logfile}")
        return

    analyzer = LogAnalyzer(args.logfile)
    analyzer.parse()

    print(f"Parsed {analyzer.entry_count} entries ({analyzer.malformed_count} malformed)")
    print(f"Error rate: {analyzer.error_rate():.1%}")

    print("\nStatus code distribution")
    print("-" * 24)
    for status, count in analyzer.status_distribution().items():
        print(f"  {status}: {count}")

    print("\nTop requesting IPs")
    print("-" * 18)
    for ip, count in analyzer.top_requesting_ips():
        print(f"  {ip:<16} {count}")

    print_findings(
        "Brute force attempts",
        analyzer.detect_brute_force(args.threshold, args.window),
    )
    print_findings("Attack patterns in request paths", analyzer.detect_attack_patterns())
    print_findings("Automated scanners", analyzer.detect_scanners())
    print_findings("Directory enumeration", analyzer.detect_enumeration(args.enum_threshold))


if __name__ == "__main__":
    main()

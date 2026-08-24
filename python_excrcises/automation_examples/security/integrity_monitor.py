"""
File integrity monitor.

Records SHA-256 hashes of files in a directory tree and detects modifications,
additions, and deletions on subsequent runs. Since any content change produces
a completely different hash, this catches tampering even when an attacker
preserves timestamps and file sizes.

Usage:
    python integrity_monitor.py baseline /etc --output baseline.json
    python integrity_monitor.py check /etc --baseline baseline.json
"""

import argparse
import hashlib
import json
import stat
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

CHUNK_SIZE = 65536  # 64KB - balances syscall overhead against memory use


@dataclass
class FileRecord:
    path: str
    sha256: str
    size: int
    mode: str
    mtime: float


@dataclass
class IntegrityReport:
    modified: list[str]
    added: list[str]
    deleted: list[str]
    permission_changed: list[str]
    checked_at: str

    @property
    def has_changes(self) -> bool:
        return bool(
            self.modified or self.added or self.deleted or self.permission_changed
        )

    @property
    def total_changes(self) -> int:
        return (
            len(self.modified)
            + len(self.added)
            + len(self.deleted)
            + len(self.permission_changed)
        )


def compute_hash(file_path: Path) -> str | None:
    """Hash a file in chunks so memory use stays constant regardless of size.

    iter(callable, sentinel) calls the lambda repeatedly until it returns
    the sentinel - here b"", which read() returns at end of file.
    """
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None


def build_baseline(
    directory: Path,
    exclude_patterns: list[str] | None = None,
) -> dict[str, FileRecord]:
    """Walk a directory tree and record a hash for every readable file."""
    exclude_patterns = exclude_patterns or []
    baseline: dict[str, FileRecord] = {}

    for path in directory.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        if any(pattern in str(path) for pattern in exclude_patterns):
            continue

        file_hash = compute_hash(path)
        if file_hash is None:
            continue

        stat_info = path.stat()
        baseline[str(path)] = FileRecord(
            path=str(path),
            sha256=file_hash,
            size=stat_info.st_size,
            mode=stat.filemode(stat_info.st_mode),
            mtime=stat_info.st_mtime,
        )

    return baseline


def compare(
    baseline: dict[str, FileRecord],
    current: dict[str, FileRecord],
) -> IntegrityReport:
    """Diff two snapshots.

    Additions and deletions matter as much as modifications - an attacker
    dropping a backdoor or deleting logs to cover tracks shows up here.
    """
    baseline_paths = set(baseline)
    current_paths = set(current)

    modified = [
        p
        for p in baseline_paths & current_paths
        if baseline[p].sha256 != current[p].sha256
    ]
    permission_changed = [
        p
        for p in baseline_paths & current_paths
        if baseline[p].sha256 == current[p].sha256
        and baseline[p].mode != current[p].mode
    ]

    return IntegrityReport(
        modified=sorted(modified),
        added=sorted(current_paths - baseline_paths),
        deleted=sorted(baseline_paths - current_paths),
        permission_changed=sorted(permission_changed),
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def save_baseline(baseline: dict[str, FileRecord], output: Path) -> None:
    data = {path: asdict(record) for path, record in baseline.items()}
    output.write_text(json.dumps(data, indent=2))


def load_baseline(path: Path) -> dict[str, FileRecord]:
    data = json.loads(path.read_text())
    return {p: FileRecord(**record) for p, record in data.items()}


def cmd_baseline(args: argparse.Namespace) -> None:
    print(f"Building baseline for {args.directory}")
    baseline = build_baseline(args.directory, args.exclude)
    save_baseline(baseline, args.output)
    print(f"Recorded {len(baseline)} files to {args.output}")


def cmd_check(args: argparse.Namespace) -> None:
    if not args.baseline.exists():
        print(f"Baseline not found: {args.baseline}")
        return

    baseline = load_baseline(args.baseline)
    print(f"Loaded baseline with {len(baseline)} files")

    current = build_baseline(args.directory, args.exclude)
    report = compare(baseline, current)

    if not report.has_changes:
        print("No changes detected - integrity verified")
        return

    print(f"\n{report.total_changes} changes detected\n")

    for label, items in [
        ("MODIFIED", report.modified),
        ("ADDED", report.added),
        ("DELETED", report.deleted),
        ("PERMISSIONS CHANGED", report.permission_changed),
    ]:
        if items:
            print(f"{label} ({len(items)})")
            for item in items[:20]:
                print(f"  {item}")
            if len(items) > 20:
                print(f"  ... and {len(items) - 20} more")
            print()


def main() -> None:
    parser = argparse.ArgumentParser(description="File integrity monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline_parser = subparsers.add_parser("baseline", help="Create a baseline")
    baseline_parser.add_argument("directory", type=Path)
    baseline_parser.add_argument("--output", type=Path, default=Path("baseline.json"))
    baseline_parser.add_argument(
        "--exclude", nargs="*", default=["__pycache__", ".git"]
    )
    baseline_parser.set_defaults(func=cmd_baseline)

    check_parser = subparsers.add_parser("check", help="Check against a baseline")
    check_parser.add_argument("directory", type=Path)
    check_parser.add_argument("--baseline", type=Path, default=Path("baseline.json"))
    check_parser.add_argument("--exclude", nargs="*", default=["__pycache__", ".git"])
    check_parser.set_defaults(func=cmd_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

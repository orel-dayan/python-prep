"""Pathlib practice — every demo runs inside a temp sandbox and cleans up.

Run:  python pathlib_ex.py
"""

import csv
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath

# --------------------------------------------------------------------------
# Project layout template — paths are DEFINED here, not created.
# Creating directories at import time is a side effect: importing this module
# would litter the disk. Call ensure_project_dirs() explicitly when you want it.
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"


def ensure_project_dirs() -> None:
    """Create the standard project directory tree."""
    for directory in (DATA_DIR, RAW_DIR, OUTPUT_DIR, LOG_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


# --------------------------------------------------------------------------
# 1. Creating, reading, inspecting a single file
# --------------------------------------------------------------------------
def demo_basic_file(work: Path) -> None:
    """Write a file, read it back, inspect it."""
    section("1. Basic file operations")

    p = work / "test.txt"
    p.write_text("Hello, World!\n", encoding="utf-8")

    print("content   :", p.read_text(encoding="utf-8").strip())
    print("exists    :", p.exists())
    print("is_file   :", p.is_file())
    print("is_dir    :", p.is_dir())

    stats = p.stat() 
    print("size      :", stats.st_size, "bytes")
    mtime = datetime.fromtimestamp(stats.st_mtime, tz=timezone.utc)
    print("modified  :", mtime)


# --------------------------------------------------------------------------
# 2. Decomposing a path
# --------------------------------------------------------------------------
def demo_path_parts(work: Path) -> None:
    """Show the read-only attributes that split a path apart."""
    section("2. Path components")

    p = work / "reports" / "2026" / "summary.tar.gz"

    print("full      :", p)
    print("name      :", p.name)
    print("stem      :", p.stem)
    print("suffix    :", p.suffix)
    print("suffixes  :", p.suffixes)
    print("parent    :", p.parent)
    print("parents[1]:", p.parents[1])
    print("parts     :", p.parts)
    print("anchor    :", p.anchor)

    # with_* methods return a NEW path; the original is unchanged
    print("as pdf    :", p.with_suffix(".pdf").name)
    print("renamed   :", p.with_name("final.txt").name)
    print("new stem  :", p.with_stem("report").name)


# --------------------------------------------------------------------------
# 3. Cross-platform anchors
# --------------------------------------------------------------------------
def demo_anchors() -> None:
    """Locations you can rely on without hardcoding an absolute path."""
    section("3. Cross-platform anchors")

    print("home      :", Path.home())
    print("cwd       :", Path.cwd())
    print("script dir:", PROJECT_ROOT)
    print("temp dir  :", Path(tempfile.gettempdir()))

    # A config path that works on every OS
    config = Path.home() / ".config" / "myapp" / "settings.json"
    print("config    :", config)

    # APPDATA / LOCALAPPDATA exist only on Windows.
    # Using os.environ["..."] directly raises KeyError on Linux and macOS.
    if os.name == "nt":
        print("appdata   :", Path(os.environ["APPDATA"]))
        print("localapp  :", Path(os.environ["LOCALAPPDATA"]))
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
        print("xdg config:", Path(xdg))


# --------------------------------------------------------------------------
# 4. Directories: create, rename, delete
# --------------------------------------------------------------------------
def demo_directories(work: Path) -> None:
    """mkdir / rmdir / rename / unlink, each guarded correctly."""
    section("4. Directories and renaming")

    # parents=True builds the whole tree; exist_ok=True avoids FileExistsError
    nested = work / "output" / "logs"
    nested.mkdir(parents=True, exist_ok=True)
    print("created   :", nested.relative_to(work))

    # rmdir only removes an EMPTY directory, and raises if it is missing
    empty = work / "empty_dir"
    empty.mkdir(exist_ok=True)
    empty.rmdir()
    print("removed   :", empty.name, "->", empty.exists())

    # rename fails if the source does not exist, so create it first.
    # replace() overwrites the target on both Windows and Linux; rename()
    # raises FileExistsError on Windows when the target already exists.
    old = work / "old.txt"
    old.write_text("data\n", encoding="utf-8")
    new = old.replace(work / "new.txt")
    print("renamed   :", new.name, "exists:", new.exists())

    # missing_ok=True means no exception when the file is already gone
    new.unlink(missing_ok=True)
    (work / "never_existed.txt").unlink(missing_ok=True)
    print("deleted   : ok")

    # rmdir cannot remove a non-empty tree — that needs shutil
    shutil.rmtree(work / "output")
    print("rmtree    : output/ removed")


# --------------------------------------------------------------------------
# 5. Absolute paths and normalization
# --------------------------------------------------------------------------
def demo_resolve(work: Path) -> None:
    """resolve, absolute, relative_to, is_relative_to."""
    section("5. Resolving paths")

    messy = work / ".." / work.name / "." / "test.txt"

    print("messy     :", messy)
    print("resolved  :", messy.resolve())
    print("absolute? :", messy.is_absolute())

    # relative_to raises ValueError when the path is not under the base
    print("relative  :", messy.resolve().relative_to(work))
    print("under work:", messy.resolve().is_relative_to(work))

    # Comparison is syntactic. Single dots are stripped on construction,
    # but '..' is not — so these two are NOT equal until resolved.
    print("naive ==   :", Path("a/b") == Path("a/c/../b"))
    print("resolved ==:", Path("a/b").resolve() == Path("a/c/../b").resolve())


# --------------------------------------------------------------------------
# 6. Globbing — remember these are generators
# --------------------------------------------------------------------------
def demo_glob(work: Path) -> None:
    """Build a small tree, then query it with glob patterns."""
    section("6. Globbing")

    src = work / "src"
    (src / "utils").mkdir(parents=True, exist_ok=True)
    (src / "main.py").write_text("# main\n", encoding="utf-8")
    (src / "config.json").write_text("{}\n", encoding="utf-8")
    (src / "test_main.py").write_text("# test\n", encoding="utf-8")
    (src / "utils" / "helpers.py").write_text("# helpers\n", encoding="utf-8")

    # glob() returns a generator — wrap in list()/sorted() to use the result
    print("*.py      :", sorted(p.name for p in src.glob("*.py")))
    print("test_*.py :", sorted(p.name for p in src.glob("test_*.py")))
    print("recursive :", sorted(str(p.relative_to(src)) for p in src.rglob("*.py")))
    print("dirs only :", sorted(p.name for p in src.glob("*") if p.is_dir()))

    # iterdir lists direct children only
    print("children  :", sorted(p.name for p in src.iterdir()))

    # match() compares from the right-hand side of the path
    helper = src / "utils" / "helpers.py"
    print("match *.py:", helper.match("*.py"))
    print("match u/*  :", helper.match("utils/*.py"))


# --------------------------------------------------------------------------
# 7. Walking a tree with pruning (Python 3.12+)
# --------------------------------------------------------------------------
def demo_walk(work: Path) -> None:
    """Path.walk() lets you skip entire branches; rglob does not."""
    section("7. Walking with pruning")

    skip = {"__pycache__", ".git", ".venv"}
    (work / "src" / "__pycache__").mkdir(parents=True, exist_ok=True)
    (work / "src" / "__pycache__" / "main.pyc").write_bytes(b"\x00")

    for dirpath, dirnames, filenames in work.walk():
        # Modifying dirnames IN PLACE prunes the traversal
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            print("  ", (dirpath / name).relative_to(work))


# --------------------------------------------------------------------------
# 8. Pure paths — logic without touching the disk
# --------------------------------------------------------------------------
def demo_pure_paths() -> None:
    """PurePath models another OS's rules from any machine."""
    section("8. Pure paths")

    posix = PurePosixPath("/srv/uploads") / "orel" / "data.csv"
    windows = PureWindowsPath("C:/Users/orel") / "Documents" / "data.csv"

    print("posix     :", posix)
    print("windows   :", windows)
    print("win parts :", windows.parts)
    print("as posix  :", windows.as_posix())

    # Useful for unit tests: no filesystem required, same result everywhere
    print("win drive :", windows.drive)
    print("absolute? :", windows.is_absolute())


# --------------------------------------------------------------------------
# 9. Working with JSON and CSV
# --------------------------------------------------------------------------
def demo_serialization(work: Path) -> None:
    """read_text/write_text for JSON; open() for CSV."""
    section("9. JSON and CSV")

    # ensure_ascii=False keeps non-Latin characters readable in the file
    config_path = work / "config.json"
    config_path.write_text(
        json.dumps({"name": "demo", "retries": 3}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print("json      :", json.loads(config_path.read_text(encoding="utf-8")))

    # csv needs a file object; newline="" prevents blank rows on Windows
    csv_path = work / "scores.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "score"])
        writer.writeheader()
        writer.writerows([{"name": "a", "score": 95}, {"name": "b", "score": 88}])

    with csv_path.open(newline="", encoding="utf-8") as f:
        print("csv       :", list(csv.DictReader(f)))


# --------------------------------------------------------------------------
# 10. Error handling — EAFP beats checking first
# --------------------------------------------------------------------------
def read_config(path: Path) -> str:
    """Read a text file, returning a sane default when it is missing."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except IsADirectoryError:
        print(f"{path} is a directory, not a file")
        return ""
    except UnicodeDecodeError:
        # Fallback for legacy files that are not UTF-8
        return path.read_text(encoding="latin-1")
    except PermissionError:
        print(f"No access to {path}")
        raise


def demo_errors(work: Path) -> None:
    """Show the guarded read in action."""
    section("10. Error handling")

    print("missing   :", repr(read_config(work / "nope.txt")))
    print("directory :", repr(read_config(work)))


# --------------------------------------------------------------------------
# 11. Reusable helpers worth keeping
# --------------------------------------------------------------------------
def write_atomic(path: Path, content: str) -> None:
    """Write via a temp file and swap, so readers never see a partial file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def unique_path(path: Path) -> Path:
    """Return path, or path with (1), (2)... appended if it already exists."""
    if not path.exists():
        return path

    counter = 1
    while True:
        candidate = path.with_stem(f"{path.stem} ({counter})")
        if not candidate.exists():
            return candidate
        counter += 1


def safe_join(base: Path, user_input: str) -> Path:
    """Join user input to base, refusing anything that escapes base."""
    base = base.resolve()
    target = (base / user_input).resolve()
    if not target.is_relative_to(base):
        raise ValueError(f"Path escapes base directory: {user_input}")
    return target


def demo_helpers(work: Path) -> None:
    """Exercise the helpers above."""
    section("11. Reusable helpers")

    target = work / "state.json"
    write_atomic(target, '{"ok": true}\n')
    print("atomic    :", target.read_text(encoding="utf-8").strip())

    print("unique 1  :", unique_path(target).name)
    print("unique 2  :", unique_path(work / "brand_new.json").name)

    print("safe ok   :", safe_join(work, "sub/file.txt").relative_to(work.resolve()))
    try:
        safe_join(work, "../../etc/passwd")
    except ValueError as exc:
        print("safe block:", exc)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> None:
    """Run every demo inside a self-cleaning sandbox."""
    with tempfile.TemporaryDirectory(prefix="pathlib_demo_") as td:
        work = Path(td)
        print("sandbox   :", work)

        demo_basic_file(work)
        demo_path_parts(work)
        demo_anchors()
        demo_directories(work)
        demo_resolve(work)
        demo_glob(work)
        demo_walk(work)
        demo_pure_paths()
        demo_serialization(work)
        demo_errors(work)
        demo_helpers(work)

    print("\nSandbox removed. Nothing was left on disk.")


if __name__ == "__main__":
    main()

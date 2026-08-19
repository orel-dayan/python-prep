"""Pathlib practice - creates its own sandbox and cleans up."""

import shutil
from collections import defaultdict
from pathlib import Path

# Sandbox next to this script, not next to wherever you ran python from
work = Path(__file__).resolve().parent / "sandbox"
if work.exists():
    shutil.rmtree(work)
work.mkdir()

print("--- creating and reading ---")
f = work / "test.txt"
f.write_text("Hello, World!\n", encoding="utf-8")
print(f.read_text(encoding="utf-8").strip())
print(f.exists(), f.is_file(), f.is_dir())
print(f.stat().st_size, "bytes")

print("--- path parts ---")
print(f.name, f.stem, f.suffix, sep=" | ")
print(f.parent)

print("--- rename ---")
old = work / "old.txt"
old.write_text("data\n", encoding="utf-8")
new = old.replace(work / "new.txt")
print(new.name, new.exists())

print("--- directories ---")
empty = work / "empty_dir"
empty.mkdir()
print(empty.exists())
empty.rmdir()
print(empty.exists())

print("--- nested tree and globbing ---")
(work / "src" / "utils").mkdir(parents=True)
(work / "src" / "main.py").write_text("# main\n", encoding="utf-8")
(work / "src" / "utils" / "helpers.py").write_text("# helpers\n", encoding="utf-8")

for py in sorted(work.rglob("*.py")):
    print(py.relative_to(work))

print("--- cleanup ---")
shutil.rmtree(work)
print("sandbox exists:", work.exists())


# 1. Write a function that takes a folder and returns a dict of extension → number of files, sorted descending.
def count_extensions(folder: Path) -> dict[str, int]:
    """Count file extensions in a folder and return a dict of extension → number of files, sorted descending."""
    counts = {}
    for file in folder.rglob("*"):
        if file.is_file():
            ext = file.suffix
            counts[ext] = counts.get(ext, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def find_duplicates_by_name(folder: Path) -> dict[str, list[Path]]:
    files_by_name = defaultdict(list)

    for file in folder.rglob("*"):
        if file.is_file():
            files_by_name[file.name].append(file)

    return {name: paths for name, paths in files_by_name.items() if len(paths) > 1}

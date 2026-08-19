# Argparse Tutorial — full walkthrough

Both `qa_tool.py` and `runner_cli.py` are built on Python's built-in `argparse` module for
parsing command-line arguments. This is a deep, from-scratch explanation of the whole topic,
with references to where each concept shows up in this folder.

## 1. Why argparse

Instead of manually parsing `sys.argv` (splitting strings, checking prefixes, converting types
by hand), you **declare** what arguments your program accepts, and argparse handles:
- Parsing and type conversion.
- Required vs. optional arguments, and defaults.
- Validation (`choices`, custom `type` functions).
- Automatic `--help`/`-h` generation.
- Consistent, well-formatted error messages and exit codes on bad input.

The alternative (hand-rolled parsing) scales badly: every new flag means more manual
`if arg == "--foo"` branches, more places to forget validation, and no free `--help`.

## 2. Creating the parser

```python
import argparse

parser = argparse.ArgumentParser(
    prog="qa_tool",                # name shown in usage/help text (defaults to sys.argv[0])
    description="Run QA tests.",   # shown at the top of --help
)
```
(see `qa_tool.py`)

Other useful `ArgumentParser(...)` options:
- `epilog="..."` — extra text shown at the *bottom* of `--help`.
- `add_help=False` — disable the automatic `-h/--help` (rare; you'd add your own).
- `formatter_class=argparse.ArgumentDefaultsHelpFormatter` — automatically appends
  `(default: ...)` to each argument's help text, so you don't have to write it manually.

## 3. Positional arguments

Required, identified by **position**, not by a flag:

```python
parser.add_argument("suite", help="Name of the test suite to run.")
```

Running `python qa_tool.py smoke_suite` sets `args.suite == "smoke_suite"`. If you omit it,
argparse prints a usage error and exits with status code 2 — no manual validation needed.

### `nargs` — controlling how many values an argument consumes

| `nargs` | Meaning | Result type |
|---|---|---|
| *(omitted)* | Exactly one value | scalar |
| `"?"` | Zero or one value | scalar or `default` |
| `"*"` | Zero or more values | `list` (possibly empty) |
| `"+"` | One or more values (error if zero) | `list` |
| `N` (an int) | Exactly N values | `list` of length N |

```python
parser.add_argument("paths", nargs="*", help="Optional test file paths.")
```
(see `runner_cli.py`) — `python runner_cli.py smoke a.py b.py` → `args.paths == ["a.py", "b.py"]`;
`python runner_cli.py smoke` → `args.paths == []`.

> **Gotcha:** mixing a `nargs="*"` positional with other positionals after it is ambiguous —
> argparse can't tell where the list ends and the next positional begins. Keep variable-length
> positionals last, or use flags instead.

## 4. Optional arguments (flags)

Identified by `-x`/`--xyz` prefixes; not required unless `required=True` is passed. Both a
short and a long form can be registered together, and either can be used on the command line:

```python
parser.add_argument("-e", "--env", choices=["dev", "staging", "prod"], default="dev",
                     help="Environment to run the tests against. Default is 'dev'.")
```

- **`choices=[...]`** — argparse rejects any value not in the list with an automatic error
  message (`invalid choice: 'x' (choose from 'dev', 'staging', 'prod')`). Best for enum-like
  options (here: environment, or `--browser`).
- **`default=...`** — value used when the flag is not passed. Accessed identically whether the
  user supplied it or not (`args.env`). Without `default=`, the attribute is `None` if omitted.
- **`required=True`** — makes an *optional-looking* flag mandatory (rare, but valid — e.g. an
  `--api-key` that has no sane default).
- **`type=int`** — converts the raw string argument at parse time, raising a clean
  `argument -t/--timeout: invalid int value: 'abc'` error on bad input instead of an
  unhandled `ValueError` deep inside your program:

```python
parser.add_argument("-t", "--timeout", type=int, default=30,
                     help="Timeout in seconds for each test.")
parser.add_argument("--retries", type=int, default=0)
```

- **`type=Path`** — converts straight into a `pathlib.Path`, so downstream code never deals
  with raw strings:

```python
parser.add_argument("--output", type=Path, default=Path("results.json"),
                     help="Output file for test results.")
```

- **`type` can be any callable**, including your own validation function. Raise
  `argparse.ArgumentTypeError` inside it for a clean, argparse-formatted error message:

```python
def positive_int(value: str) -> int:
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError(f"{value!r} is not a positive integer")
    return n

parser.add_argument("--workers", type=positive_int, default=1)
```

## 5. Boolean flags — `action="store_true"` / `"store_false"`

For on/off switches that take no value on the command line:

```python
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
```

`args.verbose` is `False` unless `-v`/`--verbose` is present, in which case it's `True`. There's
no `type=bool` here — passing the flag *is* the "on" signal, there is no `--verbose true/false`
syntax. Use `action="store_false"` (with `default=True`) for a flag that turns something *off*,
e.g. `--no-color` → `args.color == False`.

## 6. Repeatable flags — `action="append"`

Lets the same flag be passed multiple times, collecting every value into a list — good for
tags, include/exclude filters, extra paths, etc.:

```python
parser.add_argument("--tag", action="append", default=[], help="Filter tests by tag.")
```

`python qa_tool.py suite --tag smoke --tag regression` → `args.tag == ["smoke", "regression"]`.
If `--tag` is never passed, `args.tag` stays `[]` (the `default`).

> **Note on the mutable `default=[]` here:** this is safe, unlike a mutable *function* default
> argument (see [python_rules.py](python_rules.py)). Argparse builds a **fresh** `Namespace`
> object on every call to `parse_args()`, and for `action="append"` it copies/extends from the
> default rather than mutating the same list object shared across parser instances or calls.
> The classic Python footgun is specifically about **function** defaults, which *are* created
> once at function-definition time and reused on every call — argparse's `default=` doesn't
> have that lifetime problem here.

Related actions:
- `action="count"` — counts how many times a flag appears (`-vvv` → `args.v == 3`), handy for
  verbosity levels.
- `action="extend"` (3.8+) — like `append`, but for flags that also accept multiple values via
  `nargs`, flattening the results into one list.

## 7. Mutually exclusive groups

Use `add_mutually_exclusive_group()` when two flags conflict and should never be passed
together (argparse errors out if both are given):

```python
group = parser.add_mutually_exclusive_group()
group.add_argument("--dry-run", action="store_true")
group.add_argument("--force", action="store_true")
```

## 8. Argument groups (organizational only)

`add_argument_group("Network options")` doesn't change parsing behavior — it only changes how
`--help` visually groups related arguments together, which matters once a CLI has many flags.

## 9. Parsing

```python
args = parser.parse_args()          # reads from sys.argv[1:] by default
args = parser.parse_args(["suite", "--env", "staging"])  # or pass an explicit list
```

Passing an explicit list (instead of relying on `sys.argv`) is exactly how you'd unit-test an
argparse-based CLI without actually invoking a subprocess:

```python
def test_env_defaults_to_dev():
    args = parser.parse_args(["smoke_suite"])
    assert args.env == "dev"
```

`parse_args()` returns a `Namespace` object — attribute access matches each argument's
*destination* name: the long option name with leading dashes stripped and internal dashes
turned into underscores (e.g. `--dry-run` → `args.dry_run`). You can override this explicitly
with `dest="..."` on `add_argument`.

`parse_known_args()` is a variant that returns `(namespace, remaining_args)` instead of erroring
on unrecognized arguments — useful when wrapping/forwarding args to another tool.

## 10. Auto-generated help and errors

Argparse builds `--help`/`-h` automatically from your `add_argument` calls, including each
argument's `help=` text, its `choices`, and its `default` (if you used
`ArgumentDefaultsHelpFormatter`):

```powershell
python cli_tools\qa_tool.py --help
```

Invalid input (missing positional, bad `choices`, non-numeric `--timeout`, etc.) prints a
`usage:` line plus a specific error message to **stderr** and exits with status **2** — no
manual `try`/`except` needed for basic validation. This matters for scripting: callers can
check the exit code without parsing your error text.

## 11. Subcommands (not used here, but common)

For CLIs with multiple distinct commands (`git commit`, `git push`, ...), `add_subparsers()`
lets each subcommand have its own independent set of arguments and its own help text:

```python
subparsers = parser.add_subparsers(dest="command", required=True)

run_parser = subparsers.add_parser("run", help="Run a suite")
run_parser.add_argument("suite")

report_parser = subparsers.add_parser("report", help="Show a report")
report_parser.add_argument("--format", choices=["json", "html"], default="json")

args = parser.parse_args()
if args.command == "run":
    ...
elif args.command == "report":
    ...
```

## 12. Common pitfalls

- **Negative numbers as values:** `--timeout -5` can confuse argparse into treating `-5` as a
  flag. If you truly need negative numeric values, pass them as `--timeout=-5` (with `=`), or
  declare the option with a leading digit-only prefix pattern.
- **Order of `add_argument` calls** doesn't affect parsing, but does affect the order flags
  appear in `--help`.
- **Reusing one parser across tests** without re-adding arguments works fine (the parser is
  stateless between `parse_args()` calls) — but building a *fresh* `ArgumentParser()` per test
  is the safer, more explicit pattern if you're mutating it (e.g. adding subparsers
  conditionally).
- **Forgetting `choices` is case-sensitive:** `--env Dev` will fail against
  `choices=["dev", "staging", "prod"]`; normalize input yourself (e.g. `.lower()`) before
  validating if you want case-insensitive matching.

## Where to look next

| Concept | File |
|---|---|
| Positional + optional args, `choices`, `type`, `store_true`, `append` | [qa_tool.py](qa_tool.py) |
| `nargs="*"` for optional positional paths | [runner_cli.py](runner_cli.py) |
| The unrelated (but similarly-named) mutable-default-*argument* pitfall | [../exercises/python_rules.py](../exercises/python_rules.py) |

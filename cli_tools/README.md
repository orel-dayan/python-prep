# CLI Tools

Small command-line utilities built around `argparse`, plus a Windows helper script for
repeatedly running the test suite.

## Files

- `qa_tool.py` — `argparse`-based CLI (`qa_tool`) for running QA test suites: accepts a suite
  name, environment (`dev`/`staging`/`prod`), timeout, retries, verbosity, tags, browser choice,
  and an output file (defaults to `results.json`) for storing results.
- `runner_cli.py` — A simpler/alternate `argparse` CLI (`runner`) mirroring similar options
  (suite, paths, env, timeout, verbose, tag, browser) for running a test suite. Named without a
  `test_` prefix on purpose — pytest's default discovery matches `test_*.py`/`*_test.py`, and
  this file calls `parser.parse_args()`, which would otherwise crash test collection.
- `runTests.bat` — Windows batch script that clears the screen and repeatedly runs
  `python -m pytest -v` in a loop, pausing between runs.

## Running

```powershell
python cli_tools\qa_tool.py <suite> --env dev
.\cli_tools\runTests.bat
```

For a full argparse walkthrough (parser setup, positional/optional args, `choices`, `type`,
`store_true`, `append`, subcommands, and common pitfalls), see
[ARGPARSE_TUTORIAL.md](ARGPARSE_TUTORIAL.md).

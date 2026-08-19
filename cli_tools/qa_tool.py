import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class RunConfig:
    suite: str
    paths: list[str]
    env: str
    timeout: int
    verbose: bool
    tag: list[str]
    browser: str
    output: Path

parser = argparse.ArgumentParser(prog="qa_tool", description="Run QA tests.")
parser.add_argument("suite", help="Name of the test suite to run.")
#parser.add_argument("paths", nargs="*", help="Optional test file paths to run. If not provided, all tests in the suite will be executed.")
parser.add_argument("-e", "--env", choices=["dev", "staging", "prod"], default="dev", help="Environment to run the tests against. Default is 'dev'.")
parser.add_argument("-t", "--timeout", type=int, default=30, help="Timeout in seconds for each test. Default is 30 seconds.")
parser.add_argument("--retries", type=int, default=0, help="Number of times to retry failed tests. Default is 0 (no retries).")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
parser.add_argument("--tag", action="append", default=[], help="Filter tests by tag.")
parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome", help="Browser to use for running tests.")

parser.add_argument("--output", type=Path, default=Path("results.json"), help="Output file for test results.")


# Guard parse_args() so importing this module (e.g. to reuse RunConfig) doesn't parse real sys.argv.
if __name__ == "__main__":
    args = parser.parse_args()
if args.retries < 0: 
    parser.error("retries must be non-negative")
config = RunConfig(**vars(args)) 
print(config)
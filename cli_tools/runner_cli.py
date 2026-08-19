import argparse

parser = argparse.ArgumentParser(prog="runner", description="Run a test suite.")
parser.add_argument("suite", help="suite name")
parser.add_argument("paths", nargs="*", help="optional test file paths")
parser.add_argument("-e", "--env", choices=["dev", "staging", "prod"], default="dev")
parser.add_argument("-t", "--timeout", type=int, default=30)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--tag", action="append", default=[])
parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome")

# Guard parse_args() so importing this module (e.g. from a test) doesn't parse real sys.argv.
if __name__ == "__main__":
    args = parser.parse_args()
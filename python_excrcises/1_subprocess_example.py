"""
subprocess example — run a C++ executable from Python and validate output.
Typical interview question: "write a Python script that runs a C++ program
and checks its output."
"""

import subprocess


def run_program(executable: str, args: list[str]) -> tuple[int, str, str]:
    """Run an executable and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [executable] + args,
        capture_output=True,   # capture stdout and stderr
        text=True,             # decode bytes to str automatically
        timeout=5              # kill if takes more than 5 seconds
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def test_addition_program():
    """Example: test a C++ program that adds two numbers."""
    code, out, err = run_program("./add.exe", ["3", "7"])

    assert code == 0,       f"program crashed: {err}"
    assert out == "10",     f"wrong output: '{out}'"
    print("PASS: addition test")


def test_wrong_output():
    """Example: check that bad input produces an error message."""
    code, out, err = run_program("./add.exe", ["abc", "7"])

    assert code != 0,               "expected non-zero exit code for bad input"
    assert "error" in err.lower(),  f"expected error message, got: '{err}'"
    print("PASS: error-handling test")


# ── run all tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Running subprocess tests...")
    # NOTE: replace "./add.exe" with your actual compiled C++ binary path
    # test_addition_program()
    # test_wrong_output()
    print("Done. (uncomment tests above after compiling the C++ program)")

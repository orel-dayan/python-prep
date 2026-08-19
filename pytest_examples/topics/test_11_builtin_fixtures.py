"""
Topic: built-in fixtures - tmp_path, capsys, monkeypatch, caplog

- tmp_path: a unique, real temp directory (pathlib.Path) per test, auto-cleaned.
- capsys: capture stdout/stderr printed during the test.
- monkeypatch: safely patch attributes/env vars/etc., auto-undone after the test.
- caplog: capture and assert on log records emitted via the `logging` module.

Run:
    python -m pytest pytest_examples/topics/test_11_builtin_fixtures.py -v

Example run:
    4 tests should PASS.
"""
import logging
import os


def test_tmp_path(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"


def test_capsys(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_monkeypatch(monkeypatch):
    monkeypatch.setenv("MY_VAR", "test_value")
    assert os.environ["MY_VAR"] == "test_value"


def test_caplog(caplog):
    with caplog.at_level(logging.INFO):
        logging.info("something happened")
    assert "something happened" in caplog.text

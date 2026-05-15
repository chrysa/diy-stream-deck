"""Tests for __main__ entry point."""

from __future__ import annotations

from pathlib import Path

import pytest

from diy_stream_deck.__main__ import main


def test_main_no_args_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """Running without args should raise SystemExit with non-zero code."""
    monkeypatch.setattr("sys.argv", ["diy-stream-deck"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0


def test_main_dry_run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Running with --dry-run and a valid config should print and return 0."""
    config = tmp_path / "test.yml"
    config.write_text("device:\n  type: virtual\n")
    monkeypatch.setattr("sys.argv", ["diy-stream-deck", "--config", str(config), "--dry-run"])
    result = main()
    assert result == 0
    captured = capsys.readouterr()
    assert "DIY Stream Deck" in captured.out

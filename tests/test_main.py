"""Tests for __main__ entry point."""

from __future__ import annotations

from pathlib import Path

import pytest

from diy_stream_deck.__main__ import ConfigError, load_config, main


def test_main_no_args_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """Running without args should raise SystemExit with non-zero code."""
    monkeypatch.setattr("sys.argv", ["diy-stream-deck"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0


def test_main_dry_run_valid_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Running with --dry-run and a valid config validates it and returns 0."""
    config = tmp_path / "test.yml"
    config.write_text("device:\n  type: virtual\n")
    monkeypatch.setattr("sys.argv", ["diy-stream-deck", "--config", str(config), "--dry-run"])
    result = main()
    assert result == 0
    captured = capsys.readouterr()
    assert "valid" in captured.out


def test_main_dry_run_missing_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """A missing config file makes --dry-run fail with a non-zero code."""
    missing = tmp_path / "absent.yml"
    monkeypatch.setattr("sys.argv", ["diy-stream-deck", "--config", str(missing), "--dry-run"])
    assert main() == 1


def test_main_dry_run_malformed_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Malformed YAML makes --dry-run fail with a non-zero code."""
    config = tmp_path / "bad.yml"
    config.write_text("device: [unclosed\n")
    monkeypatch.setattr("sys.argv", ["diy-stream-deck", "--config", str(config), "--dry-run"])
    assert main() == 1


def test_load_config_rejects_non_mapping(tmp_path: Path) -> None:
    """A config whose root is not a mapping is rejected."""
    config = tmp_path / "list.yml"
    config.write_text("- just\n- a\n- list\n")
    with pytest.raises(ConfigError):
        load_config(config)


def test_load_config_requires_device_section(tmp_path: Path) -> None:
    """A config without a 'device' section is rejected."""
    config = tmp_path / "no-device.yml"
    config.write_text("actions: {}\n")
    with pytest.raises(ConfigError):
        load_config(config)

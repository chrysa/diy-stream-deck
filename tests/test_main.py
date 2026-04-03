"""Tests for __main__ entry point."""
import subprocess
import sys


def test_main_no_args_fails():
    """Running without args should exit with non-zero."""
    result = subprocess.run(
        [sys.executable, "-m", "diy_stream_deck"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_main_dry_run(tmp_path):
    """Running with --dry-run and a missing config should not crash the import."""
    config = tmp_path / "test.yml"
    config.write_text("device:\n  type: virtual\n")
    result = subprocess.run(
        [sys.executable, "-m", "diy_stream_deck", "--config", str(config), "--dry-run"],
        capture_output=True,
        text=True,
    )
    # Not yet implemented — just checks it doesn't crash on import
    assert result.returncode == 0

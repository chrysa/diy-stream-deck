"""DIY Stream Deck entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


class ConfigError(Exception):
    """Raised when the YAML config is missing, unreadable, or invalid."""


def load_config(path: Path) -> dict[str, object]:
    """Load and validate a YAML config file.

    Raises ConfigError on a missing file, malformed YAML, or a structurally
    invalid config (not a mapping, or missing the required ``device`` section).
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {path}") from exc
    except OSError as exc:
        raise ConfigError(f"cannot read config file {path}: {exc}") from exc

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ConfigError(f"malformed YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"config root must be a mapping, got {type(data).__name__}")
    if "device" not in data:
        raise ConfigError("config is missing the required 'device' section")
    return data


def main() -> int:
    """Run the DIY Stream Deck daemon."""
    parser = argparse.ArgumentParser(description="DIY Stream Deck")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--dry-run", action="store_true", help="Validate config without running")
    args = parser.parse_args()

    config_path = Path(args.config)
    try:
        load_config(config_path)
    except ConfigError as exc:
        sys.stderr.write(f"DIY Stream Deck — config error: {exc}\n")
        return 1

    sys.stdout.write(f"DIY Stream Deck — config: {config_path} (valid)\n")
    if args.dry_run:
        sys.stdout.write("Dry run — config is valid, not starting.\n")
        return 0

    sys.stdout.write("Not yet implemented — see roadmap in README.md\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

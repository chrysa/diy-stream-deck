# CLAUDE.md — diy-stream-deck

## Project Purpose

DIY Stream Deck alternative compatible with Linux and Windows. Maps physical inputs (USB macropad, Raspberry Pi Pico W, virtual) to configurable actions: Home Assistant service calls, shell commands, HTTP requests, media controls, and keyboard shortcuts.

## Architecture

- `core/` — event loop, key mapper, action runner
- `actions/` — action plugins (ha_service, shell_cmd, http_request, media_control, hotkey)
- `hardware/` — HID abstraction (macropad, pico-w, virtual)
- `config/` — YAML schema and loader
- `ui/` — optional system tray
- `tests/` — unit and integration tests

## Key Constraints

- Python 3.12+ minimum, target 3.14
- Must run on Linux AND Windows (no Linux-only code in core; use abstraction layer)
- `evdev` for Linux HID — `pynput` for Windows HID — imported conditionally by platform
- Home Assistant integration is optional — never required to start
- YAML config drives everything — no hardcoded key bindings
- Actions must be pluggable and independently testable

## Development Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check .
ruff format --check .
pre-commit run --all-files
```

## Related repositories

- `chrysa/D-D` — home automation infrastructure
- `chrysa/github-actions` — shared CI actions
- `chrysa/pre-commit-tools` — shared pre-commit hooks
- `chrysa/shared-standards` — Copilot instructions and standards

## Notion

Project tracking: https://www.notion.so/33759293e35e812f8d14ea4ea23618cf

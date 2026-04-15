---
# diy-stream-deck — GitHub Copilot Instructions

## MANDATORY: Read Instructions FIRST

**Before any development task**, read the relevant instruction files in `.github/instructions/`.

- `.github/instructions/python_guidelines.instructions.md` — Python 3.14, strict typing, ruff
- `.github/instructions/platform.instructions.md` — Linux/Windows cross-platform abstraction, HID, actions

---

## Project Overview

DIY Stream Deck alternative compatible with **Linux and Windows**. Maps physical inputs (USB macropad, Raspberry Pi Pico W, virtual keyboard) to configurable actions: Home Assistant service calls, shell commands, HTTP requests, media controls, keyboard shortcuts.

## Stack

| Layer | Tech |
|---|---|
| Language | Python 3.14 (min 3.12) |
| Linux HID | `evdev` |
| Windows HID | `pynput` |
| Config | YAML (Pydantic schema validation) |
| Actions | Plugin architecture |
| UI | Optional system tray (`pystray`) |
| Quality | ruff (lint+format), mypy strict |
| Testing | pytest |

## Repository Structure

```
diy_stream_deck/
  core/             Event loop, key mapper, action runner
  actions/          Action plugins (ha_service, shell_cmd, http_request, media_control, hotkey)
  hardware/         HID abstraction layer (macropad, pico-w, virtual)
  config/           YAML schema (Pydantic) + loader
  ui/               Optional system tray
tests/              Unit + integration tests
pyproject.toml
```

## Development Workflow

```bash
pip install -e ".[dev]"        # Install with dev extras
pytest tests/ -v               # Run tests
ruff check .                   # Lint
ruff format --check .          # Format check
pre-commit run --all-files     # Full pre-commit suite
```

## NON-NEGOTIABLE RULES

- **Python 3.14** — `from __future__ import annotations` in every file
- Cross-platform first: **no Linux-only code in `core/`** — use abstraction layer
- `evdev` and `pynput` imported conditionally by platform (`sys.platform`)
- YAML config drives everything — no hardcoded key bindings in source
- Actions must be independently testable without hardware
- Home Assistant integration is **optional** — app must start without it
- ALL public functions fully type-annotated
- OWASP Top 10: validate all external inputs (YAML config, HTTP responses, HA payloads)

## Related repositories

- `chrysa/github-actions` — shared CI actions
- `chrysa/pre-commit-tools` — shared pre-commit hooks
- `chrysa/shared-standards` — global Copilot instructions


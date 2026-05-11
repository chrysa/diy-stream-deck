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



## Quality Thresholds

- Max function length: 50 lines when practical.
- Max file length: 500 lines when practical.
- Max cyclomatic complexity: 10.
- Lint warnings target: 0.

## Regression Prevention (NON-NEGOTIABLE)

Before marking **any** task or sub-task as done, the agent MUST verify that no regression has been introduced.

### Required checks — run in order

1. **Tests** — `make test` (or equivalent): number of passing tests must be **>=baseline** (count before the change). Zero new failures allowed.
2. **Coverage** — coverage percentage must be **>=baseline**. Never decrease. If no baseline exists, record the current value as baseline.
3. **Lint** — `make lint` (or `ruff check` / `eslint`): warning count must be **= 0**. No increase tolerated.
4. **Types** — `mypy` / `tsc --noEmit`: error count must be **<=baseline**. No new type errors allowed.
5. **Build** — `make build` must exit 0 when applicable.

### Procedure

- Record baseline metrics **before** starting the task (tests passing, coverage %, lint count, type errors).
- After each implementation step, re-run the relevant checks.
- **If any check regresses**: stop, fix the regression, re-run all checks before continuing.
- Do NOT proceed to the next task if any gate is red.

### Reporting

After completing a task, always report:

    Tests : <N> passed (baseline <N>) pass/fail
    Coverage: <X>% (baseline <X>%) pass/fail
    Lint    : 0 warnings pass/fail
    Types   : 0 errors pass/fail
    Build   : ok pass/fail

# Architecture — DIY Stream Deck

> Grounded in the files present in this repository (`pyproject.toml`, `Makefile`,
> `README.md`, `diy_stream_deck/`, `tests/`, `scripts/`). Where the docs and the
> manifests disagreed, the manifests were trusted (see Notes).

## Purpose

Open-source, cross-platform (Linux + Windows) alternative to a Stream Deck. It maps
physical inputs (USB macropad, Raspberry Pi Pico W, or a repurposed tablet) to custom
actions, with Home Assistant integration. Configuration is expressed in YAML.

**Status: early scaffold.** Only the package skeleton, the CLI entry point, and YAML
config validation exist today. The action engine, device backends, and Home Assistant
actions described in the README are the *target* design, not yet implemented.

## Stack

- Language: Python (`requires-python = ">=3.14"` in `pyproject.toml`).
- Runtime dependencies: `pyyaml>=6.0`, `requests>=2.32`, `pynput>=1.7`.
- Optional extra `linux`: `evdev>=1.7`.
- Dev extra: `pytest`, `pytest-asyncio`, `pytest-cov`, `mypy`, `ruff`, `pre-commit`.
- Tooling: Ruff (lint + format), mypy (type-check), pytest + coverage (gate at 85%),
  pre-commit, a custom quality gate (`scripts/quality_gate.py`), Docker test image
  (`Dockerfile.test`).

## Layout

```
diy_stream_deck/
  __init__.py        # package marker
  __main__.py        # CLI entry point + YAML config load/validation (implemented)
tests/
  __init__.py
  test_main.py       # unit tests for the CLI / config validation
scripts/
  quality_gate.py    # baseline/verify quality gate
  gen_context_files.py
docs/reference/       # reference documentation
```

Modules referenced by the README (`devices/`, `actions/`, `virtual/`, etc.) are the
planned target architecture and are **not present** in the tree yet.

## Entrypoints

- `python -m diy_stream_deck --config <file>` — loads and validates the YAML config;
  with `--dry-run`, validates only and exits without starting.
- `main()` in `diy_stream_deck/__main__.py` parses args, calls `load_config()`, and
  currently prints "Not yet implemented — see roadmap" when not a dry run.
- `load_config(path)` raises `ConfigError` on a missing/unreadable file, malformed YAML,
  a non-mapping root, or a missing required `device` section.

## Data / External deps

- Config: a YAML file with a required top-level `device` section (schema otherwise
  documented in `README.md`; only the `device` key is enforced by code today).
- Home Assistant: HTTP API integration via `requests` — **planned** (`ha_service` action),
  not implemented. Requires an HA URL and long-lived access token when built.
- HID input: `evdev` (Linux) / `pynput` (cross-platform) — planned device backends.
- No database or persistent store present.

## Build & test

Real commands (from `Makefile` / `pyproject.toml`):

```bash
make install-dev        # pip install -e ".[dev]"
make lint               # ruff check diy_stream_deck/ tests/
make format-check       # ruff format --check diy_stream_deck/ tests/
make typecheck          # mypy
make test               # pytest tests/ -v
make test-cov           # pytest with coverage, --cov-fail-under=85
make ci                 # lint + format-check + typecheck + test-cov
make docker-test        # build & run tests in Docker (Dockerfile.test)
make pre-commit         # install + run pre-commit hooks
```

## Notes

- `pyproject.toml` pins `requires-python = ">=3.14"`, while `README.md`/`CLAUDE.md`
  reference Python 3.13 (and a Ruff `py313` comment). Per the "trust the manifest" rule,
  3.14 is authoritative here; the discrepancy is flagged.
- No secrets are stored in the repo; HA credentials are supplied via environment/config
  at runtime (planned).

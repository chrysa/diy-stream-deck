# Requirements — DIY Stream Deck

> Derived from `README.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `pyproject.toml`, and the
> source (`diy_stream_deck/__main__.py`, `tests/`). Each requirement is tagged
> FACT (stated/observed in the repo), INFERENCE (reasonable deduction), or
> UNKNOWN. The implementation matrix marks IMPLEMENTED only where verifiable in code.

## Product requirements

| ID | Requirement | Tag | Evidence |
|----|-------------|-----|----------|
| REQ-PROD-001 | Provide an open-source, cross-platform (Linux + Windows) alternative to a proprietary Stream Deck. | FACT | `README.md` Overview / Goals |
| REQ-PROD-002 | Map physical inputs (USB macropad, Raspberry Pi Pico W, repurposed tablet) to configurable actions. | FACT | `README.md` Overview, Hardware Options |
| REQ-PROD-003 | Support action types: Home Assistant service call, shell command, HTTP request, media control, keyboard hotkey. | FACT | `README.md` Actions table |
| REQ-PROD-004 | Integrate natively with Home Assistant; the integration is optional and never required to start. | FACT | `README.md`, `CLAUDE.md` Key Constraints |
| REQ-PROD-005 | Drive all behaviour from a YAML configuration file — no hardcoded key bindings. | FACT | `CLAUDE.md`, `README.md` Configuration |
| REQ-PROD-006 | Keep total hardware cost under ~50 € with commodity components. | FACT | `README.md` Goals, Cost Estimate |
| REQ-PROD-007 | Offer an optional system-tray UI and config hot-reload. | FACT (planned) | `README.md` Roadmap v0.3, `CLAUDE.md` `ui/` |
| REQ-PROD-008 | Offer a tablet UI as a later milestone. | FACT (planned) | `README.md` Roadmap v1.0 |

## Technical requirements

| ID | Requirement | Tag | Evidence |
|----|-------------|-----|----------|
| REQ-TECH-001 | CLI entry point `python -m diy_stream_deck --config <file>` with a `--dry-run` config-validation mode. | FACT | `diy_stream_deck/__main__.py`, `README.md` |
| REQ-TECH-002 | Validate YAML config: root must be a mapping and must contain a `device` section; malformed/missing files fail with a non-zero exit. | FACT | `load_config()` in `__main__.py`; `tests/test_main.py` |
| REQ-TECH-003 | Run on Python — `requires-python = ">=3.14"`. | FACT | `pyproject.toml` |
| REQ-TECH-004 | No Linux-only code in core; HID input abstracted per platform (`evdev` Linux, `pynput` cross-platform), imported conditionally. | FACT (constraint; backend not yet implemented) | `CLAUDE.md` Key Constraints, `pyproject.toml` deps/extras |
| REQ-TECH-005 | Actions are pluggable and independently unit-testable. | FACT (constraint) | `CLAUDE.md` Key Constraints |
| REQ-TECH-006 | Home Assistant actions call the HA HTTP API via `requests` using a URL + long-lived token supplied at runtime (env/config). | INFERENCE (planned) | `README.md` HA Integration, `requests` dependency |
| REQ-TECH-007 | Test coverage gate ≥ 85 %. | FACT | `pyproject.toml` `--cov-fail-under=85`, `Makefile` `test-cov` |
| REQ-TECH-008 | Lint/format via Ruff, types via mypy `strict`, quality gate via `scripts/quality_gate.py`. | FACT | `pyproject.toml`, `Makefile` |
| REQ-TECH-009 | Tests runnable inside a container (`Dockerfile.test`, `make docker-test`). | FACT | `Makefile`, `Dockerfile.test` |

## Implementation matrix (verifiable only)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| REQ-TECH-001 (CLI + `--dry-run`) | IMPLEMENTED | `main()` in `__main__.py`; `tests/test_main.py::test_main_dry_run_*` |
| REQ-TECH-002 (config validation) | IMPLEMENTED | `load_config()`; `test_load_config_*` |
| REQ-PROD-002/003/004 (device backends, action runner, HA) | NOT IMPLEMENTED | `main()` prints "Not yet implemented — see roadmap"; no `core/`, `actions/`, `hardware/` modules present |
| REQ-PROD-005 (YAML-driven) | PARTIAL | Config is loaded and the `device` key is enforced; the full schema (actions, home_assistant) is documented but not validated in code |
| REQ-PROD-007/008 (tray/hot-reload/tablet UI) | NOT IMPLEMENTED | Roadmap-only; no code |

**Status:** early scaffold. Only the CLI and YAML validation exist; everything in the
Actions/Hardware/HA tables is target design (see `ROADMAP.md`).

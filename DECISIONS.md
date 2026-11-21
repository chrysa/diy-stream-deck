# Decisions (ADR log) — DIY Stream Deck

> Lightweight ADR log reconstructed from repository evidence. Decisions not recorded
> in-repo are marked UNKNOWN. Repo-wide chrysa decisions are inherited via the managed
> standards block in `CLAUDE.md` ("Cross-cutting stack — settled ADRs").

## ADR-001 — YAML as the single configuration source

- **Status:** Accepted — FACT (`CLAUDE.md`, `README.md`, `__main__.py`)
- **Context:** Key bindings and actions must be user-editable without code changes.
- **Decision:** All behaviour is driven by a YAML config with a required `device`
  section; no hardcoded bindings.
- **Consequence:** A config loader/validator is the first implemented component;
  the full schema is validated incrementally (only `device` today).

## ADR-002 — Cross-platform via a HID abstraction layer

- **Status:** Accepted (constraint; backend not yet built) — FACT (`CLAUDE.md`)
- **Context:** Must run on Linux (primary) and Windows.
- **Decision:** Core stays platform-neutral; `evdev` (Linux) and `pynput`
  (cross-platform) are imported conditionally behind an abstraction.
- **Consequence:** `evdev` is an optional `linux` extra; `pynput` is a base dependency.

## ADR-003 — Pluggable, independently testable actions

- **Status:** Accepted (constraint) — FACT (`CLAUDE.md`)
- **Decision:** Action types (`ha_service`, `shell_cmd`, `http_request`,
  `media_control`, `hotkey`) are plugins, each unit-testable in isolation.
- **Consequence:** Planned `actions/` package; not present yet.

## ADR-004 — Python 3.14 target, Ruff pinned to py313

- **Status:** Accepted with a documented workaround — FACT (`pyproject.toml`)
- **Context:** ruff format ≤0.15.15 strips multi-`except` parens under `py314`.
- **Decision:** `requires-python >= 3.14`, but Ruff `target-version = "py313"` until
  the upstream formatter bug is fixed.
- **Consequence:** A minimum-version discrepancy across docs (see `REVIEW.md`).

## ADR-005 — Ship as an early scaffold first

- **Status:** Accepted — FACT (`ARCHITECTURE.md`, `README.md`, `main()` stub)
- **Decision:** Land the package skeleton, CLI, and config validation before the
  runtime; grow modules per roadmap milestones, not ahead of them.
- **Consequence:** README Actions/Hardware tables describe target design; `main()`
  prints "Not yet implemented — see roadmap" outside `--dry-run`.

## Inherited / external decisions

- chrysa transverse "settled ADRs — do not relitigate" apply via the managed block in
  `CLAUDE.md` (`standards/rules/stack.md`). — FACT
- `handover.md` reports project profile, DDD level, and repo-local ADRs as
  "(not available)". — UNKNOWN (not recorded in-repo)

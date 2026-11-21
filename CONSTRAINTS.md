# Constraints — DIY Stream Deck

> Tag legend: FACT (stated/enforced in the repo), INFERENCE (deduced),
> UNKNOWN (not determinable from the repo).

## Platform & runtime

- **Cross-platform (Linux primary, Windows fully compatible).** No Linux-only code in
  core; platform-specific HID goes through an abstraction layer. — FACT (`CLAUDE.md`)
- **Python `>=3.14`** per `pyproject.toml`. `CLAUDE.md` states "Python 3.12+ minimum,
  target 3.14"; `README.md` badge says 3.14+. — FACT (see Contradictions in `REVIEW.md`)
- **Ruff `target-version = "py313"`** deliberately, with an inline note: ruff format
  ≤0.15.15 strips multi-`except` parens under `py314` — to be restored upstream. — FACT (`pyproject.toml`)

## Dependencies

- Runtime: `pyyaml>=6.0`, `requests>=2.32`, `pynput>=1.7`; optional `linux` extra adds
  `evdev>=1.7`. — FACT (`pyproject.toml`)
- HID input is imported conditionally by platform (`evdev` Linux / `pynput` cross-platform). — FACT (`CLAUDE.md`) / INFERENCE (backend not yet coded)

## Configuration

- All behaviour is YAML-driven; no hardcoded key bindings. — FACT (`CLAUDE.md`)
- Only the `device` section is enforced by code today; the wider schema (actions,
  home_assistant) is documented but not yet validated. — FACT (`__main__.py`)
- Home Assistant integration is optional — never required to start. — FACT (`CLAUDE.md`)

## Cost / hardware

- Target total hardware cost ≤ ~50 €. — FACT (`README.md`)

## Quality & process (chrysa standards)

- Test coverage gate ≥ 85 %. — FACT (`pyproject.toml`, `Makefile`)
- mypy `strict`; Ruff lint + format; custom quality gate (`scripts/quality_gate.py`
  baseline/verify). — FACT
- Tests are pytest-only and runnable in a container (`Dockerfile.test`). — FACT
- Lint runs in pre-commit locally and is replayed in CI only at release time; PR CI
  keeps tests + Sonar to limit per-push billing. — FACT (`.github/workflows/ci.yml` header)
- Repo inherits chrysa transverse standards via a managed block in `CLAUDE.md`
  (`distribute-standards.sh`). — FACT

## Security constraints

- HA credentials are supplied at runtime via environment/config
  (`${HA_TOKEN}` placeholder), never committed. — FACT (`README.md`)
- Shell-command and HTTP actions execute user-configured commands/requests — a config
  file is a trust boundary. Input-validation and command-execution hardening are
  design concerns for when those actions are implemented. — INFERENCE (see `SECURITY.md`)

# Testing — DIY Stream Deck

> Commands verified against `Makefile` and `pyproject.toml`. Coverage/pass numbers are
> not asserted here (not re-run during documentation); run the commands to confirm.

## Test suite (present)

- `tests/test_main.py` — unit tests for the CLI and `load_config()`:
  - `--dry-run` on a valid config returns 0 and prints "valid". — FACT
  - a missing config file makes `--dry-run` fail with a non-zero code. — FACT
  - malformed YAML makes `--dry-run` fail with a non-zero code. — FACT
  - a `--config`-required argparse error exits non-zero. — FACT
- `tests/__init__.py` — package marker.

No integration or hardware tests exist yet (device backends and actions are not
implemented).

## Commands

```bash
make test          # pytest tests/ -v
make test-cov      # pytest with coverage, xml + term-missing, --cov-fail-under=85
make docker-test   # build --target test (Dockerfile.test) and run tests in a container
make ci            # lint + format-check + typecheck + test-cov (full local gate)
```

Direct invocation: `pytest tests/ -v` (from `README.md` Development).

## Configuration

- pytest config in `pyproject.toml`: `testpaths = ["tests"]`, `test_*.py`,
  `--cov=diy_stream_deck --cov-report=xml --cov-report=term-missing --cov-fail-under=85`.
- `PLR2004` (magic values) is ignored in test files (`per-file-ignores`).
- Coverage source is `diy_stream_deck`, omitting `tests/*`.

## Gates

- **Coverage ≥ 85 %** or the run fails. — FACT (`--cov-fail-under=85`)
- **Quality gate:** `make quality-gate-baseline` / `make quality-gate-verify`
  (`scripts/quality_gate.py`).
- **CI:** `.github/workflows/ci.yml` runs tests + SonarCloud on PRs; lint/type gates run
  in pre-commit locally and at release time (per the workflow header comment). — FACT

## Debt

- Only the CLI/config path is covered; every roadmap feature (devices, actions, HA)
  will need its own tests as it lands. — INFERENCE

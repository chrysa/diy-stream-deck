---
# Copilot instructions for diy-stream-deck

## Project

DIY Stream Deck alternative — Python 3.12+, Linux/Windows cross-platform, YAML-driven key binding → action system with Home Assistant integration.

## Architecture rules

- Core engine in `core/` must remain platform-agnostic
- Hardware abstraction in `hardware/` — platform-specific imports must be conditional on `sys.platform`
- Action plugins in `actions/` must be independently testable (no hardware required)
- Configuration in `config/` — always load from YAML, never hardcode
- Use `pynput` as the cross-platform fallback; use `evdev` only on Linux

## Code standards

- Python 3.12+ syntax only
- Type annotations on all public functions
- `ruff` for lint and format — line length 100
- `pytest` for tests with `pytest-asyncio` for async tests
- No secrets in code — use environment variables only
- OWASP Top 10 compliance: validate all external inputs

## Testing

- Each action plugin must have unit tests in `tests/actions/`
- Hardware layer must have tests using the `virtual` device type
- Config loader must have schema validation tests

## Related patterns

- See `chrysa/github-actions` for shared CI actions
- See `chrysa/pre-commit-tools` for shared pre-commit hooks
- See `chrysa/shared-standards` for global Copilot instructions

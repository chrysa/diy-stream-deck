---
applyTo: "**/*.py"
description: "Python 3.14 coding guidelines for diy-stream-deck"
---
# Python Guidelines — diy-stream-deck

## Language version

- **Python 3.14** (minimum 3.12 for compatibility)
- `from __future__ import annotations` in **every** Python file
- Built-in generics: `list[str]`, `dict[str, int]`, `tuple[str, ...]`
- Union syntax: `str | None` (never `Optional[str]`)

## Typing

- ALL public functions fully type-annotated (parameters + return type)
- No `Any` unless absolutely necessary — use `object` or generics
- Use `Final` for constants: `DEFAULT_CONFIG_PATH: Final[Path] = Path("config.yaml")`
- `if typing.TYPE_CHECKING:` for import-time-only type references
- Pydantic models for config schema: `class KeyConfig(BaseModel):`

## Code style

- `ruff` — zero-tolerance, check before every commit (`ruff check --fix`)
- Line length: 100
- Entry point pattern: `main(argv: Sequence[str] | None = None) -> int`
- `logging` module only — never `print()` in production code
- Log levels: DEBUG for HID events, INFO for action execution, WARNING for config issues, ERROR for failures

## File / module conventions

```
diy_stream_deck/
  core/
    __init__.py
    event_loop.py       # KeyEvent dataclass, event dispatcher
    key_mapper.py       # YAML config → KeyMap[str, Action]
    action_runner.py    # ActionRunner: execute(action: Action) -> None
  actions/
    base.py             # Abstract Action protocol
    ha_service.py       # Home Assistant REST call
    shell_cmd.py        # subprocess (no shell=True)
    http_request.py     # httpx async GET/POST
    media_control.py    # platform-conditional
    hotkey.py           # pynput key sequence sender
  hardware/
    base.py             # InputDevice protocol
    macropad.py         # USB HID via evdev (Linux) / pynput (Windows)
    pico_w.py           # Raspberry Pi Pico W (WebSocket)
    virtual.py          # Software virtual device for tests
  config/
    schema.py           # Pydantic models for YAML structure
    loader.py           # load_config(path: Path) -> Config
```

## Async patterns

- Event loop in `core/event_loop.py` is `asyncio`-based
- Hardware polling runs in `asyncio.to_thread()` or dedicated thread
- Action execution: `await action_runner.execute(action)` — all actions are async
- Timeout: all external calls (HA, HTTP) must have explicit timeout (`httpx.AsyncClient(timeout=5.0)`)

## Security

- No secrets in YAML config — use `${ENV_VAR}` interpolation pattern
- HA token via `HA_TOKEN` env var, never hardcoded
- Validate all YAML inputs with Pydantic before use
- `subprocess` calls: always `list[str]` args, never `shell=True`

## Testing

- pytest + `pytest-asyncio` for async tests
- Hardware tests use `virtual` device type — no physical device required
- Mock HA client with `respx` or `unittest.mock`
- 100% tests passing before commit
- No `@pytest.mark.skip` without documented reason

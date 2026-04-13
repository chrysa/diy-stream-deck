---
applyTo: "diy_stream_deck/hardware/**,diy_stream_deck/actions/**,diy_stream_deck/core/**"
description: "Cross-platform abstraction rules, HID drivers, action plugin system"
---
# Platform Guidelines — diy-stream-deck

## Core principle: platform-agnostic core

`core/` must contain **zero** platform-specific imports.
All platform differences live in `hardware/` and `actions/`, behind the abstraction layer.

## HID abstraction — hardware/

### InputDevice protocol

Every hardware driver must implement this protocol:

```python
from __future__ import annotations
from typing import Protocol, AsyncIterator
from dataclasses import dataclass

@dataclass(frozen=True)
class KeyEvent:
    key_code: int
    pressed: bool  # True = keydown, False = keyup

class InputDevice(Protocol):
    async def events(self) -> AsyncIterator[KeyEvent]: ...
    async def close(self) -> None: ...
```

### Platform-conditional imports

```python
# hardware/macropad.py
from __future__ import annotations
import sys

if sys.platform == "linux":
    import evdev  # type: ignore[import]
elif sys.platform == "win32":
    from pynput import keyboard  # type: ignore[import]
else:
    raise ImportError(f"Unsupported platform: {sys.platform}")
```

**Never** do bare `import evdev` at module top-level — always guard with `sys.platform`.

### Available hardware drivers

| Driver | File | Platform | Description |
|---|---|---|---|
| macropad | `hardware/macropad.py` | Linux + Windows | USB HID macropad |
| pico_w | `hardware/pico_w.py` | Any | Raspberry Pi Pico W (WebSocket) |
| virtual | `hardware/virtual.py` | Any | Software device for testing |

## Action plugin system — actions/

### Action protocol

```python
from __future__ import annotations
from typing import Protocol

class Action(Protocol):
    async def execute(self) -> None: ...
    def describe(self) -> str: ...  # human-readable description for logs
```

### Available action plugins

| Plugin | Class | Config key | Description |
|---|---|---|---|
| ha_service | `HAServiceAction` | `ha_service` | Home Assistant REST service call |
| shell_cmd | `ShellCmdAction` | `shell_cmd` | Shell command (no `shell=True`) |
| http_request | `HttpRequestAction` | `http_request` | GET/POST HTTP request |
| media_control | `MediaControlAction` | `media_control` | Play/pause/volume (platform-conditional) |
| hotkey | `HotkeyAction` | `hotkey` | Key sequence via pynput |

### Adding a new action plugin

1. Create `actions/my_action.py` with a class implementing `Action` protocol
2. Add Pydantic model to `config/schema.py`
3. Register in `actions/__init__.py` plugin registry
4. Add unit tests in `tests/actions/test_my_action.py`
5. Document in `README.md` under "Available actions"

## YAML config schema

```yaml
# config.yaml — minimal example
version: "1"
device:
  type: macropad           # macropad | pico_w | virtual
  path: /dev/input/event3  # Linux only — omit on Windows

bindings:
  KEY_KP1:
    - type: ha_service
      entity: light.desk
      service: light.toggle

  KEY_KP2:
    - type: shell_cmd
      command: ["notify-send", "Hello"]

  KEY_KP3:
    - type: hotkey
      keys: ["ctrl", "shift", "t"]
```

Always validate config on load with Pydantic — raise `ConfigValidationError` with field path on failure.

## Home Assistant integration

- HA integration is **optional** — app starts without it (graceful degradation)
- On `ha_service` action with no HA config: log WARNING and skip execution
- HA token via `HA_TOKEN` env var — never in config.yaml
- Use `httpx.AsyncClient` with `timeout=5.0` — catch `httpx.TimeoutException` and log ERROR

## Media control — platform handling

```python
# actions/media_control.py
import sys
from __future__ import annotations

if sys.platform == "linux":
    async def _send(cmd: str) -> None:
        await asyncio.to_thread(subprocess.run, ["playerctl", cmd], check=False)
elif sys.platform == "win32":
    async def _send(cmd: str) -> None:
        from pynput.keyboard import Key, Controller  # type: ignore[import]
        ctrl = Controller()
        KEY_MAP = {"play-pause": Key.media_play_pause, ...}
        ctrl.press(KEY_MAP[cmd])
```

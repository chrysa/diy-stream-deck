# Glossary — DIY Stream Deck

> Terms as used in this repository. Definitions grounded in `README.md`, `CLAUDE.md`,
> and the source.

- **Stream Deck** — a physical grid of programmable keys (originally an Elgato product)
  that triggers actions; this project is an open, cross-platform alternative.
- **Action** — a task bound to a key. Types: `ha_service`, `shell_cmd`,
  `http_request`, `media_control`, `hotkey`. — FACT (`README.md`)
- **`ha_service`** — an action that calls a Home Assistant service (e.g. `light.toggle`).
- **`shell_cmd`** — an action that runs a shell command.
- **`http_request`** — an action that sends an HTTP GET/POST.
- **`media_control`** — an action that emits a media key (e.g. play/pause).
- **`hotkey`** — an action that sends a keyboard shortcut.
- **Device / backend** — the physical input source. Types: `macropad`, `pico-w`,
  `virtual`. Declared in the config `device.type`. — FACT
- **`macropad`** — a small USB HID keypad (plug-and-play).
- **`pico-w`** — a Raspberry Pi Pico W running custom firmware for wireless input.
- **`virtual`** — a software-only device for testing without hardware.
- **`device` section** — the required top-level YAML key; the only part enforced by the
  current config validator. — FACT (`__main__.py`)
- **`--dry-run`** — CLI flag that validates the config and exits without starting.
- **`ConfigError`** — the typed exception raised by `load_config()` on an invalid config.
- **Home Assistant (HA)** — the home-automation platform this project optionally targets
  via its HTTP API and a long-lived access token.
- **Quality gate** — `scripts/quality_gate.py` baseline/verify check enforced in the dev
  loop and CI.
- **Managed standards block** — the `chrysa:standards` region in `CLAUDE.md`, generated
  by `distribute-standards.sh`; do not hand-edit.

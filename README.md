# DIY Stream Deck

[![CI](https://github.com/chrysa/diy-stream-deck/actions/workflows/ci.yml/badge.svg)](https://github.com/chrysa/diy-stream-deck/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey)](https://github.com/chrysa/diy-stream-deck)

> DIY Stream Deck alternative — fully compatible with Linux and Windows. Maps physical inputs (macro pad, Raspberry Pi Pico W, or repurposed tablet) to custom actions with Home Assistant integration.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Hardware Options](#hardware-options)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Actions](#actions)
- [Home Assistant Integration](#home-assistant-integration)
- [Development](#development)
- [Roadmap](#roadmap)

---

## Overview

This project builds a fully open-source Stream Deck alternative that works on Linux and Windows without vendor lock-in. It supports multiple hardware form factors and provides a flexible action/key-mapping system configurable via YAML.

### Goals

- Replace proprietary Stream Deck software with an open, cross-platform solution
- Support Linux (primary) and Windows (fully compatible)
- Integrate natively with Home Assistant
- Allow custom action plugins (scripts, HTTP calls, HA services, macros)
- Keep cost under 50 € with commodity hardware

---

## Architecture

```
hardware/          # Hardware abstraction layer (HID, Pico W, virtual)
  pico-w/          # MicroPython firmware for Raspberry Pi Pico W
  macropad/        # Support for USB macropad HID devices
  virtual/         # Virtual device for testing (no hardware required)

core/              # Core engine
  engine.py        # Main event loop and action dispatcher
  key_mapper.py    # Key binding resolution
  action_runner.py # Action executor (async)

actions/           # Built-in action plugins
  ha_service.py    # Home Assistant service call
  shell_cmd.py     # Execute shell command
  http_request.py  # HTTP GET/POST
  media_control.py # Media keys (play/pause/volume)
  hotkey.py        # Send keyboard shortcut to OS

config/            # Configuration layer
  schema.py        # YAML config schema validation
  loader.py        # Config loader with hot-reload

ui/                # Optional display and feedback
  tray.py          # System tray icon (Linux/Windows)

tests/             # Unit and integration tests
docs/              # Architecture, setup, hardware guides
```

---

## Hardware Options

| Option | Cost | Difficulty | Notes |
|--------|------|------------|-------|
| USB macropad (mini keyboard) | 7–20 € | Easy | Plug-and-play HID device |
| Raspberry Pi Pico W | 10–20 € | Medium | Wireless, custom firmware |
| Old Android tablet/phone | 0–30 € | Medium | Touch display via ADB or web UI |

**Recommended start**: USB macropad — cheapest, most portable, works instantly on Linux and Windows.

---

## Requirements

- Python 3.12+
- `evdev` (Linux) or `pynput` (Windows/cross-platform) for HID input
- `requests` for HTTP actions and Home Assistant API
- `pyyaml` for configuration
- Home Assistant instance (optional, for HA actions)

---

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Copy example config
cp config/examples/macropad.yml config/diy-stream-deck.yml

# Edit key bindings
vim config/diy-stream-deck.yml

# Run
python -m diy_stream_deck --config config/diy-stream-deck.yml
```

---

## Configuration

Key bindings are defined in YAML:

```yaml
device:
  type: macropad       # macropad | pico-w | virtual
  id: "auto"           # auto-detect or specific device path

actions:
  key_1:
    label: "Toggle Living Room Light"
    type: ha_service
    service: light.toggle
    entity_id: light.living_room

  key_2:
    label: "Open Terminal"
    type: shell_cmd
    command: "xterm"

  key_3:
    label: "Play/Pause"
    type: media_control
    action: play_pause

home_assistant:
  url: "http://homeassistant.local:8123"
  token: "${HA_TOKEN}"
```

---

## Actions

| Type | Description | Platforms |
|------|-------------|-----------|
| `ha_service` | Call a Home Assistant service | Linux, Windows |
| `shell_cmd` | Execute a shell command | Linux, Windows |
| `http_request` | Send HTTP GET/POST | Linux, Windows |
| `media_control` | Media key press | Linux, Windows |
| `hotkey` | Send keyboard shortcut | Linux, Windows |

---

## Home Assistant Integration

Set your HA URL and long-lived access token:

```bash
export HA_URL="http://homeassistant.local:8123"
export HA_TOKEN="your-long-lived-access-token"
```

---

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check .
ruff format --check .

# Pre-commit
pre-commit install
pre-commit run --all-files
```

---

## Roadmap

See [GitHub Issues](https://github.com/chrysa/diy-stream-deck/issues) for the full roadmap.

Key milestones:
1. **v0.1** — USB macropad HID input + basic action runner + HA service calls
2. **v0.2** — Pico W firmware + wireless mode
3. **v0.3** — System tray UI + config hot-reload
4. **v0.4** — Windows full compatibility + packaging
5. **v1.0** — Tablet UI + full documentation

---

## Cost Estimate

| Component | Min | Max |
|-----------|-----|-----|
| USB macropad | 7 € | 20 € |
| Raspberry Pi Pico W | 5 € | 10 € |
| Cables and accessories | 2 € | 10 € |
| **Total** | **7 €** | **50 €** |

Time estimate: 22–43 hours for full v1 implementation.

---

## Related

- [Notion project page](https://www.notion.so/33759293e35e812f8d14ea4ea23618cf)
- [chrysa/D-D](https://github.com/chrysa/D-D) — Home automation infrastructure

DIY Stream Deck alternative compatible with Linux and Windows — key mapping, action system, Home Assistant integration

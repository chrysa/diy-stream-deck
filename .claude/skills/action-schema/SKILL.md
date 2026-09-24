---
description: 'YAML config/action schema knowledge for diy-stream-deck: the device section, the per-action-type mapping shape (ha_service, shell_cmd, http_request, media_control, hotkey), and validation rules. Load in background when reading or extending the config loader (currently `diy_stream_deck/__main__.py::load_config` / `ConfigError`), and invoke `/action-schema` when adding a new action type or config field.'
---

# Action schema — diy-stream-deck config contract

The YAML config is the project's central contract (see `CLAUDE.md`: "YAML config
drives everything — no hardcoded key bindings"). This skill documents its shape so
new fields/action types stay consistent with the existing loader instead of being
re-derived from scratch each session.

## Top-level structure

```yaml
device:        # required — hardware section, validated first
  type: macropad | pico-w | virtual
  ...           # type-specific fields, TBD as hardware/ is implemented

actions:        # mapping of input id -> action config (not yet implemented)
  <input_id>:
    type: ha_service | shell_cmd | http_request | media_control | hotkey
    ...         # type-specific fields below
```

Today (`diy_stream_deck/__main__.py::load_config`) only validates:
- the file loads as YAML and parses to a mapping (`ConfigError` otherwise),
- a top-level `device` key is present.

Everything below is the target shape from `CLAUDE.md`'s architecture section —
apply it when `actions/` and the per-type plugins are implemented.

## Action types (one example each)

```yaml
# ha_service — Home Assistant service call
type: ha_service
domain: light
service: turn_on
entity_id: light.desk

# shell_cmd — arbitrary shell command (injection surface — see cross-platform-check
# skill and the report's deferred security-reviewer subagent note)
type: shell_cmd
command: "notify-send 'hello'"

# http_request
type: http_request
method: POST
url: "https://example.com/webhook"
body: {}

# media_control
type: media_control
action: play_pause | next | previous | volume_up | volume_down

# hotkey
type: hotkey
keys: ["ctrl", "shift", "a"]
```

## Validation rules to preserve when extending the loader

- Raise `ConfigError` (never a bare exception) for any structurally invalid config —
  keep the daemon's single error type at the config boundary.
- `device` section required; missing it is already enforced — extend the same
  `if "field" not in data` pattern for new required top-level sections (e.g. `actions`).
- Each action's `type` must be one of the five known values — reject unknown types
  with a `ConfigError` naming the input id and the bad type, not a silent skip.
- No action type may assume Linux or Windows-only behavior in its schema (e.g. a
  `shell_cmd` field must not encode a POSIX-only shell) — see `cross-platform-check`.

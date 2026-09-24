---
description: 'Linux/Windows parity checklist for diy-stream-deck. Run before finishing any change that touches `diy_stream_deck/core/`, `diy_stream_deck/hardware/`, or any other platform-crossing code, to enforce the CLAUDE.md rule "must run on Linux AND Windows, no Linux-only code in core."'
---

# Cross-platform check — Linux + Windows parity

`CLAUDE.md` states the single hardest, most-repeated-risk rule for this repo:
**no Linux-only code in core; use an abstraction layer.** This skill turns that
into a checklist to run before calling platform-touching work done.

## Checklist

- **Paths**: `pathlib.Path` only — no manual `/`-joined strings, no hardcoded
  `/dev/...` or `C:\...` paths outside a named platform module.
- **HID/serial imports**: `evdev` (Linux) and `pynput` (Windows) are imported
  conditionally by platform per `CLAUDE.md` — never unconditionally at module
  top-level in `core/`. Confine platform-specific imports to `hardware/<platform>.py`
  and expose a platform-neutral interface from `hardware/__init__.py`.
- **POSIX-only stdlib**: `fcntl`, `termios`, `pwd`, `grp`, `os.fork`, `signal.SIGHUP`
  outside an explicitly-named platform module (`hardware/linux_*.py`) is a violation.
- **Process/service model**: don't assume systemd or a POSIX daemon model in
  `core/` — a Windows service or plain foreground process must also work.
- **Line endings / encoding**: read/write text with explicit `encoding="utf-8"`
  (already done in `load_config`); don't rely on platform default text mode.
- **Shell commands** (`shell_cmd` action type): don't hardcode `/bin/sh` or bash-only
  syntax — use `subprocess` with `shell=True` and the OS default shell, or split
  into an explicit list understood on both platforms.

## When to run this

- Before finishing any edit under `diy_stream_deck/core/` or `diy_stream_deck/hardware/`.
- Before adding a new action type that shells out or touches file paths/hotkeys.
- The `cross-platform-guard` PostToolUse hook already flags the import-level version
  of this mechanically; this skill covers the broader review (process model, shell
  syntax, path handling) a grep-based hook can't catch.

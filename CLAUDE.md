# CLAUDE.md — diy-stream-deck

## Project Purpose

DIY Stream Deck alternative compatible with Linux and Windows. Maps physical inputs (USB macropad, Raspberry Pi Pico W, virtual) to configurable actions: Home Assistant service calls, shell commands, HTTP requests, media controls, and keyboard shortcuts.

## Architecture

- `core/` — event loop, key mapper, action runner
- `actions/` — action plugins (ha_service, shell_cmd, http_request, media_control, hotkey)
- `hardware/` — HID abstraction (macropad, pico-w, virtual)
- `config/` — YAML schema and loader
- `ui/` — optional system tray
- `tests/` — unit and integration tests

## Key Constraints

- Python 3.12+ minimum, target 3.14
- Must run on Linux AND Windows (no Linux-only code in core; use abstraction layer)
- `evdev` for Linux HID — `pynput` for Windows HID — imported conditionally by platform
- Home Assistant integration is optional — never required to start
- YAML config drives everything — no hardcoded key bindings
- Actions must be pluggable and independently testable

## Development Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check .
ruff format --check .
pre-commit run --all-files
```

## Related repositories

- `chrysa/D-D` — home automation infrastructure
- `chrysa/github-actions` — shared CI actions
- `chrysa/pre-commit-tools` — shared pre-commit hooks
- `chrysa/shared-standards` — Copilot instructions and standards

## Notion

Project tracking: https://www.notion.so/33759293e35e812f8d14ea4ea23618cf

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **diy-stream-deck** (50 symbols, 42 relationships, 0 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/diy-stream-deck/context` | Codebase overview, check index freshness |
| `gitnexus://repo/diy-stream-deck/clusters` | All functional areas |
| `gitnexus://repo/diy-stream-deck/processes` | All execution flows |
| `gitnexus://repo/diy-stream-deck/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->

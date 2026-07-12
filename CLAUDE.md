# CLAUDE.md — diy-stream-deck

> **Claude Code**: also read `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` for code specifications.

## Project Purpose

DIY Stream Deck alternative compatible with Linux and Windows. Maps physical inputs (USB macropad, Raspberry Pi Pico W, virtual) to configurable actions: Home Assistant service calls, shell commands, HTTP requests, media controls, and keyboard shortcuts.


## Language Rules

- Language: English — all code, comments, documentation, instructions, and configuration files must be in English.
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

## Skills

Shared skills from `shared-standards/.claude/skills/`:

- `ui-ux/SKILL.md` — UX/UI/ergonomics across ALL surfaces (web, CLI, VS Code, Discord, desktop, game, agent) + WCAG 2.1 AA + dark mode + i18n FR+EN (load when building any human-facing surface)

<!-- chrysa:standards-import:start -->
@.chrysa/STANDARDS.md
<!-- chrysa:standards-import:end -->

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

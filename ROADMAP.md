# Roadmap — DIY Stream Deck

> Reproduced from `README.md` (Roadmap) and cross-checked against the code. The full
> live backlog is the [GitHub Issues](https://github.com/chrysa/diy-stream-deck/issues)
> tracker; this file summarises the declared milestones. Only real, in-repo/declared
> items are listed.

## Current state

Early scaffold — CLI entry point + YAML config validation (`--dry-run`) implemented.
The runtime action engine, device backends, and Home Assistant actions are not yet
built. — FACT (`ARCHITECTURE.md`, `main()` stub)

## Declared milestones (from README)

| Milestone | Scope | Status |
|-----------|-------|--------|
| v0.1 | USB macropad HID input + basic action runner + HA service calls | Not started (scaffold only) |
| v0.2 | Raspberry Pi Pico W firmware + wireless mode | Planned |
| v0.3 | System-tray UI + config hot-reload | Planned |
| v0.4 | Windows full compatibility + packaging | Planned |
| v1.0 | Tablet UI + full documentation | Planned |

## Estimates (from README)

- Total effort: ~22–43 hours for a full v1 implementation. — FACT (`README.md`)
- Hardware cost: 7–50 €. — FACT (`README.md` Cost Estimate)

## Notes

- Status labels beyond "scaffold only" reflect the README's declared plan, not tracked
  progress; consult GitHub Issues for authoritative state. — INFERENCE
- `CHANGELOG.md` is git-cliff-generated and currently shows only `[Unreleased]`. — FACT

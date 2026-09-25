# Documentation Review — DIY Stream Deck

> Meta-review produced during the documentation pass. Records what exists, what was
> added, contradictions found, and open UNKNOWNs. No source, tests, deps, CI, or config
> were modified.

## Existing docs (preserved)

- `README.md` — thorough; overview, architecture (target), hardware, config, actions,
  HA, dev, roadmap, cost. Accurately flags "early scaffold" status.
- `ARCHITECTURE.md` — grounded, honest about scaffold vs target; notes the Python-version
  discrepancy.
- `CLAUDE.md` — purpose, constraints, dev commands, related repos + managed standards
  block.
- `AGENTS.md`, `CONTRIBUTING.md`, `handover.md`, `CHANGELOG.md`, `ai-instructions.md`,
  `llms-full.txt`, `docs/reference/github-inspiration.md` — present, consistent.
- `legal/mentions-legales.md`, `legal/cgu.md` — `/cgu`-skill drafts with `[À COMPLÉTER]`
  placeholders (see debt).

## Docs generated this pass (root)

| File | Why |
|------|-----|
| `REQUIREMENTS.md` | No consolidated REQ list existed; extracted PROD/TECH reqs + IMPLEMENTED matrix. |
| `CONSTRAINTS.md` | Constraints were scattered across README/CLAUDE/pyproject; consolidated + tagged. |
| `DECISIONS.md` | No ADR log in-repo; reconstructed from evidence. |
| `TESTING.md` | Verified test commands and gates in one place. |
| `SECURITY.md` | Secret-scan result + forward-looking design findings. |
| `ROADMAP.md` | Milestones summarised from README + code status. |
| `GLOSSARY.md` | Domain vocabulary (actions, devices, config terms). |
| `REVIEW.md` | This meta-review. |

## Docs skipped (recorded)

- **PRD / TRD** — content would duplicate `README.md` + `REQUIREMENTS.md` for a
  single-CLI scaffold; not justified. Skipped.
- **OBSERVABILITY.md** — no logging/metrics/tracing implemented yet (only stdout/stderr
  writes in `main()`); nothing verifiable to document. Skipped (record: revisit when the
  runtime lands).

## Contradictions found

1. **Minimum Python version.** `pyproject.toml` sets `requires-python = ">=3.14"` and the
   README badge says 3.14+, but `CLAUDE.md` states "Python 3.12+ minimum, target 3.14".
   Per the "trust the manifest" rule, **3.14** is authoritative. `ARCHITECTURE.md`
   already flags this. Not fixed (docs-only; owner should reconcile `CLAUDE.md`).
2. **Ruff target vs runtime.** Ruff `target-version = "py313"` while runtime is 3.14 —
   this is intentional (documented formatter-bug workaround in `pyproject.toml`), not a
   true contradiction.

## Key UNKNOWNs

- Project **profile** and **DDD level** — `handover.md` reports "(not available)".
- Repo-local **ADRs** — none recorded in-repo ("(not available)").
- Actual **coverage %** and CI pass state — not re-run during this docs pass.

## Documentation debt

- Complete the `legal/` drafts (remove all `[À COMPLÉTER]`) before publication.
- Reconcile the Python-minimum statement in `CLAUDE.md` with `pyproject.toml`.
- Regenerate context files (`handover.md`, `llms-full.txt`) once profile/DDD/ADRs are set
  (`make gen-context-files`).
- Expand `TESTING.md` and the implementation matrix as roadmap features land.

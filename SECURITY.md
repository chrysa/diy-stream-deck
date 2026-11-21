# Security — DIY Stream Deck

> Documentation-only review. No code was changed. Secrets are never reproduced here:
> findings reference location and nature only. Severity uses HIGH / MEDIUM / LOW /
> INFO. This repo is an early scaffold, so most items are forward-looking design
> concerns for features not yet implemented.

## Secret scan

- **No hardcoded secrets, keys, tokens, or passwords found** in tracked source, config,
  or fixtures. — FACT
- Home Assistant credentials appear only as placeholders: `${HA_TOKEN}` in the README
  config example and `your-long-lived-access-token` in the env example. This is the
  correct pattern (runtime env/config injection). — FACT, INFO
- `.mcp.json` at root references credentials only through env placeholders
  (`${GITHUB_TOKEN}`, `${NOTION_API_KEY}`) — no committed tokens. — FACT

## Design-level findings (for when features land)

| # | Severity | Area | Finding | Note (owner to address in code, not here) |
|---|----------|------|---------|-------------------------------------------|
| S1 | MEDIUM (future) | `shell_cmd` action | A config-driven action will execute arbitrary shell commands. The YAML config is a trust boundary; a malicious/edited config yields arbitrary code execution as the running user. | When implementing: avoid `shell=True` with interpolation, validate/allowlist, document the trust model. Not present yet. |
| S2 | MEDIUM (future) | `http_request` / `ha_service` | Outbound HTTP with user-supplied URLs and a bearer token. | Enforce TLS for non-loopback, avoid logging the token, treat URL as untrusted (SSRF awareness). |
| S3 | LOW (future) | HA token handling | Long-lived token read from env/config. | Never log it; support it only via env/secret, not inline in committed configs. |
| S4 | INFO (satisfied) | Config parsing | Config is parsed with `yaml.safe_load` (not `yaml.load`), validated structurally, and raises a typed `ConfigError`. | Confirmed in `diy_stream_deck/__main__.py:30`. |

No HIGH or CRITICAL findings were identified in the current tree.

## Documentation debt (not a security finding)

- `legal/mentions-legales.md` and `legal/cgu.md` are `/cgu`-skill drafts containing
  `[À COMPLÉTER]` placeholders and an explicit "do not publish with placeholders"
  banner (LCEN art. 6-III). These must be completed by the owner before any public
  publication. — FACT

## Owner action

- Track S1–S3 as security acceptance criteria on the corresponding roadmap milestones.
- Complete the `legal/` drafts before any public publication.

#!/usr/bin/env node
/**
 * Cross-platform guard — PostToolUse hook (file writes).
 *
 * Enforces the diy-stream-deck CLAUDE.md rule "must run on Linux AND Windows,
 * no Linux-only code in core": flags POSIX-only stdlib imports (fcntl, termios,
 * pwd, grp) or unconditional evdev/pynput imports in files under
 * diy_stream_deck/core/ or diy_stream_deck/__main__.py, outside a module whose
 * name signals it's an explicit platform-abstraction layer
 * (hardware/, *_linux.py, *_windows.py, *linux*, *windows*).
 *
 * Hook type: PostToolUse — target: Write, Edit, MultiEdit
 * Does NOT block (informative only — exit 0). Prints warnings to stderr.
 */

"use strict";

const fs = require("fs");

const CORE_PATH_RE = /diy_stream_deck\/(core|__main__\.py)/;
const PLATFORM_MODULE_RE = /hardware\/|_linux\.py|_windows\.py|linux|windows/i;
const POSIX_ONLY_RE = /^\s*(import|from)\s+(fcntl|termios|pwd|grp)\b/m;
const UNCONDITIONAL_HID_IMPORT_RE = /^\s*(import|from)\s+(evdev|pynput)\b/m;

function readStdinJson() {
  try {
    return JSON.parse(fs.readFileSync(0, "utf8"));
  } catch {
    return null;
  }
}

function main() {
  const input = readStdinJson();
  if (!input) process.exit(0);

  const filePath = input.tool_input?.file_path ?? "";
  if (!filePath.endsWith(".py")) process.exit(0);
  if (!CORE_PATH_RE.test(filePath)) process.exit(0);
  if (PLATFORM_MODULE_RE.test(filePath)) process.exit(0);

  let content;
  try {
    content = fs.readFileSync(filePath, "utf8");
  } catch {
    process.exit(0);
  }

  const warnings = [];
  if (POSIX_ONLY_RE.test(content)) {
    warnings.push(
      "imports a POSIX-only stdlib module (fcntl/termios/pwd/grp) outside a " +
        "platform-abstraction module"
    );
  }
  if (UNCONDITIONAL_HID_IMPORT_RE.test(content)) {
    warnings.push(
      "imports evdev/pynput unconditionally — CLAUDE.md requires these be " +
        "imported conditionally by platform, confined to hardware/"
    );
  }

  if (warnings.length) {
    process.stderr.write(
      `cross-platform-guard: ${filePath} ${warnings.join("; ")}. ` +
        "See CLAUDE.md 'Key Constraints' and the cross-platform-check skill.\n"
    );
  }
  process.exit(0);
}

main();

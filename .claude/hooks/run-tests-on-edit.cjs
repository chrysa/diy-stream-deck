#!/usr/bin/env node
/**
 * Run tests on edit — PostToolUse hook (file writes under diy_stream_deck/).
 *
 * pyproject.toml already sets --cov-fail-under=85 in [tool.pytest.ini_options]
 * addopts, but nothing ran it automatically after an edit. This runs `pytest`
 * right after a write/edit under diy_stream_deck/, so a coverage or test
 * regression surfaces immediately instead of at CI.
 *
 * Hook type: PostToolUse — target: Write, Edit, MultiEdit
 * Does NOT block (informative only — exit 0). Prints failures to stderr.
 * Best-effort: skipped if pytest isn't on PATH or the repo has no tests/ yet.
 */

"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const SCOPE_RE = /diy_stream_deck\/.*\.py$/;

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
  if (!SCOPE_RE.test(filePath)) process.exit(0);

  const root = process.env.CLAUDE_PROJECT_DIR ?? process.cwd();
  if (!fs.existsSync(path.join(root, "tests"))) process.exit(0);

  const result = spawnSync("pytest", ["tests/", "-q"], {
    cwd: root,
    encoding: "utf8",
    timeout: 60000,
  });

  if (result.error) process.exit(0); // pytest not available — best-effort, skip
  if (result.status !== 0) {
    process.stderr.write(
      `run-tests-on-edit: pytest failed after editing ${filePath} ` +
        "(coverage gate is --cov-fail-under=85 per pyproject.toml):\n" +
        `${(result.stdout || "").slice(-2000)}\n${(result.stderr || "").slice(-1000)}\n`
    );
  }
  process.exit(0);
}

main();

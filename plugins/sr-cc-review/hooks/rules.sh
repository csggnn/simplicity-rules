#!/usr/bin/env bash
# SessionStart hook: prints rules.md. Claude Code adds the output to the session context.
set -euo pipefail
cat "$(dirname "$0")/../rules.md"

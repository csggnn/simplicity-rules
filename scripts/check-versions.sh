#!/usr/bin/env bash
# Compare installed tool versions against the minimums in versions.toml.
# Exit status is 1 when a tool is missing or older than its minimum.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
status=0

installed() {
    case "$1" in
        claude) claude --version ;;
    esac </dev/null 2>/dev/null | grep -oE '[0-9]+(\.[0-9]+)+' | head -n1
}

while IFS='=' read -r tool min; do
    tool=$(echo "$tool" | tr -d ' ')
    min=$(echo "$min" | tr -d ' "')
    have=$(installed "$tool" || true)
    if [ -z "$have" ]; then
        echo "missing: $tool (minimum $min)"
        status=1
    elif [ "$(printf '%s\n%s\n' "$min" "$have" | sort -V | head -n1)" != "$min" ]; then
        echo "too old: $tool $have (minimum $min)"
        status=1
    else
        echo "ok: $tool $have (minimum $min)"
    fi
done < <(sed -n '/^\[tools\]/,/^\[/{/^[a-z]/p}' "$root/versions.toml")

exit $status

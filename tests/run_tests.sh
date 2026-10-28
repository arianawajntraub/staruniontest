#!/usr/bin/env bash
# E2E Test Suite Runner Wrapper for Star Union S.R.L.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"
python3 "$SCRIPT_DIR/run_tests.py" "$@"

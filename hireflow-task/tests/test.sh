#!/usr/bin/env bash
set -euo pipefail

if command -v python >/dev/null 2>&1; then
  python test_outputs.py
else
  python3 test_outputs.py
fi

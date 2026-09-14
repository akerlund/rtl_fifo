#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CORE="akerlund::fifo_example_py:0"

export PYTHONPATH="${SCRIPT_DIR}/tb:${SCRIPT_DIR}/tc${PYTHONPATH:+:${PYTHONPATH}}"

if [ "$#" -eq 0 ]; then
  fusesoc --cores-root "${REPO_ROOT}" run --target sim "${CORE}"
else
  fusesoc --cores-root "${REPO_ROOT}" run "$@" "${CORE}"
fi

#!/usr/bin/env bash
# Regenerates the README demo GIFs with vhs (https://github.com/charmbracelet/vhs).
# Usage, from the repo root:   ./docs/demo/record.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

if ! command -v vhs >/dev/null 2>&1; then
  echo "vhs is required: brew install vhs" >&2
  exit 1
fi

# The recorded shell must see latex-forge and the TeX toolchain.
if ! command -v latex-forge >/dev/null 2>&1; then
  echo "latex-forge must be on PATH (pipx install latex-forge)" >&2
  exit 1
fi
if [ -d /Library/TeX/texbin ]; then
  export PATH="$PATH:/Library/TeX/texbin"
fi

mkdir -p docs/assets

for tape in docs/demo/*.tape; do
  echo "Recording $tape …"
  vhs "$tape"
done

echo "Done. GIFs written to docs/assets/."

#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
command -v latexmk >/dev/null || {
  echo "latexmk is required. Install TeX Live or MacTeX." >&2
  exit 1
}
if [ "$#" -eq 0 ]; then set -- main; fi
case "$1" in
  main) latexmk main.tex ;;
  anonymous) latexmk anonymous.tex ;;
  clean) latexmk -c main.tex anonymous.tex ;;
  *) echo "Usage: bash build.sh [main|anonymous|clean]" >&2; exit 2 ;;
esac

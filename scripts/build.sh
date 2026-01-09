#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

VERSION=""

usage() {
  cat <<EOF
Usage: $(basename "$0") -v <version> | --version <version>
Example: $(basename "$0") -v v1.2.3
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--version) VERSION="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "Missing required argument: -v/--version" >&2
  usage
  exit 2
fi

# Normalize v/V prefix for python packaging
VER_STRIPPED="$(printf '%s' "$VERSION" | sed -E 's/^[[:space:]]*[vV]//; s/^[[:space:]]+//; s/[[:space:]]+$//')"

export SETUPTOOLS_SCM_PRETEND_VERSION="$VER_STRIPPED"

python -m PyInstaller "$ROOT_DIR/cobertura_console_reporter/__main__.py" \
  --name ccr \
  --onefile \
  --version-file "$ROOT_DIR/build/version.txt" \
  --copy-metadata cobertura-console-reporter

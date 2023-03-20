#!/usr/bin/env bash

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pyinstaller "$ROOT_DIR/cobertura_console_reporter/__main__.py" --name ccr --onefile

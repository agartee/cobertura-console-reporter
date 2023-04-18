#!/usr/bin/env bash

GRAY="\033[0;30m"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
MAGENTA="\033[0;35m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS_DIR="$ROOT_DIR/tests"

echo -e "${BLUE}Tests:${NC}" 
echo

coverage run -m pytest "$TESTS_DIR" -v --no-header --capture=no

echo
echo -e "${BLUE}Test Coverage:${NC}" 
echo

coverage report -m

echo
echo -e "${BLUE}Linting:${NC}" 

pylint "$ROOT_DIR/cobertura_console_reporter"

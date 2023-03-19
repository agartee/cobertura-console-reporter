#!/usr/bin/env bash

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GRAY="\033[0;30m"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
MAGENTA="\033[0;35m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# **************************************************************************************
# Ensure Script is Sourced (remove if debugging this script)
# **************************************************************************************
if [ "${BASH_SOURCE[0]}" -ef "$0" ]; 
    then echo -e "${RED}ERROR: In order for the Python virtual environment to remain" \
        "active, this script must be sourced.${NC}"
    exit 1
fi

# **************************************************************************************
# Check Python Installation
# **************************************************************************************
MIN_PYTHON_VERSION="3.9.9"

# note: 2> /dev/null suppresses stderr (the error message)
CURRENT_PYTHON_VERSION=$(python --version 2> /dev/null)
if [ -z "$CURRENT_PYTHON_VERSION" ]
    then echo -e "${RED}Python installation not found" \
        "(minimum: ${MIN_PYTHON_VERSION}).${NC}"
    exit 1
fi

CURRENT_PYTHON_VERSION="${CURRENT_PYTHON_VERSION/Python /""}"
if $(dpkg --compare-versions "${CURRENT_PYTHON_VERSION}" "lt" "${MIN_PYTHON_VERSION}")
    then echo -e "${RED}Current Python version not supported" \
        "(found: ${CURRENT_PYTHON_VERSION}; " \
        "minimum: ${MIN_PYTHON_VERSION}).${NC}"
    exit 1
fi

echo -e "${GREEN}Python installation found: ${CURRENT_PYTHON_VERSION}" \
    "(minimum: ${MIN_PYTHON_VERSION}).${NC}" 

# **************************************************************************************
# Create and Activate Python Virtual Environment
# **************************************************************************************
VENV_PATH="$ROOT_DIR/.venv"

if [ -d "$VENV_PATH" ]
    then 
        echo -e "${GREEN}Python virtual environment detected.${NC}"
    else
        python -m venv "$ROOT_DIR/.venv"
        echo -e "${GREEN}Python virtual environment created.${NC}"
fi

. "$VENV_PATH/bin/activate"
echo -e "${GREEN}Python virtual environment activated.${NC}"

# **************************************************************************************
# Install Python Development Dependencies
# **************************************************************************************
python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r "${ROOT_DIR}/requirements-dev.txt" > /dev/null 2>&1

echo -e "${GREEN}Python development dependencies installed.${NC}"

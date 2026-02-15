#!/bin/bash
set -e

# setup.sh: Prepare development environment for agent governance pack improvements.

echo "--- Setting up Agent Governance Pack Development Environment ---"

# 1. Install/Update Python dependencies
echo "Installing/Updating Python dependencies (ruff, pre-commit, pytest)..."
pip install -q ruff pre-commit pytest

# 2. Install pre-commit hooks
if [ -d .git ]; then
    echo "Installing pre-commit hooks..."
    pre-commit install
else
    echo "Skipping pre-commit installation (not a git repository)."
fi

# 3. Initial sync
echo "Running initial shim sync..."
python3 scripts/agents/sync_shims.py

# 4. Initial validation
echo "Running initial validation..."
python3 ci/validate_agent_assets.py

echo "--- Setup Complete ---"
echo "You can now run 'pytest' to execute unit tests."
echo "Pre-commit hooks will automatically run on 'git commit'."

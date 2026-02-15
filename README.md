# Agent Governance Pack (multi-tool)

This repo is a **portable governance + skill pack** that keeps one canonical source of truth (`AGENTS.md` + `docs/agents/` + `.agents/skills/`) and generates shims for:

- OpenAI Codex
- Claude Code
- Gemini CLI
- Google Antigravity IDE
- Cursor

## How to use

## Quick Start

1. **GitHub Template**: Click "Use this template" on GitHub to create a new repository from this one.
   - *Alternative*: Clone/copy these files into the root of your target repository.

2. Run the setup script to install tools and configure hooks:

   ```bash
   bash scripts/setup.sh
   ```

3. Commit the generated shims.
4. Add/maintain skills under `.agents/skills/<skill-name>/`.

## Development

- **Sync Shims**: `python scripts/agents/sync_shims.py`
- **Validate**: `python ci/validate_agent_assets.py`
- **Test**: `pytest`
- **Lint/Format**: `ruff check --fix` and `ruff format`

These checks are also enforced via `pre-commit` and GitHub Actions.

## Validation

- Local: `python ci/validate_agent_assets.py`
- CI: `.github/workflows/validate-agent-assets.yml`

- `AGENTS.md` and `docs/agents/**`
- `.agents/skills/**`
- `scripts/agents/**`, `ci/**`, `schemas/**`

## Frontier Orchestration (OpenCode)

- **Architecture**: [MODEL_SELECTION.md](docs/agents/opencode/MODEL_SELECTION.md)
- **Setup**: [SETUP.md](docs/agents/opencode/SETUP.md)

Do **not** hand-edit shim folders; regenerate via `sync_shims.py`.

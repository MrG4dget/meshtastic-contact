# AGENTS.md (scripts-specific)

This file overrides or extends the root `AGENTS.md` for any work performed within the `scripts/` directory.

## Script Authoring Rules

- **Language**: Always use Python 3.11+.
- **Imports**: Ensure all imports are absolute. Use `from __future__ import annotations`.
- **Typing**: Use type hints for all function signatures.
- **Paths**: Always use `pathlib.Path` instead of `os.path` strings.
- **Linting**: All scripts must pass `ruff check` and `ruff format`.

## Tooling

- If modifying shims, always re-run `python scripts/agents/sync_shims.py` and verify.

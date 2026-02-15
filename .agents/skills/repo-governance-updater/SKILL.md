---
name: repo-governance-updater
description: Update and validate this repository's agent governance pack (AGENTS.md, docs/agents, skills, shims for Claude/Gemini/Antigravity/Cursor). Use when modifying rules, adding skills, or fixing drift across tool-specific entrypoints. Do not use for application feature work.
---

## Goal

Keep agent governance **consistent across tools** by editing canonical sources and regenerating shims.

## Canonical sources (edit these)

- `AGENTS.md`
- `docs/agents/**`
- `.agents/skills/**`
- `scripts/agents/**`
- `ci/**`, `schemas/**`

## Required workflow

1. Make the requested governance change in canonical sources.
2. Regenerate shims:
   - `python scripts/agents/sync_shims.py`
   - (if governance changed) `python scripts/agents/generate_cursor_rule.py`
3. Validate:
   - `python ci/validate_agent_assets.py`
4. If validation fails, fix the canonical source and regenerate shims again.
5. Update `docs/agents/CHANGELOG.md` (add an Unreleased entry).

## Boundaries

- Do not add new dependencies unless explicitly asked.
- Do not hand-edit shim directories (`.claude/`, `.gemini/`, `.agent/`, `.cursor/`).
- Keep `AGENTS.md` short; add detail to `docs/agents/`.

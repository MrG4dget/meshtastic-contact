# Agent Governance Pack Architecture

## Overview

This repository functions as a "portable brain" for AI agents. It centralizes rules in a human-readable format and automates the creation of tool-specific entrypoints (shims).

## Core Components

### Canonical Sources (Human Maintained)

- `AGENTS.md`: High-level entry point and "at a glance" rules.
- `docs/agents/`: Detailed guidelines, style guides, and persona descriptions.
- `.agents/skills/`: Portable "actions" that agents can learn and execute.

### Automation Scripts (The Sync Layer)

- `scripts/agents/sync_shims.py`: The heart of the system. It mirrors skills and generates shims for:
  - Claude (`.claude/CLAUDE.md`)
  - Gemini (`.gemini/GEMINI.md`)
  - Antigravity (`.agent/rules/*.md`)
  - Cursor (`.cursor/rules/*.mdc` via `generate_cursor_rule.py`)

### Validation Layer

- `ci/validate_agent_assets.py`: A safeguard ensures that shims exist, `AGENTS.md` is imported correctly, and skills have valid manifests.

## Sync Logic

1. **Skill Mirroring**: Uses `shutil.copytree` or symlinks (on Linux/Mac) to project `.agents/skills` into tool-specific directories.
2. **Shim Generation**: Writes minimal wrapper files that reference the canonical sources using tool-specific syntax (e.g., `@import` for Gemini).

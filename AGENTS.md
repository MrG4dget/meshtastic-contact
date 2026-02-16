# AGENTS.md

This file is the **canonical, human-maintained source of truth** for how AI coding agents should work in this repository.

This repo also includes **tool-specific shims** so Codex, Claude Code, Gemini CLI, Antigravity IDE, and Cursor can all pick up the same governance with minimal duplication.

## Quick commands (for this template)

- Sync tool shims (symlink when possible, copy otherwise): `python scripts/agents/sync_shims.py`
- Validate the agent pack (run in CI): `python ci/validate_agent_assets.py`
- Regenerate Cursor rule from this repo’s governance docs: `python scripts/agents/generate_cursor_rule.py`

## Tool entrypoints (what reads what)

- **OpenAI Codex**: reads `AGENTS.md` (cascades by directory; nearest file wins).
- **Claude Code**: reads `CLAUDE.md` (project memory) in either `./CLAUDE.md` or `./.claude/CLAUDE.md`.
- **Gemini CLI**: reads `.gemini/GEMINI.md` (supports `@` imports).
- **Google Antigravity IDE**: reads workspace rules in `.agent/rules/` and can use `.agent/skills/`.
- **Cursor**: reads `.cursor/rules/*.mdc` rule files.

This repo keeps `AGENTS.md` canonical and makes other entrypoints thin wrappers that reference it.

## Repo contract (canonical vs shims)

### Canonical (edit these)

- `AGENTS.md` (this file)
- `docs/agents/` (detailed governance, style guides, checklists)
- `.agents/skills/` (cross-tool skill directories anchored by `SKILL.md`)
- `scripts/agents/` (shim sync + generators)
- `ci/` and `schemas/` (validation)

### Shims (do not edit by hand)

- `.claude/` (Claude Code memory + skills mirror)
- `.gemini/` (Gemini CLI memory + skills mirror)
- `.agent/` (Antigravity workspace rules/workflows + skills mirror)
- `.cursor/` (Cursor rules)

If you change governance or skills, run `python scripts/agents/sync_shims.py` and commit the results.

## Operating rules for agents

### 1) Before changing code

- Identify the smallest change that solves the task.
- Locate the relevant files; avoid broad rewrites.
- If a change affects behavior, also update tests and docs.

### 2) Before creating a PR

Run the repo’s standard checks. If this template is used standalone, run:

- `python ci/validate_agent_assets.py`

### 3) Documentation drift rule

If you modify:

- skills (`.agents/skills/**`)
- shims (`.gemini/**`, `.claude/**`, `.agent/**`, `.cursor/**`)
- validation scripts (`ci/**`, `schemas/**`, `scripts/agents/**`)

…then update the relevant docs in `docs/agents/` in the same PR.

### 4) Shim sync rule

- If you modify canonical sources (`AGENTS.md`, `docs/agents/**`, `.agents/skills/**`, `.agents/workflows/**`), you MUST run `python scripts/agents/sync_shims.py`.
- **Windows Users**: On Windows, shims are mirrored via copying. Prompt the user to run the sync script if you cannot run it yourself, as changes won't be visible to the IDE otherwise.

## Skill authoring rules

- A skill is a folder with **exactly one** `SKILL.md` containing YAML front matter with:
  - `name`
  - `description`
- Keep the `description` narrowly scoped; it’s used for skill selection.
- Put scripts inside the skill folder if the skill needs runnable helpers.

## When to add more AGENTS.md files

If your repo becomes large, add additional `AGENTS.md` files in subfolders to provide more specific instructions for that area (tests, infra, frontend, etc.). Keep each one short and scoped.

## References (tool docs)

See `docs/agents/TOOLING.md` for linkable, up-to-date pointers to each tool’s conventions.

## Persistent Context (Knowledge)

- **Knowledge SOP**: [docs/agents/KNOWLEDGE_SUBAGENT.md](docs/agents/KNOWLEDGE_SUBAGENT.md)
- **OpenCode Orchestrator**: [.agents/skills/opencode-orchestrator/SKILL.md](.agents/skills/opencode-orchestrator/SKILL.md) (Coordinates multi-model tasks).
- **Shared Knowledge**: Check `knowledge/` for architectural insights.
- [KI: Governance Architecture](knowledge/governance-pack-architecture/artifact.md)
- [KI: Meshtastic Contact Project Mission](knowledge/meshtastic-contact-project-mission/artifact.md)

# Tooling notes (agents)

This project intentionally uses **one canonical governance source** (`AGENTS.md` + `docs/agents/`) and mirrors it into tool-specific entrypoints.

## OpenAI Codex

- Custom instructions: `AGENTS.md` is read before work begins, and can cascade by directory.
- Skills: a skill is a folder anchored by `SKILL.md` (with YAML front matter: `name`, `description`).

## Claude Code

- Project memory: `CLAUDE.md` is loaded at startup. Supported locations include:
  - `./CLAUDE.md`
  - `./.claude/CLAUDE.md`
- Skills: `SKILL.md` folders can be mirrored into `.claude/skills/`.

## Gemini CLI

- Project memory: `.gemini/GEMINI.md` is loaded for the project.
- GEMINI.md supports modular imports via `@./relative.md` and `@../relative.md`.
- Skills: `.gemini/skills/` is the workspace skill directory.

## Google Antigravity IDE

- Workspace rules: `.agent/rules/`
- Workspace workflows: `.agent/workflows/`
- Skills: `.agent/skills/`

## Cursor

- Project rules: `.cursor/rules/*.mdc` (markdown with YAML front matter).
- Front matter commonly includes `description`, `globs`, and `alwaysApply`.

See the root `AGENTS.md` for operational rules and the shim sync process.

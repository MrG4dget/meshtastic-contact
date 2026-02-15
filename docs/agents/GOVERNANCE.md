# Governance (agents)

This document expands on `AGENTS.md`. Keep `AGENTS.md` short; put detail here.

## Change discipline

- Prefer minimal diffs and small PRs.
- Avoid large refactors unless explicitly required.
- Preserve existing public APIs unless the task requires changes.

## PR checklist (agent)

- [ ] Ran the relevant checks/tests
- [ ] Updated docs in `docs/agents/` if governance/skills changed
- [ ] Regenerated shims if needed: `python scripts/agents/sync_shims.py`
- [ ] Added/updated Cursor rule if governance meaningfully changed:
      `python scripts/agents/generate_cursor_rule.py`
- [ ] No accidental secrets (tokens, keys, credentials)

## Documentation drift policy

If you change any of these, update docs:
- `.agents/skills/**`
- `.gemini/**`, `.claude/**`, `.agent/**`, `.cursor/**`
- `scripts/agents/**`, `ci/**`, `schemas/**`

## Skill design guidelines

- Write narrow `description` fields; avoid “do everything” skills.
- Keep SKILL.md instructions action-oriented and testable.
- Provide “when to use / when not to use” boundaries.
- If the skill includes scripts:
  - document inputs/outputs
  - prefer deterministic behavior
  - avoid network calls unless the task demands it

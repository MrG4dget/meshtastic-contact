---
name: knowledge-manager
description: Manage (search, create, update) Knowledge Items (KIs) in the `knowledge/` directory. Use when documenting new architectural insights, non-obvious bug patterns, or domain logic.
---

## Usage

Use this skill when you need to persist knowledge for future agents.

### Commands/Operations

1. **Search KIs**: List subdirectories in `knowledge/` and read `metadata.json` files to find relevant context.
2. **Create KI**: Follow the SOP in `docs/agents/KNOWLEDGE_SUBAGENT.md`.
   - Create `knowledge/<id>/` folder.
   - Create `metadata.json` and `artifact.md`.
3. **Update KI**: Refine existing articles when technical details change or new "gotchas" are discovered.

## Key Files

- `knowledge/`: Root for all KIs.
- `docs/agents/KNOWLEDGE_SUBAGENT.md`: The operating protocol for this skill.

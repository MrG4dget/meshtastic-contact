---
description: How to manage Knowledge Items (KIs) to persist architectural and domain insights.
---

# Knowledge Management Workflow

// turbo-all

1. **Identify Necessity**: Check if the current insight involves architectural patterns, complex domain logic (e.g., Meshtastic protocols), or non-obvious issue patterns.
2. **Search Existing KIs**: List `knowledge/` and read `metadata.json` to avoid duplication.
3. **Execute Knowledge SOP**:
   - Create `knowledge/<kebab-case-id>/` directory.
   - Create `metadata.json` with `title`, `summary`, `tags[]`, and `created_at`.
   - Create `artifact.md` with the documented knowledge.
4. **Reference in Governance**:
   - Add a link to the new KI in `AGENTS.md` following the format: `[KI: Title](knowledge/id/artifact.md)`.
5. **Sync & Validate**:
   - Run `python scripts/agents/sync_shims.py`.
   - Run `python ci/validate_agent_assets.py`.

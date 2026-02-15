---
description: validate agent governance pack
---

# Workflow: validate agent governance pack

## Steps

1. Run: `python ci/validate_agent_assets.py`
2. If it fails:
   - fix canonical sources
   - re-run `python scripts/agents/sync_shims.py`
   - re-run validation

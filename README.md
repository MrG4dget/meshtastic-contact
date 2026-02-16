# Meshtastic Contact

Meshtastic Contact is a specialized toolset and governance pack designed to **improve the remote management of Meshtastic nodes**.

This project provides:

- **Enhanced Remote Management**: Streamlined workflows for interacting with and managing Meshtastic devices over various transport layers.
- **Pedigree**: Built upon the foundational work from [pdxlocations/contact](https://github.com/pdxlocations/contact).
- **Custom Protobuf Support**: Natively supports the custom Meshtastic protobuf definitions required by the [MrG4dget firmware (t1000-e-btn branch)](https://github.com/MrG4dget/firmware/tree/t1000-e-btn/protobufs).

---

## Agent Governance & Development

This repository uses a **portable governance + skill pack** to ensure consistent behavior across different AI coding assistants.

### Governance Architecture

- **Canonical Source**: [AGENTS.md](file:///c:/Users/Tomer/Documents/meshtastic-contact/AGENTS.md) contains the main instructions.
- **Detailed Docs**: [docs/agents/](file:///c:/Users/Tomer/Documents/meshtastic-contact/docs/agents/)
- **Skills**: [.agents/skills/](file:///c:/Users/Tomer/Documents/meshtastic-contact/.agents/skills/)

### Tool Shims

Shims are automatically generated for:

- OpenAI Codex
- Claude Code
- Gemini CLI
- Google Antigravity IDE
- Cursor

### Development Workflow

1. **Sync Shims**: If you modify governance or skills, run `python scripts/agents/sync_shims.py`.
2. **Validate**: `python ci/validate_agent_assets.py`
3. **Test**: `pytest`
4. **Lint/Format**: `ruff check --fix` and `ruff format`

Do **not** hand-edit the `.claude/`, `.gemini/`, `.agent/`, or `.cursor/` folders directly.

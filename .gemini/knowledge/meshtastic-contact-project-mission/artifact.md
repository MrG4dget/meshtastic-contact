# Meshtastic Contact: Project Mission & State

## Mission Strategic

The primary goal of **Meshtastic Contact** is to dramatically improve the **remote management** of Meshtastic nodes. It focuses on providing a professional, reliable, and extensible interface for node administration, monitoring, and interaction.

## Technical Pedigree

This project is not built in a vacuum. It leverages and builds upon the following foundational work:

1. **Contact Project**: Inherits core local/remote management capabilities from [pdxlocations/contact](https://github.com/pdxlocations/contact).
2. **Custom Protobufs**: Specifically designed to support the custom protobuf definitions provided by the [MrG4dget firmware (t1000-e-btn branch)](https://github.com/MrG4dget/firmware/tree/t1000-e-btn/protobufs). These allow for advanced button handling and device-specific features for the Tracker T1000-E.

## Current Repository State

As of February 2026, the repository has been fully instantiated with a portable Agent Governance Pack.

### Key Infrastructure

- **Governance**: Canonical rules live in `AGENTS.md` and `docs/agents/`.
- **Shims**: Automatically synced to `.claude/`, `.gemini/`, `.agent/`, and `.cursor/`.
- **Validation**: Enforced via `ci/validate_agent_assets.py` and `pytest`.

### Technical stack

- **Language**: Python for tooling/scripts.
- **Protobufs**: Integration point for Meshtastic device communication.
- **Agent Support**: Multi-tool support via shim generation.

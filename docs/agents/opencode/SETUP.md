# OpenCode Setup Guide

Follow these steps to set up and configure the OpenCode orchestration layer in this repository.

## Prerequisites

- **Python 3.8+**
- AI Agent tools: Claude Code, Gemini CLI, or Antigravity IDE.
- Access to the following models:
  - Gemini 3 Flash (Primary for Agentic Coding)
  - Gemini 1.5 Pro (Research & Context)
  - Claude 3.5 Sonnet (Architecture & Precision)

## Installation

1. **Clone the repository** (if not already done).
2. **Initialize Agent Governance**:

   ```bash
   python scripts/agents/sync_shims.py
   ```

3. **Verify Installation**:

   ```bash
   python scripts/agents/opencode.py --help
   ```

## Configuration

### Model Routing

OpenCode uses a tiered model routing system. You can view the selection logic in [MODEL_SELECTION.md](./MODEL_SELECTION.md).

### Environment Variables

Ensure you have the following keys in your `.env` (or environment):

- `GOOGLE_API_KEY` (for Gemini)
- `ANTHROPIC_API_KEY` (for Claude)

## Usage

To start a new orchestrated task:

```bash
python scripts/agents/opencode.py "Refactor the login logic to use OAuth2"
```

For more details on agent personas, see the [Knowledge Subagent](../KNOWLEDGE_SUBAGENT.md) documentation.

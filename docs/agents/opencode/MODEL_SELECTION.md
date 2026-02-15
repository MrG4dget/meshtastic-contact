# Model Selection Guide

This guide defines the criteria for routing tasks to different LLM models within the OpenCode ecosystem.

## Selection Matrix

| Model | Primary Strength | Use Case | Reasoning |
| :--- | :--- | :--- | :--- |
| **Gemini 3 Flash** | Speed & Agentic Coding | Implementation, code fixes, interactive agents | High-speed (3x faster than 2.5 Pro) with Pro-grade reasoning. Scored 78% on SWE-bench Verified. |
| **Gemini 1.5 Pro** | Context Window | Research, log analysis, repo-wide audits | Best for tasks requiring understanding of 1M+ tokens or scanning many files. |
| **Claude 3.5 Sonnet** | Precision & Logic | Complex architecture, logic-heavy refactoring | Exceptional at following strict protocols and executing multi-step sequences. |
| **Codex (GPT family)** | Logic & Math | Scripting, math, standalone utilities | Highly efficient for well-defined algorithmic problems and standalone Python scripts. |

## Guidance for Orchestrators

1. **Research First (Gemini)**: If the task requires knowing "where X is defined" or "how Y interacts with Z", start with Gemini.
2. **Implement Second (Claude)**: Once the scope is defined, hand over to Claude for the actual code modifications.
3. **Optimize Last (Codex)**: For performance-critical blocks or specialized logic, use Codex to refine the implementation.

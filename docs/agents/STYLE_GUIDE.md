# Style guide (agents)

## Markdown
- Prefer short sections, headings, and bullet lists.
- Keep line lengths reasonable where practical.
- Put long procedures in `docs/agents/` instead of `AGENTS.md`.

## Scripts
- Provide `--help`.
- Fail fast with clear errors.
- Avoid modifying files outside the repo root.

## Validation
- Add validation for new conventions.
- CI must run validation and fail on violations.

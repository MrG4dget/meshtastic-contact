#!/usr/bin/env python
"""
Validate this agent governance pack.

Run:
  python ci/validate_agent_assets.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(md_text: str) -> tuple[dict[str, str], str]:
    """
    Minimal YAML frontmatter parser for simple key: value pairs.
    Returns (frontmatter_dict, rest_of_document).
    """
    m = _FRONTMATTER_RE.match(md_text)
    if not m:
        return {}, md_text
    raw = m.group(1)
    rest = md_text[m.end() :]
    data: dict[str, str] = {}
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        data[k] = v
    return data, rest


def validate_skill(skill_dir: Path) -> bool:
    ok = True
    skill_md_files = [p for p in skill_dir.iterdir() if p.is_file() and p.name.lower() == "skill.md"]
    if len(skill_md_files) != 1:
        fail(f"{skill_dir}: expected exactly one SKILL.md, found {len(skill_md_files)}")
        return False

    # Frontmatter validation
    text = skill_md_files[0].read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    for key in ("name", "description"):
        if key not in fm or not fm[key].strip():
            fail(f"{skill_dir}/SKILL.md: missing or empty frontmatter key: {key}")
            ok = False

    # manifest.json validation
    manifest_path = skill_dir / "manifest.json"
    if not manifest_path.exists():
        fail(f"{skill_dir}: missing manifest.json")
        ok = False
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            # Basic schema check (minimal subset of the real schema)
            for key in ("schemaVersion", "name", "entrypoint"):
                if key not in manifest:
                    fail(f"{manifest_path}: missing required key '{key}'")
                    ok = False

            # Consistency check
            if "name" in manifest and manifest["name"] != skill_dir.name:
                fail(f"{manifest_path}: name '{manifest['name']}' does not match folder '{skill_dir.name}'")
                ok = False

            if "name" in fm and fm["name"] != skill_dir.name:
                fail(f"{skill_dir}/SKILL.md: frontmatter name '{fm['name']}' does not match folder '{skill_dir.name}'")
                ok = False

        except json.JSONDecodeError:
            fail(f"{manifest_path}: invalid JSON")
            ok = False

    return ok


def _validate_canonical_paths() -> bool:
    ok = True
    required_paths = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "docs" / "agents" / "GOVERNANCE.md",
        REPO_ROOT / "docs" / "agents" / "TOOLING.md",
        REPO_ROOT / "docs" / "agents" / "KNOWLEDGE_SUBAGENT.md",
        REPO_ROOT / "schemas" / "skill-manifest.schema.json",
        REPO_ROOT / ".agents" / "skills",
        REPO_ROOT / ".agents" / "workflows",
        REPO_ROOT / "scripts" / "agents" / "sync_shims.py",
        REPO_ROOT / "scripts" / "agents" / "generate_cursor_rule.py",
        REPO_ROOT / "scripts" / "agents" / "opencode.py",
    ]
    for p in required_paths:
        if not p.exists():
            fail(f"missing required path: {p}")
            ok = False
    return ok


def _validate_skills() -> bool:
    ok = True
    skills_root = REPO_ROOT / ".agents" / "skills"
    if skills_root.exists():
        for child in sorted(skills_root.iterdir()):
            if child.is_dir():
                if not validate_skill(child):
                    ok = False
    return ok


def _validate_workflows() -> bool:
    ok = True
    workflows_root = REPO_ROOT / ".agents" / "workflows"
    if workflows_root.exists():
        for child in sorted(workflows_root.iterdir()):
            if child.is_file() and child.suffix == ".md":
                text = child.read_text(encoding="utf-8")
                fm, _ = parse_frontmatter(text)
                if "description" not in fm or not fm.get("description", "").strip():
                    fail(f"{child}: missing or empty frontmatter key 'description'")
                    ok = False
    return ok


def _validate_rules() -> bool:
    ok = True
    rules_root = REPO_ROOT / ".agent" / "rules"
    if rules_root.exists():
        for child in sorted(rules_root.iterdir()):
            if child.is_file() and child.suffix == ".md":
                text = child.read_text(encoding="utf-8")
                fm, _ = parse_frontmatter(text)
                for key in ("name", "description"):
                    if key not in fm or not fm.get(key, "").strip():
                        fail(f"{child}: missing or empty frontmatter key '{key}'")
                        ok = False
    return ok


def _validate_shims() -> bool:
    ok = True
    shim_paths = [
        (REPO_ROOT / ".claude" / "CLAUDE.md", "CLAUDE.md"),
        (REPO_ROOT / ".gemini" / "GEMINI.md", "GEMINI.md"),
        (REPO_ROOT / ".cursor" / "rules" / "repo-governance.mdc", "repo-governance.mdc"),
        (REPO_ROOT / ".agent" / "rules" / "000-repo-governance.md", "000-repo-governance.md"),
        (REPO_ROOT / ".agent" / "workflows" / "validate-agent-assets.md", "validate-agent-assets.md"),
    ]
    for p, _label in shim_paths:
        if not p.exists():
            fail(f"missing shim path (run sync): {p}")
            ok = False
        else:
            content = p.read_text(encoding="utf-8")
            # Workflows are mirrored 1:1, so they don't have the sync warning
            if "workflows" not in str(p) and "AUTO-GENERATED" not in content:
                fail(f"{p}: shim missing 'AUTO-GENERATED' warning")
                ok = False

    # Check for stray files in Antigravity shims
    for shim_dir, source_dir in [
        (REPO_ROOT / ".agent" / "workflows", REPO_ROOT / ".agents" / "workflows"),
        (REPO_ROOT / ".agent" / "skills", REPO_ROOT / ".agents" / "skills"),
    ]:
        if shim_dir.exists():
            for child in shim_dir.iterdir():
                if child.name == "validate-agent-assets.md":
                    continue
                if not (source_dir / child.name).exists():
                    fail(f"stray file in shim directory: {child} (not in canonical source)")
                    ok = False

    gemini_md = REPO_ROOT / ".gemini" / "GEMINI.md"
    if gemini_md.exists():
        content = gemini_md.read_text(encoding="utf-8")
        if "@../AGENTS.md" not in content:
            fail(f"{gemini_md}: expected to import @../AGENTS.md")
            ok = False
    return ok


def main() -> int:
    ok = True
    if not _validate_canonical_paths():
        ok = False
    if not _validate_skills():
        ok = False
    if not _validate_workflows():
        ok = False
    if not _validate_rules():
        ok = False
    if not _validate_shims():
        ok = False

    if ok:
        print("SUCCESS: All agent assets validated.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

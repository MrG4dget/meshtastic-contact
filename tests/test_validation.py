import sys
from pathlib import Path

# Add ci directory to path to import validate_agent_assets
sys.path.append(str(Path(__file__).resolve().parents[1] / "ci"))
import validate_agent_assets


def test_parse_frontmatter_valid():
    text = "---\nname: test-skill\ndescription: A test skill\n---\nBody content"
    fm, rest = validate_agent_assets.parse_frontmatter(text)
    assert fm == {"name": "test-skill", "description": "A test skill"}
    assert rest.strip() == "Body content"


def test_parse_frontmatter_invalid():
    text = "No frontmatter here"
    fm, rest = validate_agent_assets.parse_frontmatter(text)
    assert fm == {}
    assert rest == text


def test_parse_frontmatter_partial():
    text = "---\nname: test-skill\n# commented: out\ninvalid line\n---\nBody"
    fm, rest = validate_agent_assets.parse_frontmatter(text)
    assert fm == {"name": "test-skill"}
    assert rest.strip() == "Body"


def test_validate_skill_valid(tmp_path):
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("---\nname: test-skill\ndescription: Test\n---\n", encoding="utf-8")
    manifest = skill_dir / "manifest.json"
    manifest.write_text('{"schemaVersion": "1.0", "name": "test-skill", "entrypoint": "SKILL.md"}', encoding="utf-8")

    assert validate_agent_assets.validate_skill(skill_dir) is True


def test_validate_skill_missing_md(tmp_path):
    skill_dir = tmp_path / "bad-skill"
    skill_dir.mkdir()
    assert validate_agent_assets.validate_skill(skill_dir) is False


def test_validate_skill_missing_manifest(tmp_path):
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("---\nname: test-skill\ndescription: Test\n---\n", encoding="utf-8")
    # No manifest.json
    assert validate_agent_assets.validate_skill(skill_dir) is False


def test_validate_skill_wrong_name_fm(tmp_path):
    skill_dir = tmp_path / "actual-name"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("---\nname: wrong-name\ndescription: Test\n---\n", encoding="utf-8")
    manifest = skill_dir / "manifest.json"
    manifest.write_text('{"schemaVersion": "1.0", "name": "actual-name", "entrypoint": "SKILL.md"}', encoding="utf-8")

    # This should fail because name in FM doesn't match folder name
    assert validate_agent_assets.validate_skill(skill_dir) is False


def test_validate_skill_wrong_name_manifest(tmp_path):
    skill_dir = tmp_path / "actual-name"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("---\nname: actual-name\ndescription: Test\n---\n", encoding="utf-8")
    manifest = skill_dir / "manifest.json"
    manifest.write_text('{"schemaVersion": "1.0", "name": "wrong-name", "entrypoint": "SKILL.md"}', encoding="utf-8")

    # This should fail because name in manifest doesn't match folder name
    assert validate_agent_assets.validate_skill(skill_dir) is False

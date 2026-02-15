import sys
from pathlib import Path

import pytest

# Add scripts/agents directory to path to import sync_shims
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts" / "agents"))
import sync_shims


def test_ensure_dir(tmp_path):
    test_dir = tmp_path / "a" / "b" / "c"
    sync_shims._ensure_dir(test_dir)
    assert test_dir.is_dir()


def test_safe_unlink_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    sync_shims._safe_unlink(f)
    assert not f.exists()


def test_safe_unlink_dir(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    (d / "file.txt").write_text("data")
    sync_shims._safe_unlink(d)
    assert not d.exists()


def test_symlink_or_copy_copy(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "file.txt").write_text("source")
    dst = tmp_path / "dst"

    result = sync_shims._symlink_or_copy(src, dst, mode="copy")
    assert result == "copy"
    assert dst.is_dir()
    assert (dst / "file.txt").read_text() == "source"


@pytest.mark.skipif(sys.platform == "win32", reason="Linux-specific symlink test")
def test_symlink_or_copy_symlink(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "file.txt").write_text("source")
    dst = tmp_path / "dst"

    result = sync_shims._symlink_or_copy(src, dst, mode="symlink")
    assert result == "symlink"
    assert dst.is_symlink()
    assert dst.resolve() == src.resolve()

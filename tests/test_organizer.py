"""对 organizer 模块的单元测试。"""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from mycli import organizer
from mycli.cli import app

runner = CliRunner()


def _make_files(tmp: Path) -> None:
    (tmp / "a.jpg").write_bytes(b"image-data-1")
    (tmp / "b.png").write_bytes(b"image-data-2")
    (tmp / "c.py").write_text("print(1)")
    (tmp / "d.txt").write_text("hello")


def test_organize_by_extension(tmp_path: Path) -> None:
    _make_files(tmp_path)
    result = organizer.organize_by_extension(tmp_path)

    assert len(result.organized) == 4
    assert (tmp_path / "images" / "a.jpg").exists()
    assert (tmp_path / "src" / "c.py").exists()


def test_organize_dry_run_does_not_move(tmp_path: Path) -> None:
    _make_files(tmp_path)
    result = organizer.organize_by_extension(tmp_path, dry_run=True)

    assert len(result.organized) == 4
    assert (tmp_path / "a.jpg").exists()        # 文件没被移动
    assert not (tmp_path / "images").exists()   # 目录都没建


def test_rename_with_prefix(tmp_path: Path) -> None:
    _make_files(tmp_path)
    result = organizer.rename_with_prefix(tmp_path, prefix="2026-")

    assert len(result.renamed) == 4
    assert (tmp_path / "2026-a.jpg").exists()
    assert not (tmp_path / "a.jpg").exists()


def test_find_duplicates(tmp_path: Path) -> None:
    _make_files(tmp_path)
    (tmp_path / "a-copy.jpg").write_bytes(b"image-data-1")  # 与 a.jpg 相同
    dup_groups = organizer.find_duplicates(tmp_path)

    assert len(dup_groups) == 1
    assert len(dup_groups[0]) == 2


def test_cli_organize_dry_run(tmp_path: Path) -> None:
    _make_files(tmp_path)
    result = runner.invoke(app, ["organize", str(tmp_path), "--dry-run"])
    assert result.exit_code == 0
    assert "预览" in result.output
    assert not (tmp_path / "images").exists()

"""批量文件整理器：归类、重命名、查重。"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class OrganizeResult:
    """一次整理的结果记录。"""
    organized: list[str] = field(default_factory=list)   # 已归类到子目录的文件
    renamed: list[tuple[str, str]] = field(default_factory=list)  # (旧名, 新名)
    duplicates: list[list[str]] = field(default_factory=list)  # 每组重复文件的路径
    skipped: list[str] = field(default_factory=list)      # 跳过的（目录/冲突/异常）


def _iter_files(target: Path) -> Iterable[Path]:
    """递归收集目录下的所有普通文件，跳过隐藏文件。"""
    if target.is_file():
        yield target
        return
    for p in sorted(target.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            yield p


def organize_by_extension(target, extensions=None, dry_run=False) -> OrganizeResult:
    """把文件按扩展名归类到对应子目录。"""
    result = OrganizeResult()
    if extensions is None:
        extensions = {".jpg": "images", ".png": "images", ".py": "src",
                      ".txt": "docs", ".csv": "data"}

    for file in _iter_files(target):
        if file.parent != target and file.parent.name in set(extensions.values()) | {"_other"}:
            continue
        ext = file.suffix.lower()
        dir_name = extensions.get(ext, "_other")
        dest_dir = target / dir_name
        dest = dest_dir / file.name

        if dest.exists() and dest != file:
            result.skipped.append(str(file))
            continue

        result.organized.append(str(file))
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            file.rename(dest)

    return result


def rename_with_prefix(target, prefix, dry_run=False) -> OrganizeResult:
    """给目录下所有文件加统一前缀重命名。"""
    result = OrganizeResult()
    for file in _iter_files(target):
        new_name = f"{prefix}{file.name}"
        dest = file.with_name(new_name)
        if dest.exists():
            result.skipped.append(str(file))
            continue
        result.renamed.append((file.name, new_name))
        if not dry_run:
            file.rename(dest)
    return result


def file_sha256(path, chunk_size=65536) -> str:
    """计算文件 SHA-256，大文件分块读取。"""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(target) -> list[list[str]]:
    """按内容哈希找出重复文件，返回每组重复文件路径列表。"""
    hash_map: dict[str, list[Path]] = {}
    for file in _iter_files(target):
        digest = file_sha256(file)
        hash_map.setdefault(digest, []).append(file)
    return [[str(p) for p in paths] for digest, paths in hash_map.items() if len(paths) > 1]

"""日志配置：控制台输出 + 文件输出，按级别区分。"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: str | None = None,
) -> logging.Logger:
    """配置全局日志，返回根 logger。

    - 控制台：显示 INFO 及以上
    - 文件（可选）：记录 DEBUG 及以上，追加写入
    """
    logger = logging.getLogger("mycli")
    logger.setLevel(level)
    logger.propagate = False  # 避免与 root logger 重复

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台 handler
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件 handler（可选）
    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # 文件保留更细粒度
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger

"""示例命令入口：演示 CLI、日志、核心逻辑的协同。"""

from __future__ import annotations

import logging
import time
from typing import Annotated

import typer

from mycli.logging_setup import setup_logging

app = typer.Typer(add_completion=False)
logger = logging.getLogger("mycli.cli")


@app.command()
def hello(
    name: Annotated[str, typer.Option(help="问候对象")] = "world",
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="输出 DEBUG 日志")] = False,
    log_file: Annotated[str | None, typer.Option(help="写入日志文件")] = None,
) -> None:
    """打印问候语。"""
    setup_logging(level=logging.DEBUG if verbose else logging.INFO, log_file=log_file)
    logger.info("执行 hello 命令，name=%s", name)
    print(f"Hello, {name}!")


@app.command()
def bench(
    count: Annotated[int, typer.Option(help="循环次数")] = 1000,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="输出 DEBUG 日志")] = False,
    log_file: Annotated[str | None, typer.Option(help="写入日志文件")] = None,
) -> None:
    """跑一个简单基准，演示日志与计时。"""
    setup_logging(level=logging.DEBUG if verbose else logging.INFO, log_file=log_file)
    logger.info("开始基准测试，count=%d", count)
    start = time.perf_counter()
    total = sum(range(count))
    elapsed = time.perf_counter() - start
    logger.info("基准完成，耗时 %.4fs", elapsed)
    print(f"sum(0..{count - 1}) = {total}, 耗时 {elapsed:.4f}s")


if __name__ == "__main__":
    app()

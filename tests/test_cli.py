"""对 CLI 入口的冒烟测试。"""

from __future__ import annotations

from typer.testing import CliRunner

from mycli.cli import app

runner = CliRunner()


def test_hello() -> None:
    result = runner.invoke(app, ["hello", "--name", "测试"])
    assert result.exit_code == 0
    assert "Hello, 测试!" in result.output


def test_bench() -> None:
    result = runner.invoke(app, ["bench", "--count", "5"])
    assert result.exit_code == 0
    assert "sum(0..4) = 10" in result.output

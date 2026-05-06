"""BlockSecScan CLI entry point."""

from typer import Typer

app = Typer(name="blocksec", help="BlockSecScan - 区块链安全扫描平台")


@app.command()
def scan():
    """运行安全扫描"""
    print("scan command placeholder")


@app.command()
def report():
    """生成扫描报告"""
    print("report command placeholder")


@app.command()
def rules():
    """管理规则库"""
    print("rules command placeholder")


if __name__ == "__main__":
    app()

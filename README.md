# BlockSecScan

> ⚠️ **安全声明**：本项目仅用于授权安全测试、教学实验和自有资产安全检查。请勿对未授权目标进行扫描。使用者应自行承担因不当使用产生的法律责任。

A multi-platform blockchain security scanner for Fabric networks, smart contracts, Web3 applications, RPC services, and AI-assisted security analysis.

**BlockSecScan** 是一个面向 Fabric 联盟链、智能合约、Web3 应用和区块链 RPC 服务的多平台安全扫描工具。

## Features

- 🔍 **Fabric 配置安全扫描** — 检测 TLS、CouchDB、Docker、证书、端口暴露等安全问题
- 📋 **YAML 规则库** — 可扩展的规则系统，方便社区贡献
- 🖥️ **多平台入口** — CLI 命令行 / Web GUI / 桌面 GUI / GitHub Action / MCP Server
- 📊 **多格式报告** — JSON / HTML / Markdown / SARIF
- 🤖 **AI 安全助手** — 漏洞解释、修复建议、风险总结

## Quick Start

```bash
# 安装
pip install blocksecscan

# 扫描 Fabric 项目
blocksec scan fabric --path ./fabric-network

# 生成报告
blocksec report --format html
```

## Development

```bash
# 克隆仓库
git clone https://github.com/FECES-SHIT/BlockSecScan.git
cd BlockSecScan

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查
ruff check .
```

## Roadmap

| 版本 | 内容 |
|------|------|
| v0.1 | Fabric 配置扫描 + CLI + JSON 报告 |
| v0.2 | Fabric 运行时扫描 |
| v0.3 | SARIF / Markdown 报告 + GitHub Action |
| v0.4 | Web GUI |
| v0.5 | 智能合约扫描（集成 Slither） |
| v0.6 | Web3 / RPC 扫描 |
| v1.0 | 正式开源版 |
| v1.1 | MCP Server + AI 安全助手 |

## License

Apache-2.0

## Disclaimer

This tool is intended for authorized security testing, educational purposes, and self-owned asset security inspection only. Users are solely responsible for any legal consequences arising from improper use.

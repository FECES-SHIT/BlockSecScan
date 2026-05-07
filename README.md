<p align="center">
  <br>
  <samp>
    <a href="#-english">English</a> ·
    <a href="#-中文">中文</a>
  </samp>
  <br>
  <br>
</p>

<h1 align="center">🛡️ BlockSecScan</h1>

<p align="center">
  <b>Multi-platform Blockchain Security Scanner</b><br>
  <sub>Fabric · Smart Contracts · Web3 · RPC · AI-Powered Analysis</sub>
</p>

<p align="center">
  <a href="https://github.com/FECES-SHIT/BlockSecScan/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-alpha-orange.svg" alt="Status"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Fabric-Config_Security-green" alt="Fabric">
  <img src="https://img.shields.io/badge/Fabric-Runtime_Security-green" alt="Runtime">
  <img src="https://img.shields.io/badge/Report-JSON-blue" alt="Report">
  <img src="https://img.shields.io/badge/Rules-YAML-orange" alt="Rules">
</p>

<br>

> ⚠️ **Disclaimer / 安全声明**：This tool is intended for **authorized security testing**, **educational purposes**, and **self-owned asset security inspection only**. Do not scan targets without explicit authorization. Users are solely responsible for any legal consequences arising from improper use.
>
> 本项目**仅用于授权安全测试**、**教学实验**和**自有资产安全检查**。请勿对未授权目标进行扫描。使用者应自行承担因不当使用产生的法律责任。

<br>

---

# 🇬🇧 English

## Overview

**BlockSecScan** is a multi-platform blockchain security scanner designed to detect misconfigurations and vulnerabilities across:

| Platform | Status | Description |
|----------|--------|-------------|
| 🔗 Hyperledger Fabric (Config) | ✅ Available | TLS, CouchDB, Docker, certificates, port exposure |
| 🔗 Hyperledger Fabric (Runtime) | 🚧 Beta | Live node health, chaincode risks |
| 📜 Smart Contracts | 🗓️ Planned | Solidity / Chaincode static analysis |
| 🌐 Web3 DApps | 🗓️ Planned | Front-end injection, wallet integration risks |
| 🔌 RPC Services | 🗓️ Planned | JSON-RPC endpoint hardening |

## Features

- **🔍 YAML Rule Engine** — Define detection rules in YAML. Supports `pattern`, `regex`, and `key_value` match types with negation logic.
- **🧩 Modular Scanner Architecture** — Pluggable scanners via `BaseScanner` abstract class. Register custom scanners at runtime.
- **📊 Structured Findings** — Every finding includes: severity (CRITICAL→INFO), file location, evidence, remediation, references, and confidence score.
- **📄 JSON Export** — Export scan results as structured JSON for CI/CD pipelines or further processing.
- **🖥️ Rich CLI** — Built with Typer + Rich for colorful, human-readable terminal output.
- **🏗️ Extensible** — Add new rules as YAML files. Add new scanners as Python modules.

## Quick Start

### Installation

```bash
pip install blocksecscan
```

### CLI Usage

```bash
# Scan Fabric configuration files
blocksec scan fabric --path ./my-fabric-network

# Scan Fabric runtime environment
blocksec scan fabric-runtime --path ./my-fabric-network

# Save results as JSON
blocksec scan fabric --path ./my-fabric-network --output result.json

# List all available rules
blocksec rules
```

### Scan Result Example

```json
{
  "scan_id": "a1b2c3d4-...",
  "target": { "type": "fabric_config", "path": "./fabric-network" },
  "summary": { "critical": 0, "high": 2, "medium": 1, "low": 0, "info": 0 },
  "findings": [
    {
      "rule_id": "FABRIC_COUCHDB_EXPOSED",
      "severity": "HIGH",
      "title": "CouchDB 端口暴露到宿主机",
      "location": { "file_path": "...", "start_line": 12, "end_line": 12 },
      "evidence": "- \"0.0.0.0:5984:5984\"",
      "remediation": "Bind to 127.0.0.1:5984:5984 instead"
    }
  ]
}
```

## Architecture

```
blocksec/
├── api/            # Public API functions
├── cli/            # Typer CLI (scan, rules, report commands)
├── core/           # CoreEngine, RuleEngine, RuleParser
├── models/         # Pydantic models (Finding, Rule, ScanResult)
├── reports/        # Report exporters (JSON, future: HTML/Markdown/SARIF)
├── rules/fabric/   # YAML rule definitions
└── scanners/       # Scanner implementations (fabric_config, fabric_runtime)
```

### Core Components

| Component | File | Role |
|-----------|------|------|
| `CoreEngine` | `core/engine.py` | Orchestrates scanning: dispatches target → scanner, collects findings |
| `RuleEngine` | `core/rule_engine.py` | Executes rule matching: pattern, regex, key-value against file content |
| `RuleParser` | `core/rule_parser.py` | Parses YAML rule files into `Rule` model instances |
| `BaseScanner` | `scanners/base.py` | Abstract base class — implement `can_handle()` + `scan()` |
| `FabricConfigScanner` | `scanners/fabric_config/scanner.py` | Walks target directory, collects config files, runs rules |

### Data Flow

```
Target Path → CoreEngine.scan()
                │
                ▼
         Get Scanner by target_type
                │
                ▼
         Scanner.scan(target_path)
                │
                ▼
         Walk files → RuleEngine.match_file() per rule
                │
                ▼
         Collect Finding[] → ScanResult
```

## Built-in Fabric Rules

| Rule ID | Severity | Description |
|---------|----------|-------------|
| `FABRIC_COUCHDB_EXPOSED` | HIGH | CouchDB port mapped to all interfaces |
| `FABRIC_PLAINTEXT_PASSWORD` | MEDIUM | Plaintext password in environment variables |
| `FABRIC_TLS_ORDERER` | MEDIUM | Orderer TLS not enabled |
| `FABRIC_TLS_PEER` | MEDIUM | Peer TLS not properly configured |
| `FABRIC_DEBUG_LOG` | LOW | DEBUG log level in production |

## Writing Custom Rules

Create a YAML file in `blocksec/rules/fabric/`:

```yaml
id: FABRIC_MY_RULE
name: My Custom Check
category: Fabric Configuration
severity: HIGH
version: "1.0.0"
target:
  type: docker_compose
  files:
    - docker-compose.yaml
    - docker-compose.yml
match:
  type: regex                    # pattern | regex | key_value
  file_pattern: docker-compose*
  regex: 'ports:\s*-\s*"0\.0\.0\.0:'
  case_sensitive: false
description: "External port binding detected."
remediation: "Bind services to 127.0.0.1 instead of 0.0.0.0."
references:
  - https://docs.docker.com/compose/compose-file/#ports
enabled: true
```

## Development

```bash
git clone https://github.com/FECES-SHIT/BlockSecScan.git
cd BlockSecScan
pip install -e ".[dev]"

# Run tests
pytest

# Lint & type check
ruff check .
mypy blocksec/
```

## Roadmap

| Version | Content |
|---------|---------|
| v0.1 | ✅ Fabric Config Scanning + CLI + JSON Report |
| v0.2 | 🚧 Fabric Runtime Scanning |
| v0.3 | SARIF / Markdown Export + GitHub Action |
| v0.4 | Web GUI (FastAPI) |
| v0.5 | Smart Contract Scanning (Slither integration) |
| v0.6 | Web3 / RPC Scanning |
| v1.0 | Stable Release |
| v1.1 | MCP Server + AI Security Assistant |

## License

[Apache-2.0](LICENSE)

<br>

---

# 🇨🇳 中文

## 概述

**BlockSecScan** 是一个面向多平台的区块链安全扫描工具，检测以下场景的配置错误和安全漏洞：

| 平台 | 状态 | 说明 |
|------|------|------|
| 🔗 Hyperledger Fabric（配置） | ✅ 可用 | TLS、CouchDB、Docker、证书、端口暴露 |
| 🔗 Hyperledger Fabric（运行时） | 🚧 Beta | 节点健康、链码风险 |
| 📜 智能合约 | 🗓️ 规划中 | Solidity / 链码静态分析 |
| 🌐 Web3 DApp | 🗓️ 规划中 | 前端注入、钱包集成风险 |
| 🔌 RPC 服务 | 🗓️ 规划中 | JSON-RPC 端点加固 |

## 功能特性

- **🔍 YAML 规则引擎** — 使用 YAML 定义检测规则，支持 `pattern`、`regex`、`key_value` 三种匹配模式，支持否定逻辑。
- **🧩 模块化扫描器架构** — 基于 `BaseScanner` 抽象类实现可插拔扫描器，运行时动态注册自定义扫描器。
- **📊 结构化漏洞报告** — 每个漏洞包含：严重等级（CRITICAL→INFO）、文件位置、证据、修复建议、参考链接、置信度评分。
- **📄 JSON 导出** — 将扫描结果导出为结构化 JSON，方便接入 CI/CD 流水线。
- **🖥️ Rich 命令行界面** — 基于 Typer + Rich，彩色终端输出，友好可读。
- **🏗️ 高度可扩展** — 新增 YAML 文件即新增规则，新增 Python 模块即新增扫描器。

## 快速开始

### 安装

```bash
pip install blocksecscan
```

### CLI 使用

```bash
# 扫描 Fabric 配置文件
blocksec scan fabric --path ./my-fabric-network

# 扫描 Fabric 运行时环境
blocksec scan fabric-runtime --path ./my-fabric-network

# 输出 JSON 报告
blocksec scan fabric --path ./my-fabric-network --output result.json

# 查看所有规则
blocksec rules
```

### 扫描结果示例

```json
{
  "scan_id": "a1b2c3d4-...",
  "target": { "type": "fabric_config", "path": "./fabric-network" },
  "summary": { "critical": 0, "high": 2, "medium": 1, "low": 0, "info": 0 },
  "findings": [
    {
      "rule_id": "FABRIC_COUCHDB_EXPOSED",
      "severity": "HIGH",
      "title": "CouchDB 端口暴露到宿主机",
      "location": { "file_path": "...", "start_line": 12, "end_line": 12 },
      "evidence": "- \"0.0.0.0:5984:5984\"",
      "remediation": "将端口绑定到 127.0.0.1:5984:5984"
    }
  ]
}
```

## 架构

```
blocksec/
├── api/            # 公开 API 函数
├── cli/            # Typer CLI（scan、rules、report 命令）
├── core/           # 核心引擎：CoreEngine、RuleEngine、RuleParser
├── models/         # Pydantic 数据模型（Finding、Rule、ScanResult）
├── reports/        # 报告导出器（JSON，后续：HTML/Markdown/SARIF）
├── rules/fabric/   # YAML 规则定义
└── scanners/       # 扫描器实现（fabric_config、fabric_runtime）
```

### 核心组件

| 组件 | 文件 | 职责 |
|------|------|------|
| `CoreEngine` | `core/engine.py` | 扫描编排：分发目标 → 扫描器，收集结果 |
| `RuleEngine` | `core/rule_engine.py` | 规则匹配：pattern、regex、key-value 三种模式 |
| `RuleParser` | `core/rule_parser.py` | 解析 YAML 规则文件为 `Rule` 模型 |
| `BaseScanner` | `scanners/base.py` | 抽象基类 — 实现 `can_handle()` + `scan()` |
| `FabricConfigScanner` | `scanners/fabric_config/scanner.py` | 遍历目标目录，收集配置文件，执行规则 |

### 数据流

```
目标路径 → CoreEngine.scan()
              │
              ▼
       根据 target_type 获取扫描器
              │
              ▼
       Scanner.scan(target_path)
              │
              ▼
       遍历文件 → RuleEngine.match_file() 逐规则匹配
              │
              ▼
       收集 Finding[] → ScanResult
```

## 内置 Fabric 规则

| 规则 ID | 严重等级 | 描述 |
|---------|----------|------|
| `FABRIC_COUCHDB_EXPOSED` | HIGH | CouchDB 端口映射到所有网络接口 |
| `FABRIC_PLAINTEXT_PASSWORD` | MEDIUM | 环境变量中存在明文密码 |
| `FABRIC_TLS_ORDERER` | MEDIUM | Orderer 节点未启用 TLS |
| `FABRIC_TLS_PEER` | MEDIUM | Peer 节点 TLS 配置不当 |
| `FABRIC_DEBUG_LOG` | LOW | 生产环境开启 DEBUG 日志 |

## 编写自定义规则

在 `blocksec/rules/fabric/` 目录下创建 YAML 文件：

```yaml
id: FABRIC_MY_RULE
name: 我的自定义检查
category: Fabric Configuration
severity: HIGH
version: "1.0.0"
target:
  type: docker_compose
  files:
    - docker-compose.yaml
    - docker-compose.yml
match:
  type: regex                    # pattern | regex | key_value
  file_pattern: docker-compose*
  regex: 'ports:\s*-\s*"0\.0\.0\.0:'
  case_sensitive: false
description: "检测到端口绑定到所有网络接口。"
remediation: "将服务端口绑定到 127.0.0.1 而非 0.0.0.0。"
references:
  - https://docs.docker.com/compose/compose-file/#ports
enabled: true
```

## 开发指南

```bash
git clone https://github.com/FECES-SHIT/BlockSecScan.git
cd BlockSecScan
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查与类型检查
ruff check .
mypy blocksec/
```

## 路线图

| 版本 | 内容 |
|------|------|
| v0.1 | ✅ Fabric 配置扫描 + CLI + JSON 报告 |
| v0.2 | 🚧 Fabric 运行时扫描 |
| v0.3 | SARIF / Markdown 导出 + GitHub Action |
| v0.4 | Web GUI（FastAPI） |
| v0.5 | 智能合约扫描（集成 Slither） |
| v0.6 | Web3 / RPC 扫描 |
| v1.0 | 正式发布版 |
| v1.1 | MCP Server + AI 安全助手 |

## 开源协议

[Apache-2.0](LICENSE)

<br>

---

<p align="center">
  <sub>Made with ❤️ by <a href="https://github.com/FECES-SHIT">FECES-SHIT</a></sub>
</p>

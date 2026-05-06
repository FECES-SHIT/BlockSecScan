# BlockSecScan v0.1 交付文档

> 版本：v0.1.0  
> 日期：2026-05-06  
> 状态：✅ 完成  

---

## 一、项目概述

BlockSecScan 是一个面向 Hyperledger Fabric 联盟链的安全基线扫描平台。v0.1 实现了 **Fabric 配置文件安全扫描** 的完整闭环 —— 从规则定义、扫描引擎到报告输出的全流程。

### 运行示例

```bash
# 查看帮助
blocksec --help

# 扫描安全的 Fabric 配置
blocksec scan fabric --path labs/fabric-safe
# → [PASS] 未发现安全问题！

# 扫描有漏洞的 Fabric 配置
blocksec scan fabric --path labs/fabric-vuln-couchdb-exposed
# → HIGH: 5  |  MEDIUM: 1  |  LOW: 1  |  合计: 7

# 导出 JSON 报告
blocksec scan fabric --path labs/fabric-vuln-couchdb-exposed -o report.json

# 查看规则库
blocksec rules
```

---

## 二、技术指标

| 指标 | 数值 |
|------|------|
| 源代码文件 | 17 个 Python 文件 |
| 安全规则 | 5 条 YAML 规则 |
| 代码行数 | ~700 行 Python |
| 单元测试 | 19 个 |
| 集成测试 | 8 个 |
| 测试通过率 | 27/27 (100%) |
| ruff 检查 | 0 errors |
| Python 版本 | 3.11+ |

---

## 三、架构总览

```
用户 ──→ CLI (Typer + Rich) ──→ Public API ──→ Core Engine
                                                    │
                                          ScannerRegistry
                                               │
                                        FabricConfigScanner
                                          │          │
                                    RuleParser    RuleEngine
                                          │          │
                                    YAML 规则    文本匹配
                                          │          │
                                    Rules/       Findings
                                          │
                                    JsonExporter ──→ report.json
```

### 分层依赖（单向，禁止循环引用）

```
Models（最底层，无依赖）
  ↑
RuleEngine（依赖 Models）
  ↑
Scanner（依赖 Models + RuleEngine）
  ↑
CoreEngine（依赖 Scanner + Models）
  ↑
Public API（依赖 CoreEngine + Models）
  ↑
CLI（依赖 Public API + Models）
```

---

## 四、v0.1 实现的全部功能详解

### 4.1 数据模型层（models/）

**`finding.py`** — Finding 模型（安全发现/漏洞）

```python
Severity(StrEnum): CRITICAL / HIGH / MEDIUM / LOW / INFO
Category(StrEnum): FABRIC_CONFIG / FABRIC_RUNTIME / CHAINCODE / CONTRACT / RPC / WEB3
FindingLocation:       file_path + start_line + end_line
Finding:               包含 rule_id / severity / title / description / location /
                       evidence / remediation / references / confidence / scanner_name
```

- UUID 自动生成唯一标识
- confidence 置信度 0.0~1.0（LOW 级别自动设为 0.6）
- 所有字段强类型校验，杜绝脏数据

**`rule.py`** — Rule 模型（安全规则）

```python
MatchType(StrEnum):  PATTERN / KEY_VALUE / REGEX / MULTI_FILE
MatchCondition:       定义怎么匹配（文件过滤、模式/键值/正则、大小写、反选）
TargetSpec:           定义扫描哪些文件
Rule:                 完整规则（id / name / severity / match / description / remediation）
```

**`scan.py`** — ScanTarget / ScanResult / FindingSummary

```python
ScanTargetType:  fabric_config / fabric_runtime / chaincode / contract / rpc / web3
ScanTarget:      目标类型 + 路径
FindingSummary:  按严重度统计（critical/high/medium/low/info）+ total
ScanResult:      完整扫描结果（findings + summary + 耗时 + 错误列表）
```

---

### 4.2 规则解析器（core/rule_parser.py）

`RuleParser` 负责将 YAML 规则文件解析为 Pydantic Rule 对象：

- `load_rules(rules_dir)` — 递归加载目录下所有 `.yaml` 文件
- 自动容错：YAML 语法错误或格式不正确的规则会被跳过并打印 Warning
- 支持单文件单规则和单文件多规则两种格式

**数据流**：`YAML 文本 → yaml.safe_load → RuleParser._parse_rule_dict → Pydantic Rule 对象`

---

### 4.3 规则执行引擎（core/rule_engine.py）

`RuleEngine` 是核心匹配器，支持 **3 种匹配模式**：

| 模式 | 用途 | 配置项 |
|------|------|--------|
| **PATTERN** | 字符串包含匹配 | `pattern` / `case_sensitive` / `negate` / `file_pattern` |
| **REGEX** | 正则表达式匹配 | `regex` / `case_sensitive` / `negate` / `file_pattern` |
| **KEY_VALUE** | 键值对匹配 | `key` / `value` / `case_sensitive` / `negate` / `file_pattern` |

**关键能力**：

- **文件过滤**：`file_pattern: "docker-compose*"` 只匹配 docker-compose 文件
- **大小写敏感控制**：`case_sensitive: false` 不区分大小写
- **反选模式**：`negate: true` 匹配不符合条件的行（如检测"未开启 TLS"）
- **Docker Compose 兼容**：自动识别 `- KEY=VALUE` 格式的环境变量行
- **容错**：无效正则自动跳过，不会中断整个扫描流程

**执行流程**：
```
Rule + 文件路径 + 文件内容
  → 检查 enabled / file_pattern 过滤
  → 根据 MatchType 分发到 _match_pattern / _match_regex / _match_key_value
  → 返回 [(start_line, end_line, 匹配文本), ...]
```

---

### 4.4 Fabric 配置扫描器（scanners/fabric_config/scanner.py）

`FabricConfigScanner` 实现了 `BaseScanner` 抽象接口：

1. **文件收集** (`_collect_files`)：遍历目标目录，按规则定义的 `target.files` 模式自动收集文件
2. **规则循环**：对每个文件 × 每条规则执行 `RuleEngine.match_file()`
3. **Finding 生成**：每条匹配结果被包装为 `Finding` 对象（含文件位置、证据行、修复建议）
4. **置信度赋值**：LOW 级别自动设 `confidence=0.6`，其他 `1.0`

**默认扫描文件模式**（无规则定制时）：
```
docker-compose.yaml, docker-compose.yml, .env, core.yaml, orderer.yaml, configtx.yaml
```

---

### 4.5 核心调度引擎（core/engine.py）

`CoreEngine` 负责任务调度和结果聚合：

- **ScannerRegistry**：持有所有注册的扫描器列表
- **默认注册**：启动时自动注册 `FabricConfigScanner`
- **插件扩展**：通过 `register_scanner()` 可动态添加新扫描器
- **类型分发**：`get_scanner(target_type)` 按 ScanTargetType 匹配扫描器
- **性能计时**：`time.perf_counter()` 精确计时微秒级
- **异常安全**：扫描器内部异常被捕获为 errors，不中断主流程

---

### 4.6 Public API 层（api/__init__.py）

`scan_fabric(path)` — 唯一的对外入口函数：

```python
from blocksec.api import scan_fabric
result = scan_fabric("./my-fabric-project")
```

- 内部构造 `ScanTarget` → 调用 `CoreEngine.scan()` → 返回 `ScanResult`
- CLI / Web GUI / MCP 都通过这个接口调用，保证结果一致性

---

### 4.7 CLI 命令行（cli/main.py）

| 命令 | 功能 | 参数 |
|------|------|------|
| `blocksec scan fabric` | 运行 Fabric 配置扫描 | `--path` / `-p`（目标路径），`--output` / `-o`（JSON 报告路径） |
| `blocksec rules` | 查看规则库 | 无 |
| `blocksec report` | 报告生成提示 | 无 |

**输出美化**：Rich 表格 + 彩色 Panel，各严重度用不同颜色区分

---

### 4.8 JSON 报告导出器（reports/exporters/json_exporter.py）

`JsonExporter.export(result, path)` 将 `ScanResult` 序列化为 JSON，包含：

- scan_id / target / timestamp / duration
- summary（各严重度计数）
- findings 完整列表（id / rule_id / severity / location / evidence / remediation）
- errors

---

### 4.9 Scanner 抽象基类（scanners/base.py）

```python
class BaseScanner(ABC):
    name: str
    description: str

    can_handle(target_type) → bool    # 是否支持此目标类型
    scan(target_path) → list[Finding]  # 执行扫描
```

所有扫描器必须继承此类，保证 `CoreEngine.scan()` 可以统一调度。

---

### 4.10 5 条 Fabric 安全规则

| 规则 ID | 名称 | 严重度 | 匹配方式 | 检测内容 |
|---------|------|--------|---------|---------|
| FABRIC_PEER_TLS_DISABLED | Peer 节点未开启 TLS | HIGH | KEY_VALUE | `CORE_PEER_TLS_ENABLED=false` |
| FABRIC_ORDERER_TLS_DISABLED | Orderer 节点未开启 TLS | HIGH | KEY_VALUE | `ORDERER_GENERAL_TLS_ENABLED=false` |
| FABRIC_COUCHDB_EXPOSED | CouchDB 端口暴露 | HIGH | REGEX | 端口映射非 localhost 的 5984 |
| FABRIC_PLAINTEXT_PASSWORD | 明文密码 | MEDIUM | REGEX | `password=/pwd=/secret=` 等模式 |
| FABRIC_DEBUG_LOG_ENABLED | DEBUG 日志开启 | LOW | KEY_VALUE | `FABRIC_LOGGING_SPEC=debug` |

每条规则包含：id / name / severity / description / remediation / references / false_positive_note

---

### 4.11 本地靶场

| 靶场 | 路径 | 状态 | 检出结果 |
|------|------|------|---------|
| fabric-safe | `labs/fabric-safe/` | TLS 全部开启 + 端口绑定 localhost | 0 漏洞 |
| fabric-vuln-couchdb-exposed | `labs/fabric-vuln-couchdb-exposed/` | TLS 关闭 + CouchDB 暴露 + 明文密码 + DEBUG 日志 | 7 个漏洞 |

每个靶场含 `expected_findings.json`，用于自动化验证扫描结果。

---

### 4.12 测试体系

| 测试文件 | 类型 | 数量 | 覆盖内容 |
|---------|------|------|---------|
| `tests/unit/test_rule_engine.py` | 单元 | 14 | PATTERN 5 + REGEX 4 + KEY_VALUE 5 |
| `tests/unit/test_rule_parser.py` | 单元 | 4 | 规则加载 / 严重度校验 / 必填字段 / 空目录 |
| `tests/unit/test_rule_engine.py` | 单元 | 1 | FindingSummary 统计 |
| `tests/integration/test_scan.py` | 集成 | 5 | safe靶场 / vuln靶场 / expected对比 / 不存在路径 / JSON导出 |
| `tests/integration/test_scan.py` | 集成 | 3 | 额外验证（子测试） |

---

## 五、不需要你关心的内容

以下目录在当前版本中只是占位，**没有实现任何功能**：

- `blocksec/config/` — 配置管理（空壳）
- `blocksec/mcp/` — MCP Server（后期）
- `blocksec/scanners/fabric_runtime/` — 运行时扫描（v0.2）
- `blocksec/scanners/smart_contract/` — 合约扫描（v0.5）
- `blocksec/scanners/rpc/` — RPC 扫描（v0.6）
- `blocksec/scanners/web3/` — Web3 扫描（v0.6）
- `blocksec/reports/templates/` — HTML/Markdown 模板（v0.3）
- `tests/e2e/` — 端到端测试（v0.2+）
- `docs/` — 文档目录（空）
- `labs/fabric-vuln-tls-disabled/` — 更细粒度靶场（后续扩充）

---

## 六、项目目录结构

```
blocksecscan/
├── pyproject.toml                          # 项目配置
├── README.md                               # 项目说明
├── .gitignore                              # 忽略规则
│
├── blocksec/                               # 主包
│   ├── __init__.py                         # 版本号
│   ├── cli/main.py                         # ✅ CLI 入口
│   ├── api/__init__.py                     # ✅ Public API
│   ├── core/
│   │   ├── engine.py                       # ✅ 核心引擎
│   │   ├── rule_engine.py                  # ✅ 规则执行
│   │   └── rule_parser.py                  # ✅ 规则解析
│   ├── models/
│   │   ├── finding.py                      # ✅ Finding 模型
│   │   ├── rule.py                         # ✅ Rule 模型
│   │   └── scan.py                         # ✅ ScanTarget/Result/Summary
│   ├── scanners/
│   │   ├── base.py                         # ✅ 抽象基类
│   │   └── fabric_config/scanner.py        # ✅ Fabric 扫描器
│   ├── rules/fabric/                       # ✅ 5条规则
│   │   ├── tls_peer.yaml
│   │   ├── tls_orderer.yaml
│   │   ├── couchdb_exposed.yaml
│   │   ├── plaintext_password.yaml
│   │   └── debug_log.yaml
│   └── reports/exporters/
│       └── json_exporter.py                # ✅ JSON 导出
│
├── labs/
│   ├── fabric-safe/                        # ✅ 安全配置靶场
│   └── fabric-vuln-couchdb-exposed/        # ✅ 漏洞配置靶场
│
└── tests/
    ├── unit/
    │   ├── test_rule_engine.py             # ✅ 14 测试
    │   └── test_rule_parser.py             # ✅ 4 测试
    └── integration/
        └── test_scan.py                    # ✅ 8 测试
```

> ✅ = 已实现并测试通过  
> 空目录 = 占位，未实现

---

## 七、v1 完整版功能规划一览

v1 是 BlockSecScan 的完整版，分为 8 个版本阶段逐步迭代。以下是全部规划功能：

### v0.1 ✅ 已完成 — Fabric 配置安全扫描（就是你现在这个版本）

```
✅ Fabric 配置安全扫描（5条规则：TLS/CouchDB/密码/日志）
✅ CLI 命令（Typer + Rich）
✅ JSON 报告
✅ 2 个本地靶场
✅ 27 个测试全通过
```

### v0.2 — Fabric 增强版

新增“运行时扫描”——不再是静态读配置文件，而是检测 **正在运行的** Fabric 环境：

- `docker ps` 查看容器状态
- `docker inspect` 检查容器权限（是否 root）、挂载卷、网络模式
- 端口开放情况扫描（Peer 7051/Orderer 7050/CouchDB 5984 是否对外暴露）
- TLS 握手验证（真实连接测试，不只是配置文件检查）
- CouchDB 可访问性检测（HTTP 请求尝试）
- 证书有效期检测（解析证书文件中的 NotAfter 字段）
- 新命令：`blocksec scan fabric-runtime --local`

### v0.3 — 报告和工程化

- **Markdown 报告**：用 Jinja2 模板渲染 Markdown，适合论文和文档
- **SARIF 报告**：对接 GitHub Code Scanning，提交代码时自动在 GitHub 上显示安全问题
- **GitHub Action**：CI/CD 集成，每次 push/PR 自动扫描
- 规则文档完善
- 测试覆盖率提升到 80%+

### v0.4 — Web GUI

- 后端：FastAPI + SQLite
- 前端：Vue 3 / React + TypeScript + TailwindCSS
- 页面：
  - 首页仪表盘（漏洞趋势、风险分布图 ECharts）
  - 项目列表管理
  - 创建扫描任务（选择目标、规则集）
  - 扫描进度实时显示
  - 漏洞列表（筛选、排序、搜索）
  - 漏洞详情（风险描述 + 修复建议 + 参考链接）
  - 规则管理（增删改查 YAML 规则）
  - 报告下载
  - AI 分析页面（v1.1 阶段）
  - 系统设置

### v0.5 — 智能合约扫描（Solidity / EVM）

不走从零写静态分析器，而是**集成现有成熟工具**：

- 集成 **Slither**（Trail of Bits 出品，业界标准 Solidity 静态分析）
- 调用 Slither → 解析其 JSON 输出 → 映射到统一 Finding 模型
- 覆盖漏洞：重入攻击、访问控制、tx.origin、整数溢出、不安全随机数、代理升级风险、闪电贷、预言机操纵
- 映射到 **OWASP Smart Contract Top 10** 分类标准
- 可选集成 Mythril、Solhint、Foundry
- 命令行：`blocksec scan contract --path ./hardhat-project`
- 中文漏洞解释和修复建议

### v0.6 — Web3 前端 + 区块链 RPC 扫描

**Web3 前端扫描**：

- 扫描 React/Vue/Next.js 项目源码
- 检测：私钥硬编码、RPC Key 泄露、合约地址硬编码
- 检测：危险 approve 调用、无限授权、不安全 signMessage
- 检测：npm 依赖漏洞（集成 npm audit）
- 检测：CSP 缺失、XSS 风险、钓鱼跳转、第三方 JS 风险

**区块链 RPC 节点扫描**：

- 扫描 Ethereum/Geth/Erigon/Nethermind RPC 端点
- 检测：RPC 端口 8545/8546 暴露、admin/personal/debug namespace 开放
- 检测：CORS 配置、认证缺失、客户端版本泄露
- 命令行：`blocksec scan rpc --target http://127.0.0.1:8545`
- 包含运行时安全确认提示（非 localhost 目标需二次确认）

### v1.0 — 正式开源版

- 完整 README（中英文）
- 完整使用文档
- Docker 镜像发布（一键部署扫描环境）
- GitHub Action 市场发布
- 示例靶场整理（带有教学说明）
- 贡献指南（CONTRIBUTING.md）
- Apache-2.0 License 文件
- GitHub Release 发布
- PyPI 包发布（`pip install blocksecscan`）

### v1.1 — AI + MCP 版本

**MCP Server**：让 AI（如 Claude、Codex、Cursor）通过标准协议调用扫描能力

- MCP Tools：
  - `scan_fabric_path` — AI 调用扫描
  - `get_scan_result` — 获取历史结果
  - `explain_finding` — 解释漏洞
  - `suggest_fix` — 生成修复建议
  - `list_rules` / `get_rule_detail` — 规则查询
  - `generate_report` — 生成报告

- MCP Resources：`blocksec://scans/latest` 等资源 URI

- MCP Prompts：内置提示词模板
  - 总结扫描报告
  - 生成修复方案
  - 撰写论文实验分析
  - 误报分析

**AI 功能分阶段**：

1. **AI 漏洞解释**：输入规则 ID + 证据行，输出中文风险说明
2. **AI 修复建议**：具体到哪个文件哪一行怎么改、为什么、改完怎么验证
3. **AI 报告总结**：统计高危中危低危，总结风险集中点
4. **AI 辅助规则编写**：用户说"检测 5984 端口暴露"，AI 生成对应 YAML 规则

---

## 八、已用到的技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.11 | 全部后端逻辑 |
| 数据校验 | Pydantic v2 | 所有数据传输对象 |
| CLI | Typer | 命令行入口 |
| 终端美化 | Rich | 彩色表格和面板 |
| YAML | PyYAML | 规则文件解析 |
| 测试 | pytest | 单元 + 集成测试 |
| Lint | ruff | 代码质量检查 |

---

## 九、下一步建议

1. **v0.2 扩展**：增加 2-3 条规则（私钥泄露、证书过期、容器 root 权限），对应增加靶场
2. **Markdown 报告**：用 Jinja2 模板输出适合论文的格式化报告
3. **论文素材**：用现有数据写实验分析章节

---

## 十、开发记录

```
2026-05-06  初始化项目结构 + pyproject.toml + Git
2026-05-06  Pydantic 数据模型 (Finding, Rule, ScanTarget, ScanResult)
2026-05-06  RuleParser + RuleEngine (3种匹配模式)
2026-05-06  5条 Fabric 安全规则
2026-05-06  FabricConfigScanner + CoreEngine
2026-05-06  Public API + CLI 命令
2026-05-06  JSON 报告导出器
2026-05-06  2个本地靶场 + expected_findings
2026-05-06  27个测试全通过
2026-05-06  推送 GitHub: https://github.com/FECES-SHIT/BlockSecScan
```

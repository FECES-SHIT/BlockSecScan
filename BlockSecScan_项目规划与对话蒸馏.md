# BlockSecScan 项目规划与对话蒸馏

> 项目暂定名：**BlockSecScan**  
> 项目类型：区块链安全扫描平台 / 毕业设计 / GitHub 开源项目  
> 核心方向：**Hyperledger Fabric 联盟链安全基线扫描**  
> 长期扩展：智能合约扫描、Web3 应用扫描、区块链 RPC 扫描、MCP + AI 安全助手

---

## 0. 文档用途

本文档用于记录当前毕业设计与开源项目的完整规划，方便后续：

1. 自己继续深化项目设计；
2. 给导师说明选题方向；
3. 给其他 AI 或开发助手快速理解上下文；
4. 作为 GitHub README / docs 的基础材料；
5. 作为毕业论文需求分析、系统设计、实验方案的参考。

---

## 1. 个人背景与需求

### 1.1 个人背景

- 当前身份：大学生；
- 专业：区块链工程；
- 主学方向：网络安全；
- 区块链基础：了解基础概念，但缺乏实际项目经验；
- 毕业设计要求：必须和区块链专业相关，相关度可以不特别高，但必须体现区块链研究对象；
- 个人偏好：
  - 希望项目实际有用；
  - 希望功能尽可能完整；
  - 希望后续开源到 GitHub；
  - 希望支持多平台；
  - 希望未来集成 AI；
  - 希望 AI 能通过 MCP 接入。

### 1.2 初始想法

最开始希望做一个“漏洞扫描系统”，但传统 Web 漏洞扫描和区块链工程专业的关联度不够。

因此需要把研究对象调整为以下区块链相关对象：

- 区块链节点；
- Hyperledger Fabric 联盟链节点；
- Fabric 链码；
- 智能合约；
- Web3 应用；
- 区块链 RPC 服务。

---

## 2. 对 Fabric 的基础理解

### 2.1 Fabric 是什么

**Hyperledger Fabric** 是一个企业级联盟链平台。

它不像比特币、以太坊这种开放式公链，而更适合企业、机构之间组成有权限控制的联盟链网络。

可以简单理解为：

> Fabric 不是网页，而是一套企业内部或多组织之间使用的区块链后台基础设施。

### 2.2 Web 与 Fabric 的区别

| 对比项 | Web 应用 | Fabric 应用 |
|---|---|---|
| 用户看到的形式 | 网页、小程序、后台系统 | 通常不是直接可见，而是作为后端基础设施 |
| 核心组件 | 前端、后端、数据库 | Peer、Orderer、Channel、Chaincode、Ledger、MSP |
| 数据存储 | MySQL、PostgreSQL、Redis 等 | 区块链账本 Ledger、状态数据库 CouchDB/LevelDB |
| 身份认证 | 用户名密码、Token、OAuth | 证书、MSP、组织身份 |
| 业务逻辑 | 后端代码 | 链码 Chaincode |
| 调用方式 | HTTP API | Fabric SDK / Gateway 调用链码 |

### 2.3 一个典型 Fabric 应用的结构

```text
用户浏览器 / 小程序 / 后台管理系统
        ↓
普通 Web 后端服务
        ↓
Fabric SDK / Gateway
        ↓
Fabric Peer 节点
        ↓
链码 Chaincode
        ↓
区块链账本 Ledger
```

例如，一个农产品溯源系统中：

- 用户看到的是网页；
- 后端调用 Fabric 链码；
- 链码查询或写入账本；
- 多个企业组织共同维护数据可信性。

---

## 3. 项目总定位

### 3.1 毕业设计题目建议

毕业设计建议题目收敛一点：

> **《面向 Hyperledger Fabric 联盟链系统的安全基线扫描平台设计与实现》**

或者：

> **《面向 Fabric 链节点的安全配置漏洞扫描系统设计与实现》**

### 3.2 GitHub 开源项目定位

开源项目可以定位得更大：

> **BlockSecScan: A multi-platform blockchain security scanner for Fabric networks, smart contracts, Web3 applications, RPC services, and AI-assisted security analysis.**

中文描述：

> **BlockSecScan 是一个面向 Fabric 联盟链、智能合约、Web3 应用和区块链 RPC 服务的多平台安全扫描工具。**

### 3.3 核心设计原则

项目不应该只是一个简单脚本，而应该设计成一个可扩展平台。最核心的设计原则有两条：

#### 原则一：Core Engine 独立 + Public API 层

所有入口（CLI、Web GUI、GitHub Action、MCP Server）都通过同一个 Public API 调用 Core Engine，而不是各入口直接 import 内部模块：

```text
CLI / Web GUI / 桌面 GUI / GitHub Action / MCP Server
        │
        ▼
   Public API Layer（统一的对外接口，稳定的调用契约）
        │
        ▼
   Core Engine（内部实现可自由重构，不影响上层入口）
```

这样设计的好处：

1. Core Engine 内部重构时，只要 Public API 不变，所有入口都不需要改动 —— 这是解耦的第一道防线；
2. 易于编写自动化测试（直接调用 Public API 即可模拟各种入口行为）；
3. 第三方开发者也可以通过 Public API 集成扫描能力；
4. 强制解耦：CLI 不能直接访问扫描器内部，GUI 不能直接操作规则文件。

#### 原则二：插件化扫描器

不要让 Core Engine 硬编码所有扫描器的调用逻辑。定义 **Scanner 抽象接口**，各扫描器作为独立插件注册到 Core Engine：

```text
Core Engine
  ├── ScannerRegistry（扫描器注册中心）
  │     ├── FabricConfigScanner
  │     ├── FabricRuntimeScanner
  │     ├── FabricChaincodeScanner
  │     ├── SmartContractScanner
  │     ├── RpcScanner
  │     └── Web3Scanner
  │
  └── 扫描调度器（遍历注册的扫描器，收集结果）
```

好处：

- 新增扫描器不影响已有代码（开闭原则）；
- 毕业设计阶段只做 Fabric 配置扫描，后续扩展直接加新插件，不动 Core Engine；
- 开源社区贡献者可以写自己的扫描器插件，不需要理解整个引擎。

---

## 4. 总体架构

### 4.1 分层架构图

```text
┌─────────────────────────────────────────────────────┐
│                    入口层 Entry Layer                 │
│  CLI (Typer)  │  Web GUI (FastAPI)  │  MCP Server    │
│         桌面 GUI (Tauri)  │  GitHub Action            │
└──────────────────────┬──────────────────────────────┘
                       │ 统一调用
                       ▼
┌─────────────────────────────────────────────────────┐
│               Public API Layer（对外接口）            │
│  scan()  │  get_result()  │  list_rules()            │
│  generate_report()  │  explain_finding()              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                   Core Engine（核心引擎）              │
│  ┌───────────────────────────────────────────────┐  │
│  │         ScannerRegistry（扫描器注册中心）       │  │
│  │  FabricConfigScanner                          │  │
│  │  FabricRuntimeScanner                         │  │
│  │  FabricChaincodeScanner                       │  │
│  │  SmartContractScanner                         │  │
│  │  RpcScanner                                   │  │
│  │  Web3Scanner                                  │  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │  Rule Engine  │  │ Scan Scheduler│                 │
│  │  (规则解析+执行)│  │ (扫描调度)    │                 │
│  └──────────────┘  └──────────────┘                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                 数据与基础设施层                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Models   │  │  Config   │  │  Report Engine    │  │
│  │ (Pydantic)│  │ (Settings)│  │  (JSON/HTML/MD/   │  │
│  │           │  │           │  │   SARIF)          │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │             Rules (YAML 规则文件)              │   │
│  │  fabric/  │  rpc/  │  contract/  │  web3/     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 4.2 模块依赖方向（必须单向，禁止循环引用）

```text
Models（最底层，无任何内部依赖）
  ↑
Rule Engine（依赖 Models）
  ↑
Scanners（依赖 Models + Rule Engine）
  ↑
Core Engine（依赖 Scanners + Rule Engine + Models）
  ↑
Public API（依赖 Core Engine + Models）
  ↑
CLI / Web GUI / MCP / GitHub Action（依赖 Public API + Models）
```

> ⚠️ 如果发现下层 import 上层，说明架构出了问题，必须立刻修正。

### 4.3 各模块职责边界

| 模块 | 职责 | 不可做的事 |
|------|------|-----------|
| Models | 定义所有核心数据结构（ScanTarget, Rule, Finding, ScanResult, Report） | 不包含任何 IO 或业务逻辑 |
| Rule Engine | 解析 YAML 规则文件 → 规则对象；根据规则匹配文本/配置 | 不直接操作文件系统扫描 |
| Scanners | 读取目标文件/环境 → 调用 Rule Engine 匹配 → 返回 Finding 列表 | 不生成报告 |
| Core Engine | 调度扫描器 → 聚合 Finding → 风险评级 → 返回 ScanResult | 不格式化输出 |
| Public API | 对外暴露统一接口，参数校验，权限检查 | 不包含扫描逻辑 |
| Report Engine | 接收 ScanResult → 按模板生成 JSON/HTML/MD/SARIF | 不参与扫描 |
| Entry Layer | CLI 参数解析、Web 路由、MCP 协议处理 | 不直接调用内部 Scanner |

### 4.4 数据流（一次完整扫描的生命周期）

```text
 1. 用户调用 CLI/Web/MCP
        │
 2. Entry Layer 解析参数，构造 ScanTarget 对象
        │
 3. 调用 Public API（如 api.scan(target)）
        │
 4. Public API 校验参数，转发给 Core Engine
        │
 5. Core Engine 从 ScannerRegistry 获取匹配的 Scanner 列表
        │
 6. 遍历 Scanner，每个 Scanner：
    a. 读取目标文件/环境
    b. 加载对应类别的 Rule
    c. 调用 Rule Engine 执行匹配
    d. 产生 Finding 列表
        │
 7. Core Engine 汇总所有 Finding，去重，计算风险评分
        │
 8. 返回 ScanResult 对象给 Public API
        │
 9. Public API 返回给 Entry Layer
        │
10. 用户可进一步调用 generate_report(scan_result, format="html")
        → Report Engine 渲染模板 → 输出报告文件
```

### 4.5 数据模型层设计（Models）

所有模块之间传递 Pydantic 模型对象，而不是裸 dict。核心数据模型建议尽早定型，因为这些结构会贯穿 CLI、API、数据库、报告、MCP 等所有环节。初期设计多花一小时，后期少改三天。

**ScanTarget** — 扫描目标：
- `target_type`：fabric_config / fabric_runtime / contract / rpc / web3
- `path`：目标路径（文件系统扫描时）
- `host`：目标主机地址（网络扫描时）
- `options`：额外扫描选项 dict

**Rule** — 规则对象（YAML 解析后的结构）：
- `id`、`name`、`category`、`severity`
- `target`：目标类型描述
- `match`：匹配条件（pattern / key-value / regex 等）
- `description`、`remediation`、`references`
- `false_positive_note`：误报说明

**Finding** — 发现的漏洞/风险（一次匹配产生一个 Finding）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 唯一标识 |
| `rule_id` | str | 关联的规则 ID |
| `severity` | enum | CRITICAL / HIGH / MEDIUM / LOW / INFO |
| `category` | enum | FABRIC_CONFIG / FABRIC_RUNTIME / CHAINCODE / CONTRACT / RPC / WEB3 |
| `title` | str | 一句话标题 |
| `description` | str | 详细风险描述 |
| `file_path` | str | 发现位置的文件路径 |
| `line_number` | int (optional) | 行号 |
| `evidence` | str | 证据片段（匹配到的具体内容） |
| `remediation` | str | 修复建议 |
| `references` | list[str] | 参考链接列表 |
| `confidence` | float 0.0-1.0 | 置信度（帮助误报分析） |

**ScanResult** — 一次扫描的完整结果：
- `scan_id`：扫描唯一标识
- `target`：ScanTarget 对象
- `timestamp`：扫描时间
- `findings`：List[Finding]
- `summary`：统计摘要（critical/high/medium/low/info 各自计数）
- `duration`：扫描耗时（秒）

**Report** — 报告对象：
- `report_id`、`scan_result` 引用、`format`（json/html/markdown/sarif）、`generated_at`

### 4.6 配置管理统一化

项目中会存在多类配置，建议使用单一配置管理方案（推荐 Pydantic Settings），而不是到处散落 `os.getenv()` 或硬编码路径。

配置覆盖优先级（从高到低）：

```text
CLI 参数 > 环境变量 > 用户配置文件 > 项目默认配置
```

示例配置项：
- 规则文件目录路径
- 报告输出目录
- 默认报告格式
- 扫描超时时间
- AI 模型配置（后期）
- 数据库路径（Web GUI 阶段）

### 4.7 报告生成与扫描引擎分离

扫描过程本身不生成报告，只产出 `ScanResult` 对象。报告生成是独立的后置步骤：

```text
扫描 → ScanResult 对象 → ReportGenerator → 报告文件
```

不同报告格式通过不同 `Exporter` 实现，各自独立：
- `JsonExporter`：输出 JSON
- `HtmlExporter`：基于 Jinja2 模板渲染 HTML
- `MarkdownExporter`：输出 Markdown
- `SarifExporter`：输出 SARIF（对接 GitHub Code Scanning）

新增报告格式时完全不碰扫描逻辑，只需新增一个 Exporter 文件。

### 4.8 规则系统的分层解耦

规则系统分三层，各层独立：

```text
规则定义层（YAML 文件，纯数据，人类可读可写）
       │
       ▼
规则解析层（RuleParser：YAML → Pydantic Rule 对象）
       │
       ▼
规则执行层（RuleEngine：Rule 对象 → 文本/配置匹配 → Finding）
       │
       ▼
结果收集层（Scanner：汇总 Finding，去重，计算置信度）
```

分层的好处：
- 更换规则格式（比如将来支持 JSON 规则或 TOML 规则）只需改解析层；
- 匹配逻辑优化（比如改用更高效的文本搜索算法）不影响规则定义；
- 可以为不同扫描器类型提供不同的匹配策略（文件内容匹配 vs 网络响应匹配 vs AST 分析）；
- 规则作者不需要理解匹配引擎的实现细节。

---

## 5. 功能模块设计

## 5.1 Fabric 配置安全扫描

这是毕业设计的主线，也是最建议优先实现的模块。

### 5.1.1 扫描对象

```text
docker-compose.yaml
core.yaml
orderer.yaml
configtx.yaml
connection profile
.env
crypto-config
organizations
MSP 目录
证书目录
链码目录
```

### 5.1.2 主要检测项

| 类型 | 检测项 | 风险说明 |
|---|---|---|
| TLS 安全 | Peer 是否开启 TLS | 未开启 TLS 可能导致节点通信被窃听或篡改 |
| TLS 安全 | Orderer 是否开启 TLS | 排序节点通信风险 |
| 证书安全 | 证书是否过期 | 过期证书可能导致节点通信失败或安全风险 |
| 证书安全 | 私钥文件是否进入项目目录 | 私钥泄露属于高危风险 |
| Docker 安全 | 容器是否使用 root | 容器逃逸或权限扩大风险 |
| Docker 安全 | 是否挂载敏感目录 | 可能导致宿主机敏感文件暴露 |
| 端口暴露 | CouchDB 5984 是否暴露 | 可能导致状态数据库被未授权访问 |
| 端口暴露 | Peer / Orderer 端口是否对外暴露过多 | 增大攻击面 |
| 账户安全 | 是否存在默认密码 | 容易被暴力破解或直接登录 |
| 账户安全 | 是否存在明文密码 | 配置泄露后风险高 |
| 日志安全 | 是否开启 DEBUG 日志 | 可能泄露交易、证书、路径等敏感信息 |
| Fabric 策略 | 背书策略是否过弱 | 单组织即可背书可能降低可信性 |
| 访问控制 | ACL 是否过宽 | 非授权用户可能调用关键操作 |
| 敏感信息 | 是否硬编码 token、secret、private key | 高危 |

### 5.1.3 示例风险

#### TLS 未开启

```yaml
CORE_PEER_TLS_ENABLED=false
```

输出：

```text
高危：Peer 节点未开启 TLS，节点间通信可能被窃听或篡改。
建议开启 TLS，并配置证书、私钥和根 CA 文件。
```

#### CouchDB 暴露

```yaml
ports:
  - "5984:5984"
```

输出：

```text
高危：CouchDB 服务暴露到宿主机，可能导致状态数据库被未授权访问。
建议删除外部端口映射，仅允许 Peer 通过 Docker 内部网络访问 CouchDB。
```

---

## 5.2 Fabric 运行时扫描

此模块用于扫描正在运行的 Fabric 环境。

### 5.2.1 扫描对象

```text
Docker 容器
本机端口
Peer 节点
Orderer 节点
CouchDB
Fabric CA
```

### 5.2.2 检测内容

```text
docker ps
docker inspect
端口开放情况
TLS 握手检测
CouchDB 是否可访问
Peer / Orderer 服务识别
容器权限检测
容器网络检测
```

### 5.2.3 命令示例

```bash
blocksec scan fabric-runtime --local
blocksec scan fabric-runtime --host 127.0.0.1
```

### 5.2.4 安全边界

默认只建议扫描：

- 本机环境；
- 自建实验环境；
- 学校实验室授权环境；
- 企业明确授权环境。

不鼓励对公网未知目标进行扫描。

---

## 5.3 Fabric 链码安全扫描

Fabric 链码可以理解为联盟链中的智能合约。

### 5.3.1 扫描语言

```text
Go
Node.js
Java
```

### 5.3.2 检测内容

| 风险 | 示例 |
|---|---|
| 缺少身份校验 | 没有判断调用者组织、角色、属性 |
| 参数校验不足 | 直接使用用户输入写入账本 |
| 非确定性逻辑 | 使用当前时间、随机数 |
| 外部网络调用 | 链码访问外部 HTTP API |
| 敏感信息硬编码 | 写死密码、token、密钥 |
| 访问控制过宽 | 所有人都能修改关键资产 |
| 富查询风险 | CouchDB 查询没有权限过滤 |

### 5.3.3 示例规则思路

```text
检测链码中是否出现：
- time.Now()
- Math.random()
- http.Get()
- password =
- secret =
- privateKey =
- 未调用 GetClientIdentity()
```

---

## 5.4 智能合约扫描

此模块主要面向 Solidity / EVM。

### 5.4.1 推荐实现方式

不要一开始从零写完整静态分析器，可以集成成熟工具：

```text
Slither
Mythril，可选
Solhint，可选
Foundry，可选
```

平台主要负责：

```text
统一调用外部工具
解析扫描结果
漏洞去重
风险评级
中文解释
生成报告
映射到 OWASP Smart Contract Top 10
```

### 5.4.2 检测内容

```text
重入攻击
访问控制问题
未检查外部调用
tx.origin 使用
整数问题
不安全随机数
代理升级风险
权限过大
闪电贷相关风险
预言机操纵风险
```

### 5.4.3 命令示例

```bash
blocksec scan contract --path ./hardhat-project
```

---

## 5.5 区块链 RPC 节点扫描

此模块非常贴近网络安全。

### 5.5.1 扫描对象

```text
Ethereum / Geth / Erigon / Nethermind RPC
HTTP RPC
WebSocket RPC
```

### 5.5.2 常见端口

```text
8545  HTTP RPC
8546  WebSocket RPC
30303 P2P
```

### 5.5.3 检测内容

```text
RPC 是否暴露
是否允许 web3_clientVersion
是否开放 admin namespace
是否开放 personal namespace
是否开放 debug namespace
CORS 是否为 *
是否缺少认证
是否泄露客户端版本
```

### 5.5.4 命令示例

```bash
blocksec scan rpc --target http://127.0.0.1:8545
```

### 5.5.5 注意事项

此模块应强调：

> 仅用于授权测试、自有资产检测、教学实验环境，不用于未授权公网扫描。

---

## 5.6 Web3 前端应用扫描

此模块让项目更接近真实 Web3 安全工具。

### 5.6.1 扫描对象

```text
React 项目
Vue 项目
Next.js 项目
前端源码
package.json
.env
钱包连接代码
合约交互代码
```

### 5.6.2 检测内容

```text
私钥硬编码
RPC Key 泄露
合约地址硬编码
危险 approve 调用
无限授权风险
不安全 signMessage
依赖漏洞
CSP 缺失
XSS 风险
钓鱼跳转
第三方 JS 风险
```

### 5.6.3 命令示例

```bash
blocksec scan web3 --path ./frontend
```

---

## 6. 多平台兼容设计

## 6.1 统一核心原则

最重要的设计原则：

> 核心扫描引擎独立，不依赖 CLI，也不依赖 GUI。

调用关系：

```text
CLI       ┐
Web GUI   ├── 调用 Core Engine
桌面 GUI  │
Action    │
MCP       ┘
```

这样做的好处：

1. 减少重复代码；
2. 后续扩展平台更容易；
3. 开源项目结构更清晰；
4. GUI 和 CLI 结果一致；
5. MCP / AI 可以直接复用扫描能力。

---

## 6.2 CLI 命令行

CLI 是第一优先级，因为安全工具最适合先做 CLI。

### 6.2.1 示例命令

```bash
# 扫描 Fabric 项目目录
blocksec scan fabric --path ./fabric-network

# 扫描正在运行的 Fabric 环境
blocksec scan fabric-runtime --local

# 扫描智能合约项目
blocksec scan contract --path ./hardhat-project

# 扫描 RPC 节点
blocksec scan rpc --target http://127.0.0.1:8545

# 扫描 Web3 前端项目
blocksec scan web3 --path ./frontend

# 生成报告
blocksec report --format html

# 查看规则
blocksec rules list
```

### 6.2.2 CLI 技术建议

```text
Python Typer
Rich 美化输出
Pydantic 校验参数
```

---

## 6.3 Web GUI

Web GUI 最适合跨平台。

Windows、macOS、Linux 都可以通过浏览器访问。

### 6.3.1 页面设计

```text
首页仪表盘
项目列表
新建扫描任务
扫描进度
漏洞列表
漏洞详情
规则管理
报告下载
AI 分析页面
系统设置
```

### 6.3.2 技术建议

```text
后端：FastAPI
前端：Vue 3 或 React
图表：ECharts
数据库：SQLite / PostgreSQL
```

---

## 6.4 桌面 GUI

桌面 GUI 可以后期做。

推荐路线：

```text
第一阶段：Web GUI
第二阶段：使用 Tauri 打包成桌面应用
```

好处：

- 同一套前端可以复用；
- 比 PyQt/PySide 更适合和 Web 端共享代码；
- 可以打包 Windows / macOS / Linux。

---

## 6.5 GitHub Action

GitHub Action 能让项目真正融入开发流程。

### 6.5.1 使用场景

用户每次提交代码时自动扫描：

```yaml
name: BlockSecScan

on:
  push:
  pull_request:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run BlockSecScan
        run: |
          pip install blocksecscan
          blocksec scan fabric --path . --output report.sarif
```

### 6.5.2 SARIF 输出

建议支持 SARIF，因为它可以接 GitHub Code Scanning。

---

## 7. AI + MCP 设计

## 7.1 MCP 在项目中的作用

MCP 可以理解为：

> 让 AI 助手通过标准协议调用你的工具、读取你的扫描结果、理解你的规则库。

你的设计不是把 AI 写死在扫描器里，而是单独做：

> **blocksec-mcp-server**

架构：

```text
AI 客户端
  ↓
MCP Server
  ↓
BlockSecScan Core
  ↓
扫描结果 / 规则库 / 报告
```

---

## 7.2 MCP Tools 设计

可以暴露以下工具：

```text
scan_fabric_path
scan_fabric_runtime
scan_contract_path
scan_rpc_target
scan_web3_path
get_scan_result
get_finding_detail
generate_report
explain_finding
suggest_fix
list_rules
get_rule_detail
compare_scan_results
```

### 示例调用流程

```text
用户问 AI：
请帮我扫描这个 Fabric 项目目录，并解释高危漏洞。

AI 调用：
scan_fabric_path("./fabric-network")

MCP Server 返回：
JSON 扫描结果

AI 再调用：
get_finding_detail("FABRIC_TLS_DISABLED")
explain_finding("FABRIC_TLS_DISABLED")

最终 AI 输出：
漏洞解释 + 修复建议 + 风险总结
```

---

## 7.3 MCP Resources 设计

Resources 用于让 AI 读取已有信息。

可以设计成：

```text
blocksec://scans/latest
blocksec://scans/{scan_id}
blocksec://findings/{finding_id}
blocksec://rules
blocksec://rules/{rule_id}
blocksec://reports/{scan_id}/html
blocksec://reports/{scan_id}/markdown
```

---

## 7.4 MCP Prompts 设计

可以内置提示词模板：

```text
summarize_scan_report
explain_fabric_risk
write_remediation_plan
generate_thesis_experiment_analysis
analyze_false_positive
generate_github_issue
generate_rule_from_description
```

### 示例 Prompt 能力

用户问：

```text
帮我把这次扫描结果写成毕业论文实验分析部分。
```

AI 可以：

1. 通过 MCP 读取扫描结果；
2. 统计漏洞数量；
3. 总结高危、中危、低危；
4. 生成实验分析文字；
5. 给出局限性分析。

---

## 7.5 AI 功能分阶段

### 第一阶段：AI 漏洞解释

输入：

```json
{
  "rule_id": "FABRIC_TLS_DISABLED",
  "severity": "HIGH",
  "evidence": "CORE_PEER_TLS_ENABLED=false"
}
```

输出：

```text
该 Peer 节点未开启 TLS，节点间通信可能被窃听或篡改。
建议开启 TLS，并配置证书、私钥和根 CA 文件。
```

### 第二阶段：AI 修复建议

生成：

```text
应该修改哪个配置文件
应该修改哪一行
为什么这样改
改完如何验证
```

### 第三阶段：AI 报告总结

生成：

```text
本次扫描共发现高危 3 个、中危 5 个、低危 4 个。
风险主要集中在 TLS、CouchDB 暴露和私钥文件保护方面。
```

### 第四阶段：AI 辅助规则编写

用户说：

```text
我想检测 docker-compose 里是否暴露 5984 端口。
```

AI 生成一条 YAML 规则。

---

## 8. 技术栈建议

## 8.1 后端 / 扫描核心

```text
Python 3.11+
FastAPI（Web API）
Typer（CLI）
Pydantic v2（数据校验，务必用 v2，性能比 v1 大幅提升）
PyYAML（YAML 规则解析）
Jinja2（HTML 报告模板渲染）
Rich（终端美化输出）
SQLite（轻量数据库）
```

选择 Python 的原因：

- 安全工具生态好；
- 规则引擎实现简单；
- 方便调用 Slither 等工具；
- 方便接入 AI；
- 适合快速实现毕业设计。

**不建议毕业设计阶段过早引入的：**

| 不推荐 | 原因 | 何时引入 |
|--------|------|---------|
| SQLAlchemy ORM | v0.1 阶段数据模型简单，原生 SQL 或轻量 DB 封装即可，ORM 映射成本不值得 | Web GUI 阶段 |
| Celery / 消息队列 | 毕业设计阶段扫描任务量不大，不需要异步任务队列 | 生产化阶段 |
| Docker 化部署 | CLI 工具优先，先让功能跑通再容器化 | v1.0 阶段 |
| Redis | 无缓存/会话需求 | Web GUI 多用户阶段 |

**项目管理工具建议：**

```text
pyproject.toml  作为唯一项目配置文件
uv 或 poetry   做依赖管理（uv 更快，poetry 更成熟）
ruff            做 linting 和 formatting（比 flake8 + black + isort 快 10-100 倍）
mypy 或 pyright 做静态类型检查
pytest          做测试框架
```

---

## 8.2 前端

```text
Vue 3 或 React
TypeScript
TailwindCSS
ECharts
```

---

## 8.3 桌面端

```text
Tauri
```

---

## 8.4 报告格式

```text
JSON
HTML
Markdown
SARIF
PDF，可选
```

---

## 8.5 AI / MCP

```text
Python MCP SDK 或 TypeScript MCP SDK
本地 MCP Server
stdio transport 优先
后期支持 HTTP transport
```

---

## 9. 规则系统设计

## 9.1 规则设计原则

规则最好用 YAML 写，方便开源社区贡献。

**规则系统的三层架构（已在 4.8 节详细说明）：**

```text
规则定义层（YAML 文件，纯数据） → 规则解析层（RuleParser） → 规则执行层（RuleEngine）
```

分层的好处是规则格式和匹配逻辑互不耦合。更换规则格式（如将来支持 JSON/TOML）只需改解析层，优化匹配算法不影响规则定义。

每条规则建议包含：

```text
id              规则唯一标识（如 FABRIC_COUCHDB_EXPOSED）
name            规则名称
category        分类（Fabric Configuration / RPC 等）
severity        风险等级（CRITICAL / HIGH / MEDIUM / LOW / INFO）
target          扫描对象类型描述
match           匹配逻辑（pattern / key-value / regex / multi-file 等）
description     风险描述
remediation     修复建议
references      参考链接列表
false_positive  误报说明（什么情况下可能是误报）
```

---

## 9.2 示例规则：CouchDB 暴露

```yaml
id: FABRIC_COUCHDB_EXPOSED
name: CouchDB 服务暴露
category: Fabric Configuration
severity: HIGH
target:
  type: docker_compose
match:
  file: docker-compose.yaml
  pattern: "5984:5984"
description: >
  CouchDB 端口被映射到宿主机，可能导致状态数据库被未授权访问。
remediation: >
  建议删除外部端口映射，仅允许 Peer 容器通过内部 Docker 网络访问 CouchDB。
references:
  - https://hyperledger-fabric.readthedocs.io/
```

---

## 9.3 示例规则：TLS 未开启

```yaml
id: FABRIC_PEER_TLS_DISABLED
name: Peer 节点未开启 TLS
category: Fabric Configuration
severity: HIGH
target:
  type: env_or_yaml
match:
  any:
    - pattern: "CORE_PEER_TLS_ENABLED=false"
    - key: "peer.tls.enabled"
      equals: false
description: >
  Peer 节点未开启 TLS，节点间通信可能被窃听或篡改。
remediation: >
  建议开启 TLS，并正确配置证书、私钥和根 CA 文件。
references:
  - https://hyperledger-fabric.readthedocs.io/en/latest/enable_tls.html
```

---

## 10. 项目目录结构建议

```text
blocksecscan/
│
├── blocksec/
│   ├── cli/
│   │   └── main.py
│   │
│   ├── api/
│   │   ├── __init__.py        # Public API 对外接口
│   │   └── server.py          # FastAPI Web 服务
│   │
│   ├── core/
│   │   ├── engine.py          # Core Engine 核心调度
│   │   ├── scanner_registry.py # Scanner 注册中心
│   │   ├── rule_engine.py     # 规则执行引擎
│   │   ├── rule_parser.py     # YAML 规则解析器
│   │   └── scheduler.py       # 扫描调度器
│   │
│   ├── models/                # Pydantic 数据模型（最底层，无内部依赖）
│   │   ├── __init__.py
│   │   ├── finding.py         # Finding 模型
│   │   ├── rule.py            # Rule 模型
│   │   ├── scan.py            # ScanTarget, ScanResult 模型
│   │   └── report.py          # Report 模型
│   │
│   ├── scanners/              # 各扫描器插件
│   │   ├── base.py            # Scanner 抽象基类
│   │   ├── fabric_config/
│   │   ├── fabric_runtime/
│   │   ├── fabric_chaincode/
│   │   ├── smart_contract/
│   │   ├── rpc/
│   │   └── web3/
│   │
│   ├── rules/                 # YAML 规则定义文件（纯数据层）
│   │   ├── fabric/
│   │   ├── rpc/
│   │   ├── contract/
│   │   └── web3/
│   │
│   ├── reports/
│   │   ├── templates/         # Jinja2 模板
│   │   └── exporters/         # JsonExporter, HtmlExporter, ...
│   │
│   ├── config/
│   │   └── settings.py        # Pydantic Settings 统一配置
│   │
│   └── mcp/
│       └── server.py
│
├── web/
│   ├── src/
│   └── package.json
│
├── labs/
│   ├── fabric-safe/
│   ├── fabric-vuln-tls-disabled/
│   ├── fabric-vuln-couchdb-exposed/
│   ├── fabric-vuln-weak-password/
│   ├── solidity-vuln/
│   └── web3-vuln-demo/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/
│   ├── usage.md
│   ├── rules.md
│   ├── mcp.md
│   └── labs.md
│
├── pyproject.toml
├── README.md
├── LICENSE
└── docker-compose.yml
```

---

## 11. 测试方案

## 11.1 本地靶场设计

建议维护 `labs/` 目录，每个靶场都是一个独立的、**可以直接用 `docker-compose up` 启动的最小化环境**。

同时，为每个靶场配套一个 `expected_findings.json`，描述该靶场**应该扫出哪些漏洞**，用于自动化验证。

```text
labs/
├── fabric-safe/                    # 安全配置（应无高危漏洞）
│   ├── docker-compose.yaml
│   └── expected_findings.json      # {"expected_critical": 0, "expected_high": 0}
│
├── fabric-vuln-tls-disabled/       # TLS 关闭（应检测 FABRIC_PEER_TLS_DISABLED）
│   ├── docker-compose.yaml
│   └── expected_findings.json      # {"expected_high": 1, "rule_ids": ["FABRIC_PEER_TLS_DISABLED"]}
│
├── fabric-vuln-couchdb-exposed/
│   ├── docker-compose.yaml
│   └── expected_findings.json
│
├── fabric-vuln-weak-password/
│   ├── docker-compose.yaml
│   └── expected_findings.json
│
├── fabric-vuln-private-key-leak/
│   ├── docker-compose.yaml
│   └── expected_findings.json
│
├── fabric-vuln-debug-log/
│   ├── docker-compose.yaml
│   └── expected_findings.json
│
├── ethereum-rpc-exposed/
├── solidity-vuln-contracts/
└── web3-vuln-demo/
```

---

## 11.2 测试类型

```text
单元测试：测试每条规则能否正确匹配（纯逻辑，不需要真实 Fabric 环境）
集成测试：测试完整扫描流程（启动一个扫描器 → 加载规则 → 扫描 → 验证 Finding）
端到端测试：启动 docker-compose 靶场 → 真实扫描 → 对比实际结果和 expected_findings.json
回归测试：确保修改代码后旧规则不失效（CI 中自动运行全部靶场）
```

自动化验证流程：

```text
1. 启动靶场：docker-compose up -d
2. 运行扫描：blocksec scan fabric --path ./labs/fabric-vuln-tls-disabled --output result.json
3. 读取 expected_findings.json
4. 对比：实际 Finding 数量和 rule_id 是否与预期一致
5. 清理：docker-compose down
6. 通过 / 失败
```

---

## 11.3 毕业论文实验设计

| 实验编号 | 场景 | 预期结果 |
|---|---|---|
| Case 1 | 正常 Fabric 配置 | 无高危漏洞 |
| Case 2 | TLS 关闭 | 检测高危 |
| Case 3 | CouchDB 暴露 | 检测高危 |
| Case 4 | 明文密码 | 检测中高危 |
| Case 5 | 私钥泄露 | 检测高危 |
| Case 6 | 背书策略过弱 | 检测中危 |
| Case 7 | RPC 暴露 | 检测高危 |
| Case 8 | Solidity 重入漏洞 | 检测高危 |

---

## 11.4 真实测试方式

不建议直接扫描公网未知目标。

推荐三种方式：

### 方式一：自建真实运行环境

在本机、虚拟机、学校服务器或云服务器上部署 Fabric 测试网络。

### 方式二：扫描开源项目配置

对 GitHub 上公开的 Fabric 示例项目做离线配置扫描。

### 方式三：授权环境测试

如果学校实验室或企业提供授权环境，可以做在线扫描。

需要明确：

```text
扫描范围
目标 IP
测试时间
允许的检测方式
是否允许端口扫描
是否允许登录服务器
```

---

## 12. 开发路线图

## v0.1：毕业设计最小可用版（范围收紧）

目标：能交论文，能演示，快速跑通闭环。

> ⚠️ 不要一开始就追求完美的完整规则库。先选 3-5 条最典型的规则跑通全流程，论文就有东西写了。

```text
Fabric 配置扫描（3-5 条核心规则即可）：
  - TLS 未开启检测
  - CouchDB 端口暴露检测
  - 明文密码检测
  - 私钥文件泄露检测
  - 调试日志检测（可选）
YAML 规则库（只建 fabric/ 分类）
CLI 单命令：blocksec scan fabric --path ./xxx
JSON 报告输出
2 个本地 labs 靶场（一个安全配置 + 一个漏洞配置）
基本单元测试
```

---

## v0.2：Fabric 增强版

```text
Fabric 运行时扫描
Docker 容器检测
端口检测
CouchDB 暴露检测
证书有效期检测
```

---

## v0.3：报告和工程化

```text
Markdown 报告
SARIF 报告
GitHub Action
规则文档
测试覆盖率
```

---

## v0.4：Web GUI

```text
任务管理
扫描历史
风险看板
报告查看
规则管理
```

---

## v0.5：智能合约扫描

```text
集成 Slither
解析 Slither JSON
映射 OWASP 分类
生成合约安全报告
```

---

## v0.6：Web3 / RPC 扫描

```text
Web3 前端源码扫描
RPC 节点安全检测
钱包交互风险检测
```

---

## v1.0：正式开源版

```text
完整 README
完整文档
Docker 镜像
GitHub Action
示例靶场
贡献指南
License
Release
```

---

## v1.1：AI + MCP 版本

```text
MCP Server
AI 读取扫描结果
AI 解释漏洞
AI 生成修复建议
AI 生成报告总结
AI 辅助规则编写
```

---

## 13. 毕业论文大纲

```text
第 1 章 绪论
  1.1 研究背景
  1.2 区块链系统安全问题
  1.3 传统漏洞扫描与区块链安全扫描的区别
  1.4 本文主要工作

第 2 章 相关技术
  2.1 Hyperledger Fabric 基础
  2.2 Fabric 节点、链码、账本和 MSP
  2.3 安全基线扫描技术
  2.4 规则引擎技术
  2.5 漏洞报告与风险评级

第 3 章 需求分析
  3.1 功能需求
  3.2 非功能需求
  3.3 安全边界
  3.4 系统使用场景

第 4 章 系统设计
  4.1 总体架构
  4.2 扫描引擎设计
  4.3 规则库设计
  4.4 报告模块设计
  4.5 CLI / GUI 接口设计

第 5 章 系统实现
  5.1 Fabric 配置解析
  5.2 安全规则匹配
  5.3 风险评级实现
  5.4 报告生成实现
  5.5 实验靶场实现

第 6 章 实验与分析
  6.1 实验环境
  6.2 测试用例设计
  6.3 扫描结果分析
  6.4 准确性分析
  6.5 局限性分析

第 7 章 总结与展望
  7.1 本文工作总结
  7.2 不足之处
  7.3 后续扩展：智能合约、Web3、MCP、AI
```

---

## 14. GitHub 开源建议

## 14.1 README 内容

README 建议包含：

```text
项目简介
功能特性
安装方式
快速开始
扫描示例
报告截图
规则编写说明
MCP 使用说明
安全声明
贡献指南
路线图
```

---

## 14.2 安全声明（应落实到代码层面）

安全声明不能只写在 README 里，建议在以下几个层面落实：

**1. README 顶部显眼位置：**

```text
⚠️ 安全声明
本项目仅用于授权安全测试、教学实验和自有资产安全检查。
请勿对未授权目标进行扫描。
使用者应自行承担因不当使用产生的法律责任。
```

**2. CLI 帮助信息中展示：**

```bash
$ blocksec --help
BlockSecScan - 区块链安全扫描平台

⚠️ 仅用于授权安全测试和教学实验。

Commands:
  scan    运行安全扫描
  report  生成扫描报告
  rules   管理规则库
```

**3. 扫描远程目标时运行时警告：**

```text
当用户执行 blocksec scan rpc --target <非本地地址> 时，
在终端打印确认提示：
"⚠️ 你正在扫描一个非本地目标。请确认你已获得授权 (y/N)："
```

**4. 安全边界说明文档：**

在 `docs/security.md` 中说明：
- 工具的使用边界
- 哪些操作属于授权行为
- 哪些操作属于未授权行为
- 法律责任声明

---

## 14.3 License 建议

可选：

```text
Apache-2.0
MIT
```

更建议：

```text
Apache-2.0
```

原因：适合工具类开源项目，也更适合后续企业使用。

---

## 15. 可复制给其他 AI 的对话蒸馏

下面内容可以直接复制给其他 AI，用于让它快速理解项目背景。

```text
我是一名大学生，专业是区块链工程，但我的主要学习方向是网络安全。
对于区块链，我只了解基础概念，缺少实际动手经验。
学校要求毕业设计必须和区块链专业相关，所以我希望做一个和漏洞扫描相关，同时又能体现区块链特色的项目。

我最开始想做漏洞扫描系统，但传统 Web 漏洞扫描和区块链相关度不够，因此希望研究对象变成区块链节点、Hyperledger Fabric 联盟链节点、Fabric 链码、智能合约、Web3 应用或区块链 RPC 服务。

经过讨论，我了解到：
1. Fabric 不是网页，而是一套企业联盟链后台基础设施。
2. Fabric 应用通常由 Web 前端、后端服务、Fabric SDK、Peer 节点、Orderer 节点、链码和账本组成。
3. Fabric 适合做安全配置扫描，例如 TLS、CouchDB、Docker 配置、证书、MSP、端口暴露、背书策略等。
4. 毕业设计可以聚焦于“面向 Hyperledger Fabric 联盟链系统的安全基线扫描平台设计与实现”。
5. 开源项目可以扩展为更大的“区块链安全扫描平台”。

我希望这个项目不仅能完成毕业设计，还能真正有用，并计划开源到 GitHub。项目最好支持：
- CLI 命令行；
- Web GUI；
- 后期桌面 GUI；
- GitHub Action；
- AI 功能；
- MCP 接入。

我的目标不是只做一个简单脚本，而是做一个可扩展的平台：
- 核心扫描引擎独立；
- CLI、GUI、MCP、GitHub Action 都调用同一套扫描引擎；
- 规则库可扩展；
- 报告格式支持 JSON、HTML、Markdown、SARIF；
- AI 不直接替代扫描器，而是基于扫描结果进行漏洞解释、修复建议、风险总结、误报分析。

项目主要模块规划：
1. Fabric 配置安全扫描；
2. Fabric 运行时扫描；
3. Fabric 链码安全扫描；
4. 智能合约扫描，集成 Slither 等工具；
5. 区块链 RPC 节点扫描；
6. Web3 前端应用扫描；
7. 多平台入口，包含 CLI、Web GUI、桌面 GUI、GitHub Action；
8. MCP Server，让 AI 客户端可以调用扫描能力；
9. AI 安全助手，用于解释漏洞、生成修复建议和总结报告。

请基于以上背景，帮助我进一步细化具体模块设计、技术选型、代码结构、规则设计、实验方案、论文结构或开发计划。
```

---

## 16. 当前最推荐执行路线

最稳妥路线：

```text
第一步：Fabric 配置扫描
第二步：CLI + JSON / HTML 报告
第三步：本地 Fabric 靶场
第四步：规则库完善
第五步：Web GUI
第六步：GitHub Action
第七步：智能合约 / RPC / Web3 扩展
第八步：MCP + AI
```

不要一开始同时做完所有模块。

毕业设计阶段应重点保证：

```text
能扫描
能报告
能复现实验
能解释风险
能体现区块链专业相关性
```

开源长期阶段再逐步扩展：

```text
多平台
插件化
智能合约
Web3
MCP
AI
```

---

## 17. 开发规范与流程

### 17.1 Git 提交规范

**Commit 粒度要小，一个逻辑变更一个 commit：**

```text
✅ 好的 commit：
  feat: 添加 FABRIC_PEER_TLS_DISABLED 规则
  fix: 修复 CouchDB 端口检测正则匹配范围过宽
  test: 添加 TLS 规则单元测试
  docs: 更新规则编写说明

❌ 不好的 commit：
  feat: 完成所有规则
  fix: 修了一些 bug
```

**建议使用 Conventional Commits 格式：**

```text
feat:     新功能
fix:      Bug 修复
refactor: 重构（不改变功能）
test:     测试相关
docs:     文档更新
chore:    构建/工具链相关
```

### 17.2 分支策略

对于个人毕业设计项目，不需要复杂的 Git Flow，用简化模式即可：

```text
main        始终保持可运行状态，每个版本打 tag
  │
  ├── develop    日常开发分支，功能完成后合并到 main
  │     │
  │     ├── feat/tls-scan      功能分支（做完合并回 develop）
  │     ├── feat/couchdb-scan
  │     └── fix/rule-parser
  │
  └── thesis     论文实验专用分支，锁定版本用于复现
```

### 17.3 CHANGELOG 从第一天开始写

论文写「系统实现」章节时会非常有用，因为你可以回溯每个功能是什么时候加的、为什么加。

```markdown
# Changelog

## [0.1.0] - 2026-xx-xx
### Added
- 项目初始化，pyproject.toml 配置
- CLI 框架搭建（Typer）
- Public API 层 base 定义
- Models 层：ScanTarget, Finding, ScanResult
- RuleParser：YAML 规则解析
- RuleEngine：文本匹配引擎
- FabricConfigScanner：文件扫描器
- 规则：FABRIC_PEER_TLS_DISABLED
- 规则：FABRIC_COUCHDB_EXPOSED
- 规则：FABRIC_WEAK_PASSWORD
- 规则：FABRIC_PRIVATE_KEY_LEAK
- JsonExporter：JSON 报告输出
- labs/fabric-safe 靶场
- labs/fabric-vuln-tls-disabled 靶场
- 单元测试
```

### 17.4 开发节奏建议

```text
每天工作流程：
1. 从 develop 分支切出功能分支
2. 完成一个小功能 / 一条规则 / 一个测试
3. commit
4. 合并回 develop（自己 review 一下 diff）
5. 删除功能分支

每周节奏：
- 周一到周五：推进功能
- 周五：整理 CHANGELOG，确保所有测试通过
- 周末：可选，写文档或整理论文素材
```

### 17.5 代码质量标准

在 `pyproject.toml` 中配置自动化检查，养成提交前运行的习惯：

```bash
# 格式化代码
ruff format .

# 检查代码质量
ruff check .

# 类型检查（可选，建议 v0.2 开始）
mypy blocksec/

# 运行测试
pytest
```

> 提示：可以把这些命令配置为 pre-commit hook，但毕业设计阶段手动运行即可，不要过度工程化。

---

## 18. 参考资料

- Hyperledger Fabric Test Network  
  https://hyperledger-fabric.readthedocs.io/en/latest/test_network.html

- Hyperledger Fabric TLS  
  https://hyperledger-fabric.readthedocs.io/en/latest/enable_tls.html

- Hyperledger Fabric Peer Checklist  
  https://hyperledger-fabric.readthedocs.io/en/release-2.5/deploypeer/peerchecklist.html

- Geth Security  
  https://geth.ethereum.org/docs/fundamentals/security

- Slither  
  https://github.com/crytic/slither

- OWASP Smart Contract Top 10  
  https://owasp.org/www-project-smart-contract-top-10/

- MCP 官方文档  
  https://modelcontextprotocol.io/docs/learn/architecture

---

## 19. 一句话总结

> 先用 Fabric 配置安全扫描完成毕业设计闭环，再逐步扩展为支持 CLI、GUI、GitHub Action、MCP 和 AI 的区块链安全扫描平台。


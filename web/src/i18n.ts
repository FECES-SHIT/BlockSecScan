import { ref } from "vue";

type Lang = "zh" | "en";

const saved = (localStorage.getItem("blocksec-lang") || "zh") as Lang;
const currentLang = ref<Lang>(saved);

const messages: Record<Lang, Record<string, string>> = {
  en: {
    "app.title": "BlockSecScan",
    "app.dashboard": "Dashboard",
    "app.newScan": "New Scan",
    "app.history": "History",
    "app.rules": "Rules",
    "app.lang": "中文",

    "dashboard.hero": "Security Scanner for Hyperledger Fabric",
    "dashboard.totalScans": "Total Scans",
    "dashboard.highRisks": "High + Critical",
    "dashboard.totalFindings": "Total Findings",
    "dashboard.lastScan": "Last Scan",
    "dashboard.quickScan": "Start New Scan",
    "dashboard.recentScans": "Recent Scans",
    "dashboard.empty": "No scans yet. Start your first scan!",
    "dashboard.emptyIcon": "🔍",

    "scan.title": "New Scan",
    "scan.type": "Scan Type",
    "scan.typeConfig": "Fabric Config (static files)",
    "scan.typeRuntime": "Fabric Runtime (Docker)",
    "scan.path": "Target Path",
    "scan.pathHint": "Config: project directory | Runtime: \"local\" for Docker",
    "scan.start": "Start Scan",
    "scan.scanning": "Scanning...",
    "scan.error": "Scan failed. Check the path and try again.",

    "result.title": "Scan Result",
    "result.exportHtml": "HTML",
    "result.exportMd": "MD",
    "result.exportJson": "JSON",
    "result.exportSarif": "SARIF",
    "result.delete": "Delete",
    "result.filterAll": "All",
    "result.filterCritical": "Critical",
    "result.filterHigh": "High",
    "result.filterMedium": "Medium",
    "result.filterLow": "Low",
    "result.empty": "No security issues found.",
    "result.emptyFilter": "No findings matching filter.",
    "result.confirmDelete": "Delete this scan?",
    "result.noFindings": "No security issues found.",

    "history.title": "Scan History",
    "history.empty": "No scan history yet.",
    "history.emptyIcon": "📋",
    "history.time": "Time",
    "history.type": "Type",
    "history.target": "Target",
    "history.findings": "Findings",
    "history.duration": "Duration",
    "history.actions": "Actions",
    "history.view": "View",
    "history.confirmDelete": "Delete this scan?",

    "rules.title": "Rules",
    "rules.filterAll": "All",
    "rules.empty": "No rules loaded.",
    "rules.id": "Rule ID",
    "rules.name": "Name",
    "rules.severity": "Severity",
    "rules.category": "Category",
    "rules.description": "Description",

    "finding.evidence": "Evidence",
    "finding.remediation": "Fix",
    "finding.references": "References",
    "finding.confidence": "Confidence",

    "severity.critical": "CRITICAL",
    "severity.high": "HIGH",
    "severity.medium": "MEDIUM",
    "severity.low": "LOW",
    "severity.info": "INFO",

    "common.loading": "Loading...",
    "common.error": "An error occurred.",
    "common.confirm": "Confirm",
    "common.cancel": "Cancel",
    "common.save": "Save",
  },
  zh: {
    "app.title": "BlockSecScan",
    "app.dashboard": "仪表盘",
    "app.newScan": "新建扫描",
    "app.history": "扫描历史",
    "app.rules": "规则库",
    "app.lang": "English",

    "dashboard.hero": "面向 Hyperledger Fabric 的安全扫描平台",
    "dashboard.totalScans": "累计扫描",
    "dashboard.highRisks": "高危 + 严重",
    "dashboard.totalFindings": "发现问题",
    "dashboard.lastScan": "最近扫描",
    "dashboard.quickScan": "开始新扫描",
    "dashboard.recentScans": "最近扫描记录",
    "dashboard.empty": "暂无扫描记录，开始你的第一次扫描吧！",
    "dashboard.emptyIcon": "🔍",

    "scan.title": "新建扫描",
    "scan.type": "扫描类型",
    "scan.typeConfig": "Fabric 配置扫描（静态文件）",
    "scan.typeRuntime": "Fabric 运行时扫描（Docker 容器）",
    "scan.path": "目标路径",
    "scan.pathHint": "配置扫描：项目目录路径 | 运行时：输入 \"local\" 扫描本机 Docker",
    "scan.start": "开始扫描",
    "scan.scanning": "扫描中...",
    "scan.error": "扫描失败，请检查路径后重试。",

    "result.title": "扫描结果",
    "result.exportHtml": "HTML",
    "result.exportMd": "MD",
    "result.exportJson": "JSON",
    "result.exportSarif": "SARIF",
    "result.delete": "删除",
    "result.filterAll": "全部",
    "result.filterCritical": "严重",
    "result.filterHigh": "高危",
    "result.filterMedium": "中危",
    "result.filterLow": "低危",
    "result.empty": "未发现安全问题。",
    "result.emptyFilter": "当前筛选条件下无结果。",
    "result.confirmDelete": "确认删除此扫描结果？",
    "result.noFindings": "未发现安全问题。",

    "history.title": "扫描历史",
    "history.empty": "暂无扫描历史。",
    "history.emptyIcon": "📋",
    "history.time": "时间",
    "history.type": "类型",
    "history.target": "目标",
    "history.findings": "问题数",
    "history.duration": "耗时",
    "history.actions": "操作",
    "history.view": "查看",
    "history.confirmDelete": "确认删除此条扫描记录？",

    "rules.title": "规则库",
    "rules.filterAll": "全部",
    "rules.empty": "未加载到规则。",
    "rules.id": "规则ID",
    "rules.name": "名称",
    "rules.severity": "严重度",
    "rules.category": "分类",
    "rules.description": "描述",

    "finding.evidence": "证据",
    "finding.remediation": "修复建议",
    "finding.references": "参考资料",
    "finding.confidence": "置信度",

    "severity.critical": "严重",
    "severity.high": "高危",
    "severity.medium": "中危",
    "severity.low": "低危",
    "severity.info": "信息",

    "common.loading": "加载中...",
    "common.error": "发生错误。",
    "common.confirm": "确认",
    "common.cancel": "取消",
    "common.save": "保存",
  },
};

export function t(key: string): string {
  return messages[currentLang.value][key] || key;
}

export function setLang(lang: Lang) {
  currentLang.value = lang;
  localStorage.setItem("blocksec-lang", lang);
}

export { currentLang };

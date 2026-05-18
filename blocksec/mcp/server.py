"""BlockSecScan MCP Server — expose scanning tools to AI assistants via MCP protocol."""

import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

from blocksec.api.public import list_rules, scan
from blocksec.models.scan import ScanTarget

server = Server("blocksecscan")
_SCAN_CACHE: dict[str, dict] = {}


def _format_finding(f: dict) -> str:
    parts = [
        f"[{f.get('severity', '?')}] {f.get('title', '')}",
        f"Rule: {f.get('rule_id', '')}",
        f"File: {f.get('file_path', '')}",
        f"Evidence: {f.get('evidence', '')}",
    ]
    if f.get("description"):
        parts.append(f"Description: {f['description']}")
    if f.get("remediation"):
        parts.append(f"Remediation: {f['remediation']}")
    return "\n".join(parts)


def _summarize(result) -> str:
    s = result.summary
    lines = [
        f"Scan Complete — {s.total} findings",
        f"CRITICAL:{s.critical} HIGH:{s.high} MEDIUM:{s.medium} LOW:{s.low} INFO:{s.info}",
        f"Target: {result.target.path}  Duration: {result.duration_seconds:.1f}s",
        "",
    ]
    for f in sorted(result.findings, key=lambda x: x.severity.value, reverse=True):
        fdict = f.model_dump(mode="json")
        lines.append(_format_finding(fdict))
        lines.append("---")
    return "\n".join(lines)


def _str_prop(desc: str) -> dict:
    return {"type": "string", "description": desc}


def _bool_prop(desc: str) -> dict:
    return {"type": "boolean", "description": desc, "default": True}


@server.list_tools()
async def list_tools() -> list[Tool]:  # noqa: E501 — MCP tool schemas are inherently verbose
    return [
        Tool(name="scan_fabric_config", description="Scan Fabric config files.",
             inputSchema={"type": "object",
                          "properties": {"path": _str_prop("Project path")},
                          "required": ["path"]}),
        Tool(name="scan_fabric_runtime", description="Scan running Docker containers.",
             inputSchema={"type": "object",
                          "properties": {"local": _bool_prop("Scan local")},
                          "required": []}),
        Tool(name="scan_contract", description="Scan Solidity contracts with Slither.",
             inputSchema={"type": "object",
                          "properties": {"path": _str_prop("Project path")},
                          "required": ["path"]}),
        Tool(name="scan_rpc", description="Scan Ethereum RPC endpoint security.",
             inputSchema={"type": "object",
                          "properties": {"target": _str_prop("RPC URL")},
                          "required": ["target"]}),
        Tool(name="scan_web3", description="Scan Web3 frontend for vulnerabilities.",
             inputSchema={"type": "object",
                          "properties": {"path": _str_prop("Frontend path")},
                          "required": ["path"]}),
        Tool(name="list_rules", description="List all security rules.",
             inputSchema={"type": "object",
                          "properties": {"category": _str_prop("Category filter")},
                          "required": []}),
        Tool(name="explain_finding", description="Explain a security finding.",
             inputSchema={"type": "object",
                          "properties": {"rule_id": _str_prop("Rule ID")},
                          "required": ["rule_id"]}),
        Tool(name="get_scan_result", description="Get cached scan result.",
             inputSchema={"type": "object",
                          "properties": {"scan_id": _str_prop("Scan ID")},
                          "required": ["scan_id"]}),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    result_text = ""

    if name == "scan_fabric_config":
        target = ScanTarget(target_type="fabric_config", path=arguments["path"])
        result = scan(target)
        _SCAN_CACHE[result.scan_id] = result.model_dump(mode="json")
        result_text = _summarize(result)

    elif name == "scan_fabric_runtime":
        local = arguments.get("local", True)
        target = ScanTarget(target_type="fabric_runtime", path="local", options={"local": local})
        result = scan(target)
        _SCAN_CACHE[result.scan_id] = result.model_dump(mode="json")
        result_text = _summarize(result)

    elif name == "scan_contract":
        target = ScanTarget(target_type="contract", path=arguments["path"])
        result = scan(target)
        _SCAN_CACHE[result.scan_id] = result.model_dump(mode="json")
        result_text = _summarize(result)

    elif name == "scan_rpc":
        target_url = arguments["target"]
        host = target_url.split("://")[-1].split(":")[0] if "://" in target_url else target_url.split(":")[0]
        target = ScanTarget(target_type="rpc", path=target_url, options={"host": host})
        result = scan(target)
        _SCAN_CACHE[result.scan_id] = result.model_dump(mode="json")
        result_text = _summarize(result)

    elif name == "scan_web3":
        target = ScanTarget(target_type="web3", path=arguments["path"])
        result = scan(target)
        _SCAN_CACHE[result.scan_id] = result.model_dump(mode="json")
        result_text = _summarize(result)

    elif name == "list_rules":
        rules = list_rules(category=arguments.get("category"))
        lines = [f"Rules ({len(rules)} total):", ""]
        for r in rules:
            lines.append(f"[{r.severity}] {r.id} — {r.name}")
            if r.description:
                lines.append(f"  {r.description[:120]}")
            lines.append("")
        result_text = "\n".join(lines)

    elif name == "explain_finding":
        rule_id = arguments["rule_id"]
        rules = list_rules()
        matched = next((r for r in rules if r.id == rule_id), None)
        if matched:
            result_text = f"""Rule: {matched.id} — {matched.name}
Severity: {matched.severity}
Confidence: {matched.confidence}

Description:
{matched.description}

Remediation:
{matched.remediation}

References:
{chr(10).join(matched.references) if matched.references else 'N/A'}

False Positive Note:
{matched.false_positive_note or 'N/A'}
"""
        else:
            result_text = f"Rule '{rule_id}' not found in rule database."

    elif name == "get_scan_result":
        scan_id = arguments["scan_id"]
        cached = _SCAN_CACHE.get(scan_id)
        if cached:
            summary_json = json.dumps(cached["summary"], indent=2)
            result_text = f"Scan {scan_id}:\n{summary_json}\n{len(cached['findings'])} findings"
        else:
            result_text = f"Scan '{scan_id}' not found. Run a scan first to cache results."

    return [TextContent(type="text", text=result_text)]


@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = [
        Resource(uri="blocksec://rules", name="Security Rules",
                 description="All loaded security rules", mimeType="application/json"),
    ]
    for scan_id in _SCAN_CACHE:
        resources.append(Resource(
            uri=f"blocksec://scans/{scan_id}", name=f"Scan {scan_id[:8]}",
            description="Scan result", mimeType="application/json",
        ))
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "blocksec://rules":
        rules = list_rules()
        return json.dumps([r.model_dump(mode="json") for r in rules], indent=2, ensure_ascii=False)
    if uri.startswith("blocksec://scans/"):
        scan_id = uri.split("/")[-1]
        cached = _SCAN_CACHE.get(scan_id)
        if cached:
            return json.dumps(cached, indent=2, ensure_ascii=False)
        return f"Scan '{scan_id}' not found."
    return f"Unknown resource: {uri}"


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def run():
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    run()

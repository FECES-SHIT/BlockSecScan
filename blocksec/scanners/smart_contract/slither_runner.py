"""Slither subprocess runner and output parser."""

import json
import os
import subprocess

from blocksec.models.finding import Category, Finding, Severity
from blocksec.scanners.smart_contract.owasp_map import map_detector_to_owasp

SLITHER_SEVERITY_MAP = {
    "High": Severity.HIGH,
    "Medium": Severity.MEDIUM,
    "Low": Severity.LOW,
    "Informational": Severity.INFO,
    "Optimization": Severity.INFO,
}


def run_slither(project_path: str) -> list[Finding]:
    if not os.path.isdir(project_path):
        return []

    contracts_dir = os.path.join(project_path, "contracts")
    scan_dir = contracts_dir if os.path.isdir(contracts_dir) else project_path

    try:
        result = subprocess.run(
            ["slither", ".", "--json", "-"],
            cwd=scan_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        return []
    except subprocess.TimeoutExpired:
        return []

    if result.returncode != 0 and not result.stdout.strip():
        return []

    return parse_slither_output(result.stdout, scan_dir)


def parse_slither_output(stdout: str, scan_dir: str) -> list[Finding]:
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return []

    detectors = data.get("results", {}).get("detectors", [])
    if not detectors:
        return []

    findings: list[Finding] = []
    for d in detectors:
        check = d.get("check", "unknown")
        owasp = map_detector_to_owasp(check)

        elements = d.get("elements", [])
        for elem in elements:
            loc = _extract_location(elem, scan_dir)
            finding = Finding(
                rule_id=f"SLITHER_{check.upper().replace('-', '_')}",
                severity=_map_severity(d.get("impact", "Medium")),
                category=Category.CONTRACT,
                title=f"[{owasp['swc']}] {d.get('description', check)}",
                description=_format_description(d, owasp),
                file_path=loc["file"],
                line_start=loc["line"],
                evidence=_extract_evidence(elem),
                remediation=d.get("recommendation", d.get("first_markdown_element", "")),
                references=[owasp["url"]] if owasp["url"] else [],
                confidence=_map_confidence(d.get("confidence", "Medium")),
            )
            findings.append(finding)

    return findings


def _extract_location(elem: dict, scan_dir: str) -> dict:
    sm = elem.get("source_mapping", {})
    filename = sm.get("filename_relative", sm.get("filename_absolute", ""))
    if not filename:
        filename = "contract.sol"
    filepath = os.path.join(scan_dir, filename)
    return {
        "file": filepath,
        "line": sm.get("lines", [1])[0] if sm.get("lines") else 1,
    }


def _extract_evidence(elem: dict) -> str:
    extra = elem.get("additional_fields", {})
    sig = extra.get("signature", "")
    expr = extra.get("expression", "")
    if sig and expr:
        return f"{sig}: {expr}"
    if sig:
        return sig
    return str(extra)[:200]


def _format_description(detector: dict, owasp: dict) -> str:
    desc = detector.get("description", "")
    impact = detector.get("impact", "")
    confidence = detector.get("confidence", "")
    parts = [desc]
    if owasp["swc"] != "N/A":
        parts.append(f"Classification: {owasp['swc']} — {owasp['title']}")
    parts.append(f"Impact: {impact} | Confidence: {confidence}")
    return "\n".join(parts)


def _map_severity(impact: str) -> Severity:
    return SLITHER_SEVERITY_MAP.get(impact, Severity.MEDIUM)


def _map_confidence(conf: str) -> float:
    conf_map = {"High": 0.9, "Medium": 0.7, "Low": 0.5}
    return conf_map.get(conf, 0.5)

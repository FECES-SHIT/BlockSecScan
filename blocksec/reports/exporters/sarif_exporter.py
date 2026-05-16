"""SARIF 2.1.0 exporter for GitHub Code Scanning integration."""


from blocksec.models.scan import ScanResult

_SEVERITY_TO_LEVEL = {
    "CRITICAL": "error",
    "HIGH": "error",
    "MEDIUM": "warning",
    "LOW": "note",
    "INFO": "note",
}


class SarifExporter:
    @staticmethod
    def export(result: ScanResult) -> str:
        import json

        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "BlockSecScan",
                            "informationUri": "https://github.com/Aaa-Tongl/BlockSecScan",
                            "version": "0.2.0",
                            "rules": SarifExporter._build_rules(result),
                        }
                    },
                    "results": SarifExporter._build_results(result),
                    "invocations": [
                        {
                            "startTimeUtc": result.timestamp.isoformat(),
                            "executionSuccessful": True,
                        }
                    ],
                }
            ],
        }

        return json.dumps(sarif, indent=2, ensure_ascii=False)

    @staticmethod
    def _build_rules(result: ScanResult) -> list[dict]:
        seen: set[str] = set()
        rules: list[dict] = []
        for f in result.findings:
            if f.rule_id not in seen:
                seen.add(f.rule_id)
                rules.append({
                    "id": f.rule_id,
                    "name": f.title,
                    "shortDescription": {"text": f.description[:200]},
                    "fullDescription": {"text": f.description},
                    "helpUri": f.references[0] if f.references else "",
                })
        return rules

    @staticmethod
    def _build_results(result: ScanResult) -> list[dict]:
        results: list[dict] = []
        for f in result.findings:
            location = {
                "physicalLocation": {
                    "artifactLocation": {"uri": f.file_path},
                    "region": {},
                }
            }
            if f.line_start:
                location["physicalLocation"]["region"]["startLine"] = f.line_start
            if f.line_end:
                location["physicalLocation"]["region"]["endLine"] = f.line_end

            results.append({
                "ruleId": f.rule_id,
                "ruleIndex": 0,
                "level": _SEVERITY_TO_LEVEL.get(f.severity.value, "warning"),
                "message": {
                    "text": f"{f.title}\n\n{f.description}\n\nEvidence: {f.evidence}\n\nRemediation: {f.remediation}"
                },
                "locations": [location],
                "properties": {
                    "severity": f.severity.value,
                    "confidence": f"{f.confidence:.0%}",
                    "category": f.category.value,
                },
            })
        return results

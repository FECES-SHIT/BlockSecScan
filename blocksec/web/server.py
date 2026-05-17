import traceback

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from blocksec.api.public import generate_report, list_rules, scan
from blocksec.models.scan import ScanTarget
from blocksec.web.database import (
    create_scan,
    delete_scan,
    get_scan,
    init_db,
    list_scans,
    save_scan_error,
    save_scan_result,
)
from blocksec.web.models import ScanRequest, ScanResponse

app = FastAPI(title="BlockSecScan API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.3.0"}


@app.post("/api/scan", response_model=ScanResponse)
def api_scan(req: ScanRequest):
    target = ScanTarget(target_type=req.target_type, path=req.target_path)
    result = scan(target)
    _save(req.target_type, req.target_path, result)
    return ScanResponse(scan_id=result.scan_id, status="done")


@app.get("/api/scan/{scan_id}")
def api_get_scan(scan_id: str):
    data = get_scan(scan_id)
    if data is None:
        raise HTTPException(status_code=404, detail="scan not found")
    return data


@app.get("/api/scans")
def api_list_scans(limit: int = Query(default=50, le=200)):
    return list_scans(limit=limit)


@app.delete("/api/scan/{scan_id}")
def api_delete_scan(scan_id: str):
    if not delete_scan(scan_id):
        raise HTTPException(status_code=404, detail="scan not found")
    return {"ok": True}


@app.get("/api/rules")
def api_list_rules(category: str | None = Query(default=None)):
    rules = list_rules(category=category)
    return [
        {
            "id": r.id,
            "name": r.name,
            "severity": r.severity,
            "category": r.category,
            "description": r.description[:200],
        }
        for r in rules
    ]


@app.get("/api/scan/{scan_id}/report")
def api_get_report(scan_id: str, fmt: str = Query(default="html")):
    data = get_scan(scan_id)
    if data is None:
        raise HTTPException(status_code=404, detail="scan not found")

    from blocksec.models.finding import Category, Finding, Severity
    from blocksec.models.scan import ScanResult, ScanSummary, ScanTarget

    target = ScanTarget(target_type=data["target_type"], path=data["target_path"])
    findings = []
    for f in data["findings"]:
        findings.append(Finding(
            rule_id=f["rule_id"],
            severity=Severity[f["severity"]],
            category=Category[f["category"]],
            title=f["title"],
            description=f["description"],
            file_path=f["file_path"],
            line_start=f.get("line_start"),
            line_end=f.get("line_end"),
            evidence=f["evidence"],
            remediation=f.get("remediation", ""),
            references=f.get("references", []),
            confidence=f.get("confidence", 0.7),
        ))
    summary = ScanSummary(**data["summary"])
    result = ScanResult(
        scan_id=data["id"],
        target=target,
        findings=findings,
        summary=summary,
        duration_seconds=data["duration"],
    )

    report = generate_report(result, fmt=fmt)
    if fmt == "html":
        return HTMLResponse(content=report)
    elif fmt == "markdown":
        return PlainTextResponse(content=report, media_type="text/markdown")
    else:
        return PlainTextResponse(content=report, media_type="application/json")


def _save(target_type: str, target_path: str, result) -> None:
    try:
        import json
        create_scan(result.scan_id, target_type, target_path)
        findings_json = json.dumps([f.model_dump(mode="json") for f in result.findings])
        save_scan_result(
            result.scan_id,
            result.summary.model_dump_json(),
            findings_json,
            result.duration_seconds,
        )
    except Exception:
        save_scan_error(result.scan_id, traceback.format_exc())

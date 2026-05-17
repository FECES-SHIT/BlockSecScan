from pydantic import BaseModel


class ScanRequest(BaseModel):
    target_type: str  # fabric_config | fabric_runtime
    target_path: str
    output_format: str = "json"


class ScanResponse(BaseModel):
    scan_id: str
    status: str


class ScanDetail(BaseModel):
    id: str
    target_type: str
    target_path: str
    status: str
    summary: dict
    findings: list[dict]
    created_at: str
    duration: float


class ScanListItem(BaseModel):
    id: str
    target_type: str
    target_path: str
    status: str
    summary: dict
    created_at: str
    duration: float


class RuleItem(BaseModel):
    id: str
    name: str
    severity: str
    category: str
    description: str


class ErrorResponse(BaseModel):
    detail: str

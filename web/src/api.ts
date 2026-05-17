const BASE = "/api";

async function request(path: string, opts?: RequestInit) {
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "request failed");
  }
  return res;
}

export interface ScanListItem {
  id: string;
  target_type: string;
  target_path: string;
  status: string;
  summary: { critical: number; high: number; medium: number; low: number; info: number; total: number };
  created_at: string;
  duration: number;
}

export interface ScanDetail extends ScanListItem {
  findings: Finding[];
}

export interface Finding {
  id: string;
  rule_id: string;
  severity: string;
  category: string;
  title: string;
  description: string;
  file_path: string;
  line_start: number | null;
  evidence: string;
  remediation: string;
  references: string[];
  confidence: number;
}

export interface RuleItem {
  id: string;
  name: string;
  severity: string;
  category: string;
  description: string;
}

export async function startScan(target_type: string, target_path: string): Promise<{ scan_id: string }> {
  const res = await request("/scan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target_type, target_path }),
  });
  return res.json();
}

export async function getScan(id: string): Promise<ScanDetail> {
  const res = await request(`/scan/${id}`);
  return res.json();
}

export async function listScans(limit = 50): Promise<ScanListItem[]> {
  const res = await request(`/scans?limit=${limit}`);
  return res.json();
}

export async function deleteScan(id: string): Promise<void> {
  await request(`/scan/${id}`, { method: "DELETE" });
}

export async function getRules(category?: string): Promise<RuleItem[]> {
  const q = category ? `?category=${category}` : "";
  const res = await request(`/rules${q}`);
  return res.json();
}

export function reportUrl(scanId: string, fmt: string): string {
  return `${BASE}/scan/${scanId}/report?fmt=${fmt}`;
}

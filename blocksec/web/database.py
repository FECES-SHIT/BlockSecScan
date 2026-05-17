import json
import os
import sqlite3
from datetime import UTC, datetime

DB_PATH = os.environ.get("BLOCKSEC_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "data", "blocksec.db"))


_initialized = False


def _connect() -> sqlite3.Connection:
    global _initialized
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if not _initialized:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                target_type TEXT NOT NULL,
                target_path TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                summary_json TEXT DEFAULT '{}',
                findings_json TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                duration REAL DEFAULT 0
            )
        """)
        conn.commit()
        _initialized = True
    return conn


def init_db() -> None:
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT PRIMARY KEY,
            target_type TEXT NOT NULL,
            target_path TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            summary_json TEXT DEFAULT '{}',
            findings_json TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            duration REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def create_scan(scan_id: str, target_type: str, target_path: str) -> None:
    conn = _connect()
    now = datetime.now(UTC).isoformat()
    conn.execute(
        "INSERT INTO scans (id, target_type, target_path, status, created_at) VALUES (?, ?, ?, 'running', ?)",
        (scan_id, target_type, target_path, now),
    )
    conn.commit()
    conn.close()


def save_scan_result(scan_id: str, summary_json: str, findings_json: str, duration: float) -> None:
    conn = _connect()
    conn.execute(
        "UPDATE scans SET status='done', summary_json=?, findings_json=?, duration=? WHERE id=?",
        (summary_json, findings_json, duration, scan_id),
    )
    conn.commit()
    conn.close()


def save_scan_error(scan_id: str, error: str) -> None:
    conn = _connect()
    conn.execute("UPDATE scans SET status='error', summary_json=? WHERE id=?", (json.dumps({"error": error}), scan_id))
    conn.commit()
    conn.close()


def get_scan(scan_id: str) -> dict | None:
    conn = _connect()
    row = conn.execute("SELECT * FROM scans WHERE id=?", (scan_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_dict(row)


def list_scans(limit: int = 50) -> list[dict]:
    conn = _connect()
    rows = conn.execute("SELECT * FROM scans ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def delete_scan(scan_id: str) -> bool:
    conn = _connect()
    cur = conn.execute("DELETE FROM scans WHERE id=?", (scan_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "target_type": row["target_type"],
        "target_path": row["target_path"],
        "status": row["status"],
        "summary": json.loads(row["summary_json"]),
        "findings": json.loads(row["findings_json"]),
        "created_at": row["created_at"],
        "duration": row["duration"],
    }

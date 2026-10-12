from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).with_name("focusguard.db")
app = FastAPI(title="FOCUSGUARD API", description="Simple API for the FocusGuard prototype", version="1.0.0")

# Development setting: permits a local static frontend. Restrict origins before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                minutes INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                note TEXT
            )
        """)

init_db()

class SessionCreate(BaseModel):
    minutes: int = Field(ge=1, le=240)
    note: Optional[str] = Field(default=None, max_length=200)

@app.get("/")
def health():
    return {"name": "FOCUSGUARD API", "status": "ok", "docs": "/docs"}

@app.get("/sessions")
def list_sessions(limit: int = 20):
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    with connect() as con:
        rows = con.execute(
            "SELECT id, minutes, completed_at, note FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]

@app.post("/sessions", status_code=201)
def create_session(session: SessionCreate):
    completed_at = datetime.now(timezone.utc).isoformat()
    with connect() as con:
        cursor = con.execute(
            "INSERT INTO sessions (minutes, completed_at, note) VALUES (?, ?, ?)",
            (session.minutes, completed_at, session.note),
        )
        session_id = cursor.lastrowid
    return {"id": session_id, "minutes": session.minutes, "completed_at": completed_at, "note": session.note}

@app.get("/stats")
def stats():
    with connect() as con:
        row = con.execute(
            "SELECT COALESCE(SUM(minutes), 0) AS total_minutes, COUNT(*) AS session_count FROM sessions"
        ).fetchone()
    return dict(row)

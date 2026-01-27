from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sqlite3
from .detect import process_event
import time
import os

app = FastAPI()
DB = "events.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY, ts REAL, raw TEXT, processed JSON, anomaly INTEGER)''')
    conn.commit()
    conn.close()

class IngestModel(BaseModel):
    raw: str
    ts: float

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/ingest")
async def ingest(data: IngestModel, background_tasks: BackgroundTasks):
    # Guardar evento crudo
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (ts, raw, processed, anomaly) VALUES (?, ?, ?, ?)",
        (data.ts, data.raw, "", 0)
    )
    conn.commit()
    row_id = c.lastrowid
    conn.close()

    # Procesar en background (ML / detección)
    background_tasks.add_task(process_event, row_id, data.raw, data.ts)

    # Respuesta clara para Swagger / API clients
    return {
        "status": "ingested",
        "event_id": row_id,
        "raw_length": len(data.raw),
        "timestamp": data.ts
    }

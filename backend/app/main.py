from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, database, detect
from .database import engine
from .ws import manager
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
loop = None

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_running_loop()
    database.init_db()

@app.post("/ingest", response_model=models.Log)
async def ingest(data: models.IngestModel, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    log = crud.create_log(db=db, raw=data.raw, ts=data.ts)
    background_tasks.add_task(detect.process_event, log.id, data.raw, data.ts, loop)
    return log

@app.get("/logs", response_model=List[models.Log])
def get_logs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    logs = crud.get_logs(db, skip=skip, limit=limit)
    return logs

@app.get("/logs/count")
def get_logs_count(db: Session = Depends(database.get_db)):
    count = crud.get_logs_count(db)
    return {"count": count}

@app.get("/anomalies", response_model=List[models.Log])
def get_anomalies(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    anomalies = crud.get_anomalies(db, skip=skip, limit=limit)
    return anomalies

@app.get("/anomalies/count")
def get_anomalies_count(db: Session = Depends(database.get_db)):
    count = crud.get_anomalies_count(db)
    return {"count": count}

REPORTS_DIR = "reports"

@app.get("/reports")
def get_reports():
    if not os.path.exists(REPORTS_DIR):
        return []
    return os.listdir(REPORTS_DIR)

@app.get("/reports/{event_id}")
def get_report(event_id: int):
    report_path = os.path.join(REPORTS_DIR, f"report_{event_id}.txt")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(report_path)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
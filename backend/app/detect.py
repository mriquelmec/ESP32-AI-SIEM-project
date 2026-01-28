import json
import joblib
import numpy as np
import asyncio
from . import crud, database, report
from .preprocess import parse_raw_line, features_from_parsed
from .ws import manager

MODEL_path = "app/models/iforest.pkl"

def load_model():
    try:
        return joblib.load(MODEL_path)
    except:
        return None

def process_event(row_id: int, raw: str, ts: float, loop: asyncio.AbstractEventLoop):
    db = database.SessionLocal()
    try:
        parsed = parse_raw_line(raw)
        feat = features_from_parsed(parsed)
        X = np.array([[feat["is_beacon"], feat["is_deauth"], feat["rssi"]]])
        
        model = load_model()
        anomaly = 0
        score = None
        if model:
            pred = model.predict(X)
            score = model.decision_function(X)[0]
            anomaly = 1 if pred[0] == -1 else 0
        
        crud.update_log_processed(db, log_id=row_id, processed=parsed, anomaly=anomaly)
        
        if anomaly:
            context = {
                "id": row_id,
                "ts": ts,
                "raw": raw,
                "parsed": parsed,
                "score": float(score) if score is not None else None
            }
            report.generate_report(context)

        async def broadcast_event():
            log = crud.get_log(db, log_id=row_id)
            if log:
                await manager.broadcast({
                    "type": "new_log",
                    "data": {
                        "id": log.id,
                        "ts": log.ts,
                        "raw": log.raw,
                        "processed": log.processed,
                        "anomaly": log.anomaly
                    }
                })
        
        if loop:
            asyncio.run_coroutine_threadsafe(broadcast_event(), loop)
    finally:
        db.close()
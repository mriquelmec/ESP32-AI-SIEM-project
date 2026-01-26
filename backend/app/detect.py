import sqlite3
import json
from .preprocess import parse_raw_line, features_from_parsed
import joblib
import numpy as np
from .report import generate_report

MODEL_PATH = "app/models/iforest.pkl"

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        return None

def process_event(row_id, raw, ts):
    parsed = parse_raw_line(raw)
    feat = features_from_parsed(parsed)
    # convert to array
    X = np.array([[feat["is_beacon"], feat["is_deauth"], feat["rssi"]]])
    model = load_model()
    anomaly = 0
    score = None
    if model is not None:
        pred = model.predict(X)  # -1 = anomaly, 1 = normal
        score = model.decision_function(X)[0]
        anomaly = 1 if pred[0] == -1 else 0
    # Update DB
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("UPDATE logs SET processed=?, anomaly=? WHERE id=?", (json.dumps(parsed), anomaly, row_id))
    conn.commit()
    conn.close()

    if anomaly:
        # Llama a generador de reportes (envía parsed + evidencia)
        context = {
            "id": row_id,
            "ts": ts,
            "raw": raw,
            "parsed": parsed,
            "score": float(score) if score is not None else None
        }
        generate_report(context)

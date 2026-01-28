from sqlalchemy.orm import Session
from . import database, models

def get_log(db: Session, log_id: int):
    return db.query(database.Log).filter(database.Log.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Log).order_by(database.Log.ts.desc()).offset(skip).limit(limit).all()

def get_logs_count(db: Session):
    return db.query(database.Log).count()

def get_anomalies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Log).filter(database.Log.anomaly == 1).order_by(database.Log.ts.desc()).offset(skip).limit(limit).all()

def get_anomalies_count(db: Session):
    return db.query(database.Log).filter(database.Log.anomaly == 1).count()

def create_log(db: Session, raw: str, ts: float):
    db_log = database.Log(raw=raw, ts=ts, processed={}, anomaly=0)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update_log_processed(db: Session, log_id: int, processed: dict, anomaly: int):
    db_log = db.query(database.Log).filter(database.Log.id == log_id).first()
    if db_log:
        db_log.processed = processed
        db_log.anomaly = anomaly
        db.commit()
        db.refresh(db_log)
    return db_log

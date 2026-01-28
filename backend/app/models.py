from pydantic import BaseModel
from typing import Optional, Dict, Any

class LogBase(BaseModel):
    ts: float
    raw: str
    processed: Optional[Dict[str, Any]] = None
    anomaly: int

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True

class IngestModel(BaseModel):
    raw: str
    ts: float

import re
import numpy as np
import pandas as pd
from datetime import datetime

def parse_raw_line(raw: str) -> dict:
    # Ejemplo simplificado: adapta a tu output Marauder
    # Trata de extraer: event_type, ssid, bssid, rssi, channel, flags
    out = {"event_type": "unknown", "ssid": None, "bssid": None, "rssi": None, "channel": None}
    raw_lower = raw.lower()
    if "beacon" in raw_lower:
        out["event_type"] = "beacon"
    if "deauth" in raw_lower:
        out["event_type"] = "deauth"
    m = re.search(r"rssi[:= ](-?\d+)", raw_lower)
    if m:
        out["rssi"] = int(m.group(1))
    m2 = re.search(r"ssid[:= ]\"?([^\"]+)\"?", raw)
    if m2:
        out["ssid"] = m2.group(1)
    m3 = re.search(r"bssid[:= ]([0-9a-f:]{17})", raw_lower)
    if m3:
        out["bssid"] = m3.group(1)
    return out

def features_from_parsed(parsed: dict) -> dict:
    # Convertir a vectores; ejemplo simple
    feat = {}
    feat["is_beacon"] = 1 if parsed["event_type"]=="beacon" else 0
    feat["is_deauth"] = 1 if parsed["event_type"]=="deauth" else 0
    feat["rssi"] = parsed["rssi"] if parsed["rssi"] is not None else -100
    # Agrega features temporales, counts, rolling windows, etc.
    return feat

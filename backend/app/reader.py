import serial
import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()
SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUDRATE = int(os.getenv("BAUDRATE", 115200))
FASTAPI_URL = "http://127.0.0.1:8000/ingest"  # endpoint para enviar logs

def read_serial_and_post():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    buffer = ""
    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                time.sleep(0.1)
                continue
            # Aquí puedes filtrar o preprocesar antes de enviar
            payload = {"raw": line, "ts": time.time()}
            requests.post(FASTAPI_URL, json=payload, timeout=2)
        except Exception as e:
            print("Serial read error:", e)
            time.sleep(1)

if __name__ == "__main__":
    read_serial_and_post()

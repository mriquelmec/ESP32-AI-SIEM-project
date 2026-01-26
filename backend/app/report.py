import os
import openai
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
Eres un sistema que redacta reportes técnicos para un SIEM. Recibirás un evento de red con metadatos.
Genera un reporte breve (máx 300 palabras) que incluya:
- Resumen del evento
- Evidencia técnica (campos clave)
- Nivel de riesgo (bajo/medio/alto) y por qué
- Recomendaciones inmediatas (3 puntos)
Datos del evento (JSON):
{event_json}
"""

def generate_report(event_context: dict):
    event_json = json.dumps(event_context, indent=2)
    prompt = PROMPT_TEMPLATE.format(event_json=event_json)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # cambia según tu acceso; usa gpt-4o-mini o gpt-4o
        messages=[
            {"role":"system","content":"Eres un asistente técnico especializado en ciberseguridad."},
            {"role":"user","content": prompt}
        ],
        max_tokens=400,
        temperature=0.0
    )
    report_text = response["choices"][0]["message"]["content"]
    # Guardar reporte en disco / DB
    filename = f"reports/report_{event_context['id']}.txt"
    os.makedirs("reports", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {datetime.utcfromtimestamp(event_context['ts']).isoformat()}Z\n\n")
        f.write(report_text)
    print("Reporte generado:", filename)

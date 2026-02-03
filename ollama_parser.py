import ollama
import json
from parser import parse_text
MODEL = "qwen2.5:7b-instruct"
SYSTEM = """
    Para cada texto debes indicar en un json los siguientes datos sin informacion adicional ni inventada:
    {
        tipo: si es entrada o salida de dinero: debes color como valor en este campo "Entrada" o "Salida"; si no logras identificar pones "editar".
        medio: si es una salida entonces deberas identificar si es credito, debito o PSE o Transferencia. si no logras identificar cual es pones "editar".
        fecha: identifica la fecha en formato DD/MM/YYYY.
        hora: identifica la hora.
        valor: identifca cuanto fue el monto de la transacción y ponlo de forma exacta con decimales y todo.
        4x100: valor de 4x100, si no logras ponerlo pones 0.
    }
""".strip()
client = ollama.Client(host="http://localhost:11434")

def parse_to_json(ocr_text: str) -> dict:
    res = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Texto OCR:\n{ocr_text.strip()}"}
        ],
        options={"temperature": 0.0, "num_predict": 256}
    )

    content = res["message"]["content"].strip()
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Respuesta del modelo no contiene JSON.")
    return json.loads(content[start:end+1])
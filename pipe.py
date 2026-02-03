import sys
import json
from ocr import extract_text
from parser import parse_text
from ollama_parser import parse_to_json
from db import init_db, insert_movimiento

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pipe.py <imagen_recibo>")
        sys.exit(1)

    image_path = sys.argv[1]

    # Inicializa DB una sola vez
    init_db()

    # 1) OCR
    ocr_text = extract_text(image_path)

    # 2) Parser (normalización a un párrafo)
    parsed_text = parse_text(ocr_text)

    # 3) LLM → JSON
    tx = parse_to_json(parsed_text)

    # 4) Persistencia
    insert_movimiento(
        source="nu",
        file_name=image_path,
        data=tx
    )

    # 5) Output (debug / CLI)
    print(json.dumps(tx, ensure_ascii=False, indent=2))

import sqlite3
from datetime import datetime

DB_PATH = "finanzas.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            file_name TEXT,
            fecha TEXT,
            hora TEXT,
            tipo TEXT,
            medio TEXT,
            valor REAL,
            impuesto_4x100 REAL,
            raw_json TEXT,
            inserted_at TEXT
        )
        """)

def insert_movimiento(source, file_name, data):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO movimientos (
            source, file_name, fecha, hora, tipo, medio,
            valor, impuesto_4x100, raw_json, inserted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            source,
            file_name,
            data.get("fecha"),
            data.get("hora"),
            data.get("tipo"),
            data.get("medio"),
            data.get("valor"),
            data.get("4x100"),
            str(data),
            datetime.utcnow().isoformat()
        ))
def list_movimientos():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT
                id,
                source,
                file_name,
                fecha,
                hora,
                tipo,
                medio,
                valor,
                impuesto_4x100,
                inserted_at
            FROM movimientos
            ORDER BY inserted_at DESC
        """)
        return cursor.fetchall()

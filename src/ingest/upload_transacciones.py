import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar configuración
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Leer CSV de transacciones
df_trans = pd.read_csv(BASE_DIR / "data" / "raw" / "transacciones.csv")

# Crear tabla en SQL si no existe
create_table_sql = """
CREATE TABLE IF NOT EXISTS transacciones (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    fecha DATE,
    tipo_transaccion TEXT,
    monto NUMERIC(12, 2)
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    # Opcional: limpiar tabla para no duplicar
    conn.execute(text("DELETE FROM transacciones"))

# Insertar datos
df_trans.to_sql("transacciones", engine, if_exists="append", index=False)

print("✅ Transacciones insertadas correctamente en PostgreSQL")
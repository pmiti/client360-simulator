import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Crear conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# Leer CSV generado
df = pd.read_csv(BASE_DIR / "data" / "raw" / "clientes.csv")

# Crear tabla si no existe
create_table_sql = """
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INTEGER PRIMARY KEY,
    nombre TEXT,
    edad INTEGER,
    provincia TEXT,
    ingresos_mensuales INTEGER
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    # Borrar datos previos para no duplicar (opcional)
    conn.execute(text("DELETE FROM clientes"))

# Insertar datos
df.to_sql("clientes", engine, if_exists="append", index=False)

print("✅ Datos insertados correctamente en PostgreSQL")

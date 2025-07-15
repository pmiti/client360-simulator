import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Cargar data de clientes
df_clientes = pd.read_sql("SELECT * FROM clientes", engine)

# Cargar data de gasto mensual promedio
df_gasto = pd.read_sql("SELECT * FROM cliente_gasto_mensual", engine)

# Join por cliente_id
df_360 = pd.merge(df_clientes, df_gasto, on="cliente_id", how="left")

# Opcional: llenar con 0 donde no haya gasto
df_360["gasto_mensual_promedio"] = df_360["gasto_mensual_promedio"].fillna(0)

# Cargar score endeudamiento
df_score = pd.read_sql("SELECT * FROM cliente_score_endeudamiento", engine)

# Merge con lo anterior
df_360 = pd.merge(df_360, df_score, on="cliente_id", how="left")
df_360["score_endeudamiento"] = df_360["score_endeudamiento"].fillna(0)

# Crear tabla cliente_360
create_table_sql = """
CREATE TABLE IF NOT EXISTS cliente_360 (
    cliente_id INTEGER PRIMARY KEY,
    nombre TEXT,
    edad INTEGER,
    provincia TEXT,
    ingresos_mensuales INTEGER,
    gasto_mensual_promedio NUMERIC(12,2),
    score_endeudamiento NUMERIC(5,2)
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text("DELETE FROM cliente_360"))

# Insertar
df_360.to_sql("cliente_360", engine, if_exists="append", index=False)

print("✅ Tabla cliente_360 creada y cargada correctamente.")
print(df_360.head())

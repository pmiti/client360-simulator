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

# Cargar ingresos mensuales por cliente
df_clientes = pd.read_sql("SELECT cliente_id, ingresos_mensuales FROM clientes", engine)

# Cargar transacciones de tipo fijo
query = """
    SELECT cliente_id, monto
    FROM transacciones
    WHERE tipo_transaccion IN ('debito_automatico', 'pago_servicio')
"""
df_trans = pd.read_sql(query, engine)

# Agrupar: gasto total en pagos fijos
gasto_fijo = df_trans.groupby("cliente_id")["monto"].sum().reset_index()
gasto_fijo.rename(columns={"monto": "total_fijo"}, inplace=True)

# Join con ingresos
df_score = pd.merge(df_clientes, gasto_fijo, on="cliente_id", how="left")
df_score["total_fijo"] = df_score["total_fijo"].fillna(0)

# Calcular score
df_score["score_endeudamiento"] = df_score["total_fijo"] / df_score["ingresos_mensuales"]
df_score["score_endeudamiento"] = df_score["score_endeudamiento"].round(2)

# Crear tabla
create_table_sql = """
CREATE TABLE IF NOT EXISTS cliente_score_endeudamiento (
    cliente_id INTEGER PRIMARY KEY,
    score_endeudamiento NUMERIC(5,2)
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text("DELETE FROM cliente_score_endeudamiento"))

# Insertar
df_score[["cliente_id", "score_endeudamiento"]].to_sql(
    "cliente_score_endeudamiento", engine, if_exists="append", index=False
)

print("✅ Score de endeudamiento calculado y cargado.")
print(df_score[["cliente_id", "score_endeudamiento"]].head())
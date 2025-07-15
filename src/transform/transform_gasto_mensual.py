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

# Leer las transacciones desde la base
query = """
    SELECT cliente_id, fecha, tipo_transaccion, monto
    FROM transacciones
    WHERE tipo_transaccion IN (
        'compra_tarjeta', 'pago_servicio', 'debito_automatico', 'extraccion_cajero'
    )
"""
df = pd.read_sql(query, engine)

# Agregar columna año-mes
df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M")

# Agrupar: gasto total por cliente y mes
gasto_mensual = df.groupby(["cliente_id", "mes"])["monto"].sum().reset_index()

# Promedio mensual por cliente
promedio = gasto_mensual.groupby("cliente_id")["monto"].mean().reset_index()
promedio.rename(columns={"monto": "gasto_mensual_promedio"}, inplace=True)

# Crear tabla destino
create_table_sql = """
CREATE TABLE IF NOT EXISTS cliente_gasto_mensual (
    cliente_id INTEGER PRIMARY KEY,
    gasto_mensual_promedio NUMERIC(12, 2)
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text("DELETE FROM cliente_gasto_mensual"))

# Insertar
promedio.to_sql("cliente_gasto_mensual", engine, if_exists="append", index=False)

print("✅ Transformación completada: gasto_mensual_promedio cargado en la base")
print(promedio.head())

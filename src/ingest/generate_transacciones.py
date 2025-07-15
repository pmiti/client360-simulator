import pandas as pd
import random
from faker import Faker
from pathlib import Path

faker = Faker('es_AR')
random.seed(42)

# Configuración
BASE_DIR = Path(__file__).resolve().parents[2]
clientes_csv = BASE_DIR / "data" / "raw" / "clientes.csv"
output_dir = BASE_DIR / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "transacciones.csv"

# Cargar clientes
df_clientes = pd.read_csv(clientes_csv)
cliente_ids = df_clientes["cliente_id"].tolist()

# Tipos de transacciones y rangos de monto
tipos_transaccion = {
    "compra_tarjeta": (2000, 150000),
    "transferencia": (1000, 200000),
    "debito_automatico": (500, 30000),
    "extraccion_cajero": (1000, 50000),
    "pago_servicio": (1000, 40000),
    "ingreso_sueldo": (50000, 400000),
}

transacciones = []

for cliente_id in cliente_ids:
    num_trans = random.randint(50, 200)
    for _ in range(num_trans):
        tipo = random.choice(list(tipos_transaccion.keys()))
        monto_min, monto_max = tipos_transaccion[tipo]
        monto = round(random.uniform(monto_min, monto_max), 2)
        fecha = faker.date_between(start_date='-12m', end_date='today')

        transacciones.append({
            "cliente_id": cliente_id,
            "fecha": fecha,
            "tipo_transaccion": tipo,
            "monto": monto
        })

# Crear DataFrame
df_trans = pd.DataFrame(transacciones)

# Guardar CSV
df_trans.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ Transacciones generadas: {len(df_trans)}")
print(f"📁 Guardadas en: {output_file.resolve()}")
print(df_trans.head())

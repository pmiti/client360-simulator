import pandas as pd
import random
from faker import Faker
from pathlib import Path

# Configuración
faker = Faker('es_AR')
random.seed(42)
NUM_CLIENTES = 1000
BASE_DIR = Path(__file__).resolve().parents[2]  # Va dos niveles arriba: desde src/ingest/
output_dir = BASE_DIR / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "clientes.csv"

# Provincias comunes para simulación
provincias = [
    "Buenos Aires", "CABA", "Córdoba", "Santa Fe", "Mendoza",
    "Tucumán", "Salta", "Entre Ríos", "Neuquén", "Chaco"
]

# Simulación
clientes = []

for i in range(1, NUM_CLIENTES + 1):
    nombre = faker.name()
    edad = random.randint(18, 75)
    provincia = random.choice(provincias)
    ingresos_mensuales = round(random.gauss(200000, 80000))  # media, desvío
    ingresos_mensuales = max(ingresos_mensuales, 50000)  # no menos de $50k
    clientes.append({
        "cliente_id": i,
        "nombre": nombre,
        "edad": edad,
        "provincia": provincia,
        "ingresos_mensuales": ingresos_mensuales
    })

# Crear DataFrame
df = pd.DataFrame(clientes)

# Guardar en CSV
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Archivo generado: {output_file.resolve()}")
print(df.head())

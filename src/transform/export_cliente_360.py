import pandas as pd
from sqlalchemy import create_engine
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

# Leer tabla cliente_360
df = pd.read_sql("SELECT * FROM cliente_360", engine)

# Crear carpeta de salida si no existe
output_dir = BASE_DIR / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

# Guardar como CSV
output_path = output_dir / "cliente_360.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ Exportación completada. Archivo guardado en: {output_path.resolve()}")
print(df.head())
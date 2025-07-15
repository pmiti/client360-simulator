# client360-simulator

> Proyecto de simulación de un pipeline de datos financieros para análisis de comportamiento de clientes, replicando casos de uso comunes en bancos y fintechs.

---

## 🧠 Objetivo

Este proyecto simula un flujo de datos bancarios de punta a punta, desde la generación de datos crudos hasta la creación de una vista analítica consolidada (“cliente 360”).

Permite calcular métricas clave como:

- Gasto mensual promedio  
- Score de endeudamiento  
- Ingresos estimados  

Es una iniciativa orientada a demostrar habilidades técnicas de ingeniería de datos, especialmente para entrevistas en bancos, aseguradoras o empresas fintech.

---

## 🏗️ Arquitectura general

graph TD
    A[Simulación de datos] --> B[Ingesta en base de datos]
    B --> C[Transformaciones ETL]
    C --> D[Vista cliente_360]
    D --> E[Exportación a CSV]
    E --> F[Exploración con Notebook]

🧰 Stack tecnológico
Python (pandas, SQLAlchemy, Faker, matplotlib, seaborn)

PostgreSQL (almacenamiento de datos)

dotenv (manejo de variables de entorno)

Jupyter Notebook (exploración de resultados)

Opcionales para futuras versiones:

Docker (entorno replicable)

Airflow / Prefect (orquestación)

DBT (modelado de datos)

Streamlit (visualizaciones web)

📁 Estructura del proyecto
bash
Copiar
Editar
client360-simulator/
├── data/
│   ├── raw/             # Datos simulados (CSV)
│   └── processed/       # Salidas finales (CSV exportado)
├── notebooks/           # Exploración de datos (Jupyter)
├── src/
│   ├── ingest/          # Scripts de carga en PostgreSQL
│   ├── transform/       # Transformaciones ETL + exportación
│   └── utils/           # Utilidades y funciones auxiliares
├── .env.example         # Variables de entorno de ejemplo
├── requirements.txt     # Dependencias del proyecto
└── README.md
🚀 Cómo ejecutar el pipeline
Clonar el repositorio

bash
Copiar
Editar
git clone https://github.com/tu-usuario/client360-simulator.git
cd client360-simulator
Crear entorno virtual e instalar dependencias

bash
Copiar
Editar
python -m venv .venv

# En Windows
.venv\Scripts\activate

# En Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
Configurar la conexión a PostgreSQL

Copiar .env.example a .env

Completar con tus credenciales reales de PostgreSQL

Ejecutar scripts en orden:

bash
Copiar
Editar
# 1. Generar datos simulados
python src/ingest/generate_clientes.py
python src/ingest/generate_transacciones.py

# 2. Subir datos a PostgreSQL
python src/ingest/upload_clientes.py
python src/transform/upload_transacciones.py

# 3. Transformaciones intermedias
python src/transform/transform_gasto_mensual.py
python src/transform/transform_score_endeudamiento.py

# 4. Crear vista cliente 360
python src/transform/build_cliente_360.py

# 5. Exportar CSV final
python src/transform/export_cliente_360.py
🔎 El resultado final estará en: data/processed/cliente_360.csv

📊 Exploración de datos (Notebook)
Este proyecto incluye un notebook para visualizar el resultado final del pipeline.

Cómo abrirlo:
bash
Copiar
Editar
# Activar entorno virtual si no está activo
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # Linux/Mac

# Lanzar Jupyter
jupyter notebook
Abrir el archivo notebooks/exploracion_cliente360.ipynb y ejecutar cada celda.

Incluye:

Vista previa del dataset final

Descripción estadística

Histogramas de ingresos y gastos

Relación entre ingresos y endeudamiento por provincia

🧮 Explicación de métricas
Métrica	Descripción
gasto_mensual_promedio	Promedio de gastos recurrentes mensuales del cliente (compras, débitos, extracciones).
score_endeudamiento	Ratio entre pagos fijos (servicios y débitos automáticos) e ingresos mensuales.
ingresos_mensuales	Estimación de ingresos fijos del cliente (simulados).

📌 Estado actual
✅ Pipeline de datos funcional

✅ Transformaciones ETL básicas implementadas

✅ Exportación de datos finales a CSV

✅ Notebook exploratorio con visualizaciones

🔜 Orquestación automática (Airflow / Prefect)

🔜 Reportes interactivos (Streamlit / dashboards)

📣 Licencia y uso
Este proyecto es solo para fines educativos y demostrativos.
Los datos simulados no corresponden a personas reales.
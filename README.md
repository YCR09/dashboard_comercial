# 📈 Predicción de Próxima Compra (Customer Dashboard)

Este proyecto es un dashboard interactivo desarrollado con Streamlit que permite analizar historiales de compra desde archivos Excel y estimar la próxima fecha de compra de cada cliente.

---

## 🚀 Demo

Sube un archivo Excel con el historial de compras y obtén automáticamente:

- 📅 próxima compra estimada por cliente
- ⏳ días restantes
- 🔴🟡🟢 prioridad comercial
- 📊 dashboards interactivos
- 📥 descarga del resultado en Excel

---

## 🧠 Cómo funciona

El sistema calcula:

1. Intervalos entre compras por cliente
2. Media móvil de días entre compras
3. Estimación de próxima compra
4. Ranking de clientes según urgencia

---

## 📂 Formato del archivo Excel

El archivo debe contener al menos estas columnas:

| cliente   | fecha      |
|--------   |--------    |
| Cliente A | 2025-01-01 |
| Cliente A | 2025-02-01 |

📦 Dependencias:
streamlit
pandas
numpy
plotly
openpyxl
python-dotenv

📊 Funcionalidades:
Subida de archivos Excel
Limpieza y análisis de datos
Cálculo de frecuencia de compra
Predicción de próxima compra
Dashboard con gráficos interactivos
Exportación a Excel

📤 Exportación:
El usuario puede descargar el resultado final en formato Excel con:
Predicción por cliente
Prioridad comercial
Días restantes

📌 Tecnologías
Python 🐍
Streamlit 📊
Pandas 🧮
Plotly 📈

💡 Caso de uso
Ideal para:
Equipos comerciales
CRM básico
Análisis de clientes
Predicción de compras recurrentes

Proyecto desarrollado para análisis predictivo de clientes y automatización comercial.
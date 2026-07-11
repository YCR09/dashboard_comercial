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

## ⚖️ **Información Legal (Disclaimer) y Exención de Responsabilidad**
  
        "**Aviso:** Esta herramienta es un simulador con fines exclusivamente informativos, ilustrativos y educativos."
        "Los resultados, cálculos y proyecciones presentados son estimaciones basadas en los datos introducidos por el usuario y en fórmulas financieras estándar;"
        "por lo tanto, no garantizan resultados futuros, rendimientos ni el éxito comercial de ninguna operación. "
        "El uso de este simulador no constituye ni sustituye la asesoría financiera, contable, fiscal o legal profesional."
        " Cada negocio posee variables únicas y riesgos particulares. El desarrollador de esta herramienta no se hace responsable por pérdidas,"
        " daños o decisiones comerciales tomadas por el usuario basadas en la información generada por este sistema."

## ⭐ Si este proyecto te ha resultado útil, no olvides darle una estrella al repositorio.

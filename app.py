import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import openpyxl
import io
from dotenv import load_dotenv
import os

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

load_dotenv()

PASSWORD = st.secrets["PASSWORD"]

# Configiración Dashboard
st.set_page_config(page_title="Frecuencia Predictiva de compras", page_icon="📊", layout="wide")

st.write("⚖️ **Información Legal (Disclaimer) y Exención de Responsabilidad**")
st.caption(
        "**Aviso:** Esta herramienta es un simulador con fines exclusivamente informativos, ilustrativos y educativos."
        "Los resultados, cálculos y proyecciones presentados son estimaciones basadas en los datos introducidos por el usuario y en fórmulas financieras estándar;"
        "por lo tanto, no garantizan resultados futuros, rendimientos ni el éxito comercial de ninguna operación. "
        "El uso de este simulador no constituye ni sustituye la asesoría financiera, contable, fiscal o legal profesional."
        " Cada negocio posee variables únicas y riesgos particulares. El desarrollador de esta herramienta no se hace responsable por pérdidas,"
        " daños o decisiones comerciales tomadas por el usuario basadas en la información generada por este sistema."
    )
st.title("💼 Dashboard - Modelo Predictivo de Compras - 2026", anchor = False)
st.markdown("---")

# estado login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# pantalla login
if not st.session_state.authenticated:

    st.title("🔒 Acceso privado")

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Entrar"):

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")

    st.stop()

def datos(df):
     
    df["fecha"] = pd.to_datetime(df["fecha"])

    df = df.sort_values(["cliente", "fecha"])

    # 3. Extraer la fecha mínima y máxima
    fecha_inicio = df['fecha'].min().strftime('%d/%m/%Y')
    fecha_fin = df['fecha'].max().strftime('%d/%m/%Y')

     # 4. Mostrar el período en un contenedor llamativo al inicio
    st.info(f"📅 **Período de Análisis detectado:** Del **{fecha_inicio}** al **{fecha_fin}**")

    # calcular días entre compras
    df["dias_entre_compras"] = (
        df.groupby("cliente")["fecha"]
        .diff()
        .dt.days
    )

    resultados = []

    # calcular media 
    for cliente, grupo in df.groupby("cliente"):

        #intervalos = grupo["dias_entre_compras"].dropna()
        intervalos = grupo["dias_entre_compras"].fillna(0)

        #if len(intervalos) < 2:
        #    continue
        
        if len(intervalos) < 1:
            continue
    
        # calcula meduia móvil solo las 5 últimas compras con tail(5)
        media_dias = intervalos.tail(5).mean()

        # calcula la media movil ponderada
        intervalos_recientes = intervalos.tail(5)

        #calcula el peso de cada cliente según la cantidad de compra
        pesos = np.arange(1, len(intervalos_recientes) + 1)

        media_ponderada = (intervalos_recientes * pesos).sum() / sum(pesos)

       
        ultima_fecha = grupo["fecha"].max()

        #Calculo de la proxima compra con la media móvil
        proxima_compra_media = (
            ultima_fecha +
            pd.Timedelta(days=media_dias)
        )

        dias_restantes_media = (
            proxima_compra_media - pd.Timestamp.today()
        ).days

        #Calculo de la proxima compra con la media ponderada
        proxima_compra_ponderada = (
            ultima_fecha +
            pd.Timedelta(days=media_ponderada)
        )

        dias_restantes_ponderada = (
            proxima_compra_ponderada - pd.Timestamp.today()
        ).days
  
        desviacion = intervalos_recientes.std()

        if desviacion < 10:
            confianza = "Alta"
        elif desviacion < 25:
            confianza = "Media"
        else:
            confianza = "Baja"

        media_total = (dias_restantes_media + dias_restantes_ponderada) / 2

        # prioridad
        if media_total <= 3:
           prioridad = "Alta"
        elif media_total <= 7:
            prioridad = "Media"
        else:
            prioridad = "Baja"

        total_ventas = round(grupo["ventas"].sum(), 2)
        media_ventas = round(grupo["ventas"].mean(), 2)
        cantidad_ventas = grupo["ventas"].count()
        #cantidad_compras = len(grupo)

        resultados.append({
            "cliente": cliente,
            "ultima_compra": ultima_fecha.date(),
            "prioridad": prioridad,
            "confianza": confianza,
            "total_dias": round(media_total, 0),
            "total_ventas": total_ventas,
            "media_ventas": media_ventas,
            "cantidad_ventas": cantidad_ventas
        })

    resultado_df = pd.DataFrame(resultados)

    # ordenar por próxima compra
    resultado_df = resultado_df.sort_values(
        "total_dias"
    )

    #Clientes únicos por mes

    #3. Calcular clientes únicos por mes
    df_clientes_mes = (
            df.groupby(df["fecha"].dt.to_period("M"))
            .agg(clientes_unicos=("cliente", "nunique"))
            .reset_index()
            )
    df_clientes_mes.rename(columns={"fecha": "mes"}, inplace=True)

    df_clientes_mes["mes"] = df_clientes_mes["mes"].astype(str) 

    # Pedidos por mes
    df_ventas_mes = (
                df.groupby(df["fecha"].dt.to_period("M"))
                .size()
                .reset_index(name="ventas")
            )
        
        # Renombrar la columna del período
    df_ventas_mes.rename(columns={"fecha": "mes"}, inplace=True)

        # Convertir a texto
    df_ventas_mes["mes"] = df_ventas_mes["mes"].astype(str) 
    
    # ********************** KPIs **************************************
    st.markdown("## ✔ KPI's ")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "Total Clientes",
        len(resultado_df)
    )

    col2.metric(
        "Media Clientes (mes)",
        f"{df_clientes_mes["clientes_unicos"].mean():,.0f}"
        
    )

    col3.metric(
        "Alta prioridad",
        len(
            resultado_df[
                resultado_df["prioridad"] == "Alta"
            ]
        )
    )
    col4.metric(
        "Media días compra",
        round(
            resultado_df["total_dias"].abs().mean(),
            1
        )
    )

    col5.metric(
        #"Media venta", f"€{round(resultado_df['media_ventas'].mean(), 2)}"
        "Toptal Pedidos", len(df)
        )
    
    col6.metric(
        "Media Pedido (mes)",
        f"{df_ventas_mes["ventas"].mean():,.0f}"
        
    )

    st.divider()

    # ******************* tabla principal ***************************
   
    st.subheader("☎️ Lista Ordenada de Clientes próximos a comprar ☎️")

    st.dataframe(
        resultado_df,
        use_container_width=True
    )

    
    # ************************ gráficos ************************** 
    
    st.markdown('## ✔ Análisis de Pedidos y Clientes')

    # Gráfico pedidos por mes
    fig_mes = px.bar(
            df_ventas_mes,
            x="mes",
            y='ventas',
            title="📝 Número de Pedidos por Mes",
            #color="fecha",
            text_auto=True,
            #labels={"fecha": "Mes", "count": "Cantidad de Pedidos"}
            
        )
    #fig_mes.update_layout(bargap=0.2) # Añade espacio entre barras
    fig_mes.update_traces(textposition="outside")
        
    st.plotly_chart(
                fig_mes,
                use_container_width=True
            )

    # Gráfico Clientes únicos por mes

    fig_cli = px.bar(
            df_clientes_mes,
            x="mes",
            y='clientes_unicos',
            #histfunc='distinct',
            title="🎯 Clientes únicos por Mes",
            #color="fecha",
            text="clientes_unicos"
            #text_auto=True,
            #labels={"fecha": "Mes", "count": "Cantidad de Pedidos"}
            
        )
    st.plotly_chart(
                fig_cli,
                use_container_width=True
            )

    col1, col2 = st.columns(2)

    # gráfico prioridad
    with col1:

        fig_prioridad = px.histogram(
            resultado_df,
            x="prioridad",
            title="⭐ Clientes por prioridad",
            color="prioridad",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        st.plotly_chart(
            fig_prioridad,
            use_container_width=True
        )

      
    # gráfico torta prioridad en %
    with col2:

        prioridad_count = (
            resultado_df["prioridad"]
            .value_counts()
            .reset_index()
        )

        prioridad_count.columns = [
            "prioridad",
            "cantidad"
        ]
        fig_prioridad = px.pie(
            prioridad_count,
            names="prioridad",
            values="cantidad",
            title="✅ Clientes por prioridad en %",
            color_discrete_sequence=px.colors.qualitative.G10
        )

        st.plotly_chart(
            fig_prioridad,
            use_container_width=True
        )

    # *************************** top clientes urgentes *****************************
    st.subheader("🚨 Top clientes urgentes 🚨")

    st.dataframe(
        resultado_df.head(15),
        use_container_width=True
    )

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
    
        resultado_df.to_excel(
            writer,
            index=False,
            sheet_name="Predicción"
        )
    excel_buffer.seek(0)

    st.download_button(
        "📥 Descargar lista ordenada excel",
        data=excel_buffer,
        file_name="pronóstico.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
#cargar datos de excel desde el directorio local
mensaje = st.warning(" 👈 Ve a la sección del menú lateral **Fuente de Datos** y selecciona una opción de datos para analizar")
def main():
    opcion = st.sidebar.radio(
            " **FUENTE DE DATOS :**",
            (
                "Seleccione una opción...",
                "📝 Datos de demostración",
                "📁 Cargar archivo Excel",
                #"☁️ Google Drive Sheets"
            ),
            index=0
        )
    if opcion == "📝 Datos de demostración":
            mensaje.empty()
            try:
                df = pd.read_excel("ventas_datos.xlsx")
                
                #st.session_state['df_excel'] = df

                st.success("Datos de demostración cargados.")
                #st.dataframe(df.head())
                
                datos(df)
            except Exception as e:
                st.error(f"Error al leer el archivo {e}")
    elif opcion == "📁 Cargar archivo Excel":
            mensaje.empty()
            uploaded_file = st.file_uploader(
                "Subir un archivo Excel con las siguientes columnas en este orden a analizar :  | **cliente** | **fecha** | **ventas** | -> la columna  **cliente** es el código o id del cliente.",
                type=["xlsx"]
            )
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)

                    # 2. Convertir los nombres de las columnas a minúsculas
                    df.columns = df.columns.str.strip().str.lower()
                    st.success("Datos de archivo **excel** cargados.")
                    datos(df)
                except Exception as e:
                            st.error(f"Error al leer el archivo {e}")

    # botón cerrar sesión
    if st.sidebar.button("🚪 Cerrar sesión"):

        st.session_state.authenticated = False

        st.rerun()
    
if __name__ == "__main__":
    main()  


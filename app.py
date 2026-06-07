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
st.title("📈 DEMO Pronóstico de Próxima Compra")

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


#cargar datos de excel desde el directorio local
#df = pd.read_excel("ventas_datos.xlsx")

# subir excel

uploaded_file = st.file_uploader(
    "Sube archivo Excel con dos columnas en minúsculas : cliente , fecha, ventas",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

#print(df)

    df["fecha"] = pd.to_datetime(df["fecha"])

    df = df.sort_values(["cliente", "fecha"])

#print(df)

   # calcular días entre compras
    
    df["dias_entre_compras"] = (
        df.groupby("cliente")["fecha"]
        .diff()
        .dt.days
    )

    #print(df)

    resultados = []

    
    # calcular media 
   
    for cliente, grupo in df.groupby("cliente"):

        #intervalos = grupo["dias_entre_compras"].dropna()
        intervalos = grupo["dias_entre_compras"].fillna(0)

        #if len(intervalos) == 0:
        #    continue

        if len(intervalos) < 2:
            continue
        
        # calcula solo las 5 últimas compras con tail(5)
        media_dias = intervalos.tail(5).mean()

        #media_dias = intervalos.mean()

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
    
        #calulo de la confinaza del cliente
        desviacion = intervalos_recientes.std()

        if desviacion < 10:
            confianza = "Alta"
        elif desviacion < 25:
            confianza = "Media"
        else:
            confianza = "Baja"

        #calculo de la media de las medias
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
    
        resultados.append({
            "cliente": cliente,
            "ultima_compra": ultima_fecha.date(),
#            "media_dias": round(media_dias, 1),
#           "proxima_compra_media": proxima_compra_media.date(),
#            "dias_restantes_media": dias_restantes_media,
            "prioridad": prioridad,
#            "proxima_compra_ponderada": proxima_compra_ponderada.date(),
#            "dias_restantes_ponderada": dias_restantes_ponderada,
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

# KPIs

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Clientes",
        len(resultado_df)
    )

    col2.metric(
        "Alta prioridad",
        len(
            resultado_df[
                resultado_df["prioridad"] == "Alta"
            ]
        )
    )

    col3.metric(
        "Media días compra",
        round(
            resultado_df["total_dias"].mean(),
            1
        )
    )

    col4.metric(
        "Media venta", f"€{round(resultado_df['media_ventas'].mean(), 2)}"
        )

    st.divider()

    st.divider()

    
    #   tabla principal
   
    st.subheader("☎️ Lista Ordenada de Clientes próximos a comprar ☎️")

    st.dataframe(
        resultado_df,
        use_container_width=True
    )

    
    # gráficos
 
    col1, col2 = st.columns(2)

    # Lista con colores específicos
    colores = ['red', 'green', 'yellow']

    # gráfico prioridad
    with col1:

        fig_prioridad = px.histogram(
            resultado_df,
            x="prioridad",
            title="Clientes por prioridad",
            color="prioridad",
            text_auto=True,
#            color_discrete_sequence=['red', 'yellow', 'green']
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
            title="Clientes por prioridad",
#            color_discrete_sequence=colores
            color_discrete_sequence=px.colors.qualitative.G10
        )

        st.plotly_chart(
            fig_prioridad,
            use_container_width=True
        )


    
    # top clientes urgentes
    
    st.subheader("🚨 Top clientes urgentes 🚨")

    st.dataframe(
        resultado_df.head(10),
        use_container_width=True
    )
    
    # exportar csv

    #csv = resultado_df.to_csv(
    #    index=False
    #).encode("utf-8")

    #st.download_button(
    #    "📥 Descargar resultados cvs",
    #    csv,
    #    "pronostico.csv",
    #    "text/csv"
    #)

    #print(resultado_df)

    
    # exportar excel
    

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
    
        resultado_df.to_excel(
            writer,
            index=False,
            sheet_name="Prediccion"
        )

    excel_buffer.seek(0)

    st.download_button(
        "📥 Descargar lista ordenada excel",
        data=excel_buffer,
        file_name="pronostico.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # botón cerrar sesión
    if st.sidebar.button("🚪 Cerrar sesión"):

        st.session_state.authenticated = False

        st.rerun()

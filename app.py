import streamlit as st
import pandas as pd

# --- Cargar datos desde archivo local ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("relevamiento.xlsx", engine="openpyxl")
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo 'relevamiento.xlsx'. Asegurate que esté en la misma carpeta que esta app.")
        return pd.DataFrame()  # Devuelve DataFrame vacío

df = load_data()

# --- Configuración de la página ---
st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

# --- Estilo profesional ---
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
            display: block;
        }
        .stDataFrame {
            text-align: center;
        }
        .titulo {
            text-align: center;
            color: #003366;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">🔎 Buscador de Relevamiento</div>', unsafe_allow_html=True)

# --- Barra de búsqueda centrada ---
search = st.text_input("", key="search_input")

# --- Paginación ---
def mostrar_resultados(resultados, pagina_actual, por_pagina=1):
    total = len(resultados)
    if total == 0:
        st.warning("No se encontraron resultados.")
        return

    start_idx = (pagina_actual - 1) * por_pagina
    end_idx = start_idx + por_pagina
    st.dataframe(resultados.iloc[start_idx:end_idx], use_container_width=True)

    # Botones de paginación
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if pagina_actual > 1:
            if st.button("Anterior"):
                return pagina_actual - 1
    with col3:
        if end_idx < total:
            if st.button("Siguiente"):
                return pagina_actual + 1
    return pagina_actual

# --- Lógica de búsqueda ---
if search and not df.empty:
    resultados = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
    st.write(f"Se encontraron **{len(resultados)}** resultados para: `{search}`")
    
    pagina_actual = 1
    while True:
        nueva_pagina = mostrar_resultados(resultados, pagina_actual)
        if nueva_pagina == pagina_actual:
            break
        else:
            pagina_actual = nueva_pagina

elif df.empty:
    st.stop()








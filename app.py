import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Buscador Relevamiento", page_icon="🔍", layout="centered")

# --- TÍTULO DE LA APP ---
st.markdown("<h1 style='text-align: center; color: #003366;'>Buscador de Relevamiento</h1>", unsafe_allow_html=True)

# --- FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data
def load_data():
    url_csv = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/refs/heads/main/relevamiento.csv?token=GHSAT0AAAAAADMG3X2DW7TIIFERDW6I3ZVO2G4D2MQ"
    try:
        df = pd.read_csv(url_csv)
        return df
    except Exception as e:
        st.error(f"No se pudieron cargar los datos. Error: {e}")
        return pd.DataFrame()  # Retorna DataFrame vacío si falla

# --- CARGAR DATOS ---
df = load_data()

# --- CAJA DE BÚSQUEDA ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
search_value = st.text_input("", "").strip()  # Caja centrada, sin texto guía
st.markdown("</div>", unsafe_allow_html=True)

# --- FUNCION PAGINACIÓN ---
def mostrar_resultado(df_busqueda, page_num, resultados_por_pagina=1):
    start_idx = page_num * resultados_por_pagina
    end_idx = start_idx + resultados_por_pagina
    sub_df = df_busqueda.iloc[start_idx:end_idx]

    # Mostrar resultados centrados
    for i in range(len(sub_df)):
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.table(sub_df.iloc[i:i+1])  # Mostrar un resultado por página
        st.markdown("</div>", unsafe_allow_html=True)

# --- LÓGICA DE BÚSQUEDA Y PAGINACIÓN ---
if search_value:
    df_result = df[(df.astype(str).apply(lambda row: search_value.lower() in row.str.lower().to_string(), axis=1))]
    
    if not df_result.empty:
        # Control de páginas
        if "page_num" not in st.session_state:
            st.session_state.page_num = 0
        
        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.button("Anterior") and st.session_state.page_num > 0:
                st.session_state.page_num -= 1
        with col3:
            if st.button("Siguiente") and st.session_state.page_num < len(df_result)-1:
                st.session_state.page_num += 1
        
        mostrar_resultado(df_result, st.session_state.page_num)
    else:
        st.warning("No se encontraron resultados para la búsqueda.")





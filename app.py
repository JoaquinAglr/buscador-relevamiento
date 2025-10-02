import streamlit as st
import pandas as pd
from style import STYLES  # importa tus estilos CSS

st.set_page_config(page_title="Buscador de Relevamiento", layout="centered")

# Inyectar CSS
st.markdown(STYLES, unsafe_allow_html=True)

# Encabezado tipo Google
st.markdown(
    """
    <div class="header-google">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" alt="logo">
        <h1>Buscador de Relevamiento</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Cargar CSV
try:
    df = pd.read_csv("relevamiento.csv", encoding="utf-8")
except Exception as e:
    st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
    st.stop()

# Input principal
query = st.text_input("Ingrese texto a buscar", placeholder="Buscar en relevamiento...")

# Botón de búsqueda
buscar = st.button("🔍 Buscar")

# Mostrar resultados
if buscar and query:
    # Por defecto busca en todas las columnas
    resultados = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
    
    st.subheader("Resultados de la búsqueda")
    st.write(f"🔎 {len(resultados)} resultados encontrados")
    st.dataframe(resultados)
elif buscar:
    st.info("Ingrese un término para buscar.")

# Vista previa siempre abajo
st.subheader("Vista previa de los datos")
st.dataframe(df.head(20))












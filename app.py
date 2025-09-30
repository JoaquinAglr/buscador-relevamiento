import streamlit as st
import pandas as pd

# --- Cargar datos desde GitHub ---
@st.cache_data
def load_data():
    url_excel = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/main/relevamiento.xlsx"
    df = pd.read_excel(url_excel)
    return df

df = load_data()

# --- Configuración de la página ---
st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

st.title("🔎 Buscador de Relevamiento")
st.markdown("Aplicación para buscar información en el relevamiento cargado en Excel.")

# --- Barra de búsqueda ---
search = st.text_input("Buscar por cualquier palabra o código:")

if search:
    resultados = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
    st.write(f"Se encontraron **{len(resultados)}** resultados para: `{search}`")
    st.dataframe(resultados, use_container_width=True)
else:
    st.info("Ingresá un término de búsqueda para ver resultados.")

# --- Mostrar todo si no hay búsqueda ---
if st.checkbox("Mostrar todo el relevamiento"):
    st.dataframe(df, use_container_width=True)






import streamlit as st
import pandas as pd

# ✅ URL raw directa al CSV en GitHub
GITHUB_URL = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/main/relevamiento.csv"

st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

st.title("📊 Buscador de Relevamiento")

# Intentamos cargar los datos
try:
    df = pd.read_csv(GITHUB_URL, encoding="utf-8", sep=",")  # cambia sep=";" si tu CSV lo usa
    st.success("✅ Datos cargados desde GitHub correctamente.")
except Exception as e:
    st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
    st.stop()

# Mostrar preview
st.subheader("Vista previa de los datos")
st.dataframe(df.head(20))

# Barra lateral para búsqueda
st.sidebar.header("🔍 Filtros de búsqueda")

# Seleccionar columna
columna = st.sidebar.selectbox("Seleccionar columna para buscar", df.columns)

# Texto de búsqueda
query = st.sidebar.text_input("Ingrese texto a buscar")

# Filtrar datos
if query:
    resultados = df[df[columna].astype(str).str.contains(query, case=False, na=False)]
    st.subheader("Resultados de la búsqueda")
    st.write(f"🔎 {len(resultados)} resultados encontrados")
    st.dataframe(resultados)
else:
    st.info("Ingrese un término de búsqueda en la barra lateral.")







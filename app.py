import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

st.title("📊 Buscador de Relevamiento")

# Cargar CSV local dentro del repo
try:
    df = pd.read_csv("relevamiento.csv", encoding="utf-8")
except Exception as e:
    st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
    st.stop()

# Tabs: primero búsqueda, luego vista previa
tab1, tab2 = st.tabs(["🔎 Búsqueda", "📋 Vista previa"])

with tab1:
    st.sidebar.header("Filtros de búsqueda")

    # Seleccionar columna
    columna = st.sidebar.selectbox("Seleccionar columna para buscar", df.columns)

    # Texto de búsqueda
    query = st.sidebar.text_input("Ingrese texto a buscar")

    if query:
        resultados = df[df[columna].astype(str).str.contains(query, case=False, na=False)]
        st.subheader("Resultados de la búsqueda")
        st.write(f"🔎 {len(resultados)} resultados encontrados")

        # Mostrar tabla con botones
        for i, row in resultados.iterrows():
            with st.expander(f"🔹 {columna}: {row[columna]}"):
                st.write(row)   # muestra todos los datos de esa fila
    else:
        st.info("Ingrese un término de búsqueda en la barra lateral.")

with tab2:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(20))












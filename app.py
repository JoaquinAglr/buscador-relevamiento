import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

st.title("📊 Buscador de Relevamiento")

# Cargar CSV
try:
    df = pd.read_csv("relevamiento.csv", encoding="utf-8")
except Exception as e:
    st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
    st.stop()

# Tabs
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

        # Tabla sin botón de descarga
        st.dataframe(resultados, use_container_width=True, hide_index=False)

        # Selector para elegir una fila
        if not resultados.empty:
            fila_idx = st.selectbox(
                "👉 Seleccione un registro para ver en detalle",
                resultados.index,
                format_func=lambda x: f"{columna}: {resultados.loc[x, columna]}"
            )

            # Mostrar detalle en formato ficha
            if fila_idx is not None:
                st.markdown("### 📌 Detalle del registro seleccionado")
                fila = resultados.loc[fila_idx]
                for c, v in fila.items():
                    st.write(f"**{c}:** {v}")

    else:
        st.info("Ingrese un término de búsqueda en la barra lateral.")

with tab2:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(20), use_container_width=True, hide_index=False)












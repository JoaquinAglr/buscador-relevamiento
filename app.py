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

        # Mostrar resultados encontrados debajo de la barra lateral
        st.sidebar.markdown(f"**🔎 {len(resultados)} resultados encontrados**")

        if not resultados.empty:
            # Inicializar índice en session_state
            if "indice" not in st.session_state:
                st.session_state.indice = 0

            # Validar rango
            st.session_state.indice = max(0, min(st.session_state.indice, len(resultados) - 1))

            # Centrar la tarjeta con columnas vacías
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                fila = resultados.iloc[st.session_state.indice]
                st.markdown("### 📌 Detalle del registro seleccionado")
                st.write("---")
                for c, v in fila.items():
                    st.markdown(f"**{c}:** {v}")
                st.write("---")

                # Botones navegación
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("⬅️ Anterior") and st.session_state.indice > 0:
                        st.session_state.indice -= 1
                        st.rerun()
                with col3:
                    if st.button("Siguiente ➡️") and st.session_state.indice < len(resultados) - 1:
                        st.session_state.indice += 1
                        st.rerun()

                st.caption(f"Mostrando registro {st.session_state.indice + 1} de {len(resultados)}")

    else:
        st.info("Ingrese un término de búsqueda en la barra lateral.")

with tab2:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(20), use_container_width=True, hide_index=False)






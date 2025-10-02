import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")

# --- Función para mostrar tarjeta con estilo ---
def mostrar_tarjeta(fila):
    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd; 
            border-radius:8px; 
            padding:15px; 
            margin-bottom:10px; 
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            background-color:#f9f9f9;
        ">
        {''.join([f"<p><b>{c}:</b> {v}</p>" for c, v in fila.items()])}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Título de la página más pequeño ---
st.markdown("## 📊 Buscador de Relevamiento")

# Cargar CSV
try:
    df = pd.read_csv("relevamiento.csv", encoding="utf-8")
except Exception as e:
    st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["🔎 Búsqueda", "📋 Vista previa"])

# Cantidad de tarjetas por página
TARJETAS_POR_PAGINA = 6

with tab1:
    st.sidebar.header("Filtros de búsqueda")

    # Seleccionar columna
    columna = st.sidebar.selectbox("Seleccionar columna para buscar", df.columns)

    # Texto de búsqueda
    query = st.sidebar.text_input("Ingrese texto a buscar")

    if query:
        resultados = df[df[columna].astype(str).str.contains(query, case=False, na=False)]
        st.sidebar.markdown(f"**🔎 {len(resultados)} resultados encontrados**")

        if not resultados.empty:
            # Inicializar índice de página en session_state
            if "pagina" not in st.session_state:
                st.session_state.pagina = 0

            # Validar página
            total_paginas = (len(resultados) - 1) // TARJETAS_POR_PAGINA + 1
            st.session_state.pagina = max(0, min(st.session_state.pagina, total_paginas - 1))

            # Determinar rango de registros a mostrar
            start_idx = st.session_state.pagina * TARJETAS_POR_PAGINA
            end_idx = start_idx + TARJETAS_POR_PAGINA
            resultados_pagina = resultados.iloc[start_idx:end_idx]

            # Mostrar tarjetas en dos columnas
            col1, col2 = st.columns(2)
            for i, (_, fila) in enumerate(resultados_pagina.iterrows()):
                if i % 2 == 0:
                    with col1:
                        mostrar_tarjeta(fila)
                else:
                    with col2:
                        mostrar_tarjeta(fila)

            # Botones de navegación de página
            col_prev, col_space, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅️ Anterior") and st.session_state.pagina > 0:
                    st.session_state.pagina -= 1
                    st.rerun()
            with col_next:
                if st.button("Siguiente ➡️") and st.session_state.pagina < total_paginas - 1:
                    st.session_state.pagina += 1
                    st.rerun()

            st.caption(f"Mostrando página {st.session_state.pagina + 1} de {total_paginas}")

    else:
        st.info("Ingrese un término de búsqueda en la barra lateral.")

with tab2:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(20), use_container_width=True, hide_index=False)






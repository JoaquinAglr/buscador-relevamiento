import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(
    page_title="Relevamiento de Inventario",
    page_icon="📋",
    layout="wide"
)

# Ruta al archivo Excel en GitHub
excel_url = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/main/total relevamiento municipio.xlsx"
df = pd.read_excel(excel_url, engine="openpyxl")


# Leer archivo Excel
try:
    df = pd.read_excel(ruta_archivo, engine="openpyxl")
except Exception as e:
    st.error(f"No se pudo cargar el archivo: {e}")
    st.stop()

# Título
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📋 Relevamiento de Inventario</h1>", unsafe_allow_html=True)
st.markdown("---")

# Caja de búsqueda centrada y corta
col_b1, col_b2, col_b3 = st.columns([3, 2, 3])
with col_b2:
    busqueda = st.text_input("", key="busqueda")

if busqueda:
    # Filtrar resultados
    resultados = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

    if resultados.empty:
        st.warning("⚠️ No se encontraron coincidencias.")
    else:
        # Paginación - 1 resultado por página
        resultados_por_pagina = 1
        total_resultados = len(resultados)
        total_paginas = max(1, (total_resultados - 1) // resultados_por_pagina + 1)

        if "pagina" not in st.session_state:
            st.session_state["pagina"] = 1

        # Control de paginación siempre visible
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            anterior_desactivado = st.session_state["pagina"] == 1
            if st.button("⬅️ Anterior", disabled=anterior_desactivado):
                if not anterior_desactivado:
                    st.session_state["pagina"] -= 1
        with col3:
            siguiente_desactivado = st.session_state["pagina"] == total_paginas
            if st.button("Siguiente ➡️", disabled=siguiente_desactivado):
                if not siguiente_desactivado:
                    st.session_state["pagina"] += 1

        pagina = st.session_state["pagina"]
        inicio = (pagina - 1) * resultados_por_pagina
        fin = inicio + resultados_por_pagina

        st.markdown(
            f"<p style='text-align:center; color:gray;'>Resultado {inicio+1} de {total_resultados}</p>",
            unsafe_allow_html=True
        )

        # Mostrar un resultado centrado con tarjeta profesional
        for _, row in resultados.iloc[inicio:fin].iterrows():
            col_c1, col_c2, col_c3 = st.columns([2, 3, 2])
            with col_c2:
                # Tarjeta con borde azul oscuro y sombra ligera
                st.markdown(
                    "<div style='border:2px solid #1f4e79; border-radius:12px; "
                    "padding:20px; margin:15px 0; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align:center;'>",
                    unsafe_allow_html=True
                )
                # Resumen de datos clave arriba
                for key in ["MAC", "Número de Inventario", "Modelo"]:
                    if key in resultados.columns:
                        st.markdown(f"**{key}:** {row[key]}")
                st.markdown("<hr>", unsafe_allow_html=True)
                # Mostrar todas las columnas
                for col in resultados.columns:
                    st.markdown(f"**{col}:** {row[col]}")
                st.markdown("</div>", unsafe_allow_html=True)




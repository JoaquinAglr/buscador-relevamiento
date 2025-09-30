import streamlit as st
import pandas as pd

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(
    page_title="Buscador de Relevamiento",
    page_icon="🔍",
    layout="centered"
)

# -------------------------------
# Título
# -------------------------------
st.markdown(
    "<h1 style='text-align: center; color: #003366;'>Buscador de Relevamiento</h1>",
    unsafe_allow_html=True
)

# -------------------------------
# Cargar datos desde GitHub
# -------------------------------
url_csv = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/main/relevamiento.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(url_csv)
        return df
    except Exception as e:
        st.error(f"❌ No se pudieron cargar los datos. Error: {e}")
        return pd.DataFrame()  # retorna dataframe vacío si falla

df = load_data()

# -------------------------------
# Caja de búsqueda
# -------------------------------
search_input = st.text_input("", placeholder="", key="search_box")

# -------------------------------
# Función de búsqueda
# -------------------------------
def search_data(df, query):
    if query == "":
        return pd.DataFrame()
    # Buscar en todas las columnas, case-insensitive
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    return df[mask]

results = search_data(df, search_input)

# -------------------------------
# Paginación
# -------------------------------
if not results.empty:
    results.reset_index(drop=True, inplace=True)
    if "page" not in st.session_state:
        st.session_state.page = 0

    total_pages = len(results)
    current_page = st.session_state.page

    # Mostrar un solo resultado por página
    row = results.iloc[current_page]

    # Mostrar la información centrada
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    for col in results.columns:
        st.markdown(f"**{col}:** {row[col]}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Botones de paginación
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Anterior") and current_page > 0:
            st.session_state.page -= 1
    with col3:
        if st.button("Siguiente") and current_page < total_pages - 1:
            st.session_state.page += 1
else:
    if search_input != "":
        st.warning("No se encontraron resultados.")





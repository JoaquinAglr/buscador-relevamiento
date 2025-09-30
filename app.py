import streamlit as st
import pandas as pd

# Links
URL_ONEDRIVE = "https://mvl365-my.sharepoint.com/:x:/g/personal/joaquin_aguilar_vicentelopez_gov_ar/EcULpy53BUdNnWG0uJtwhfUBkF6Hl6mr1mp-0zOtqg09kw?download=1"
URL_GITHUB = "https://raw.githubusercontent.com/JoaquinAglr/buscador-relevamiento/main/relevamiento.xlsx"

@st.cache_data
def load_data():
    try:
        # Intentar con OneDrive
        return pd.read_excel(URL_ONEDRIVE, engine="openpyxl")
    except Exception as e:
        st.warning(f"No se pudo cargar desde OneDrive ({e}), intentando con GitHub...")
        return pd.read_excel(URL_GITHUB, engine="openpyxl")

def main():
    st.set_page_config(page_title="Buscador de Relevamiento", layout="wide")
    st.title("📊 Buscador de Relevamiento")

    try:
        df = load_data()
        st.success("✅ Datos cargados correctamente")

        query = st.text_input("🔍 Buscar en los datos:")
        if query:
            resultados = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
            st.write(f"Resultados encontrados: {len(resultados)}")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ No se pudieron cargar los datos. Error: {e}")

if __name__ == "__main__":
    main()





import streamlit as st
import pandas as pd

# Título de la app
st.set_page_config(page_title="Visor de CSV", layout="centered")
st.title("📄 Cargador y visor de archivos CSV")

# Descripción
st.write("Sube un archivo CSV para ver las primeras 10 filas del conjunto de datos.")

# Cargador de archivos
archivo_csv = st.file_uploader("Selecciona un archivo CSV", type="csv")

# Procesamiento del archivo
if archivo_csv is not None:
    try:
        # Cargar el archivo en un DataFrame
        df = pd.read_csv(archivo_csv)
        
        # Mostrar las primeras 10 filas
        st.subheader("Vista previa de los datos:")
        st.dataframe(df.head(10))
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para continuar.")


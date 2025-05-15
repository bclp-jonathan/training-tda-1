import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Visor de CSV", layout="centered")
st.title("📄 Cargador y visor de archivos CSV")

# Instrucciones
st.write("Sube un archivo CSV para ver sus dimensiones y las primeras 10 filas del conjunto de datos.")

# Cargador de archivos
archivo_csv = st.file_uploader("Selecciona un archivo CSV", type="csv")

# Procesamiento del archivo
if archivo_csv is not None:
    try:
        # Leer archivo en DataFrame
        df = pd.read_csv(archivo_csv)

        # Mostrar información de dimensiones
        num_filas, num_columnas = df.shape
        st.success(f"✅ El archivo contiene **{num_filas} filas** y **{num_columnas} columnas**.")

        # Mostrar primeras 10 filas
        st.subheader("🔍 Vista previa (primeras 10 filas):")
        st.dataframe(df.head(10))
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para continuar.")

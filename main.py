import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="CSV Analyzer - Cast Analysis", layout="centered")
st.title("🎬 Análisis de repartos en cine y TV")

st.write("Sube un archivo CSV para analizar qué actores han participado en más producciones.")

# Cargador de archivos
archivo_csv = st.file_uploader("Selecciona un archivo CSV", type="csv")

if archivo_csv is not None:
    try:
        df = pd.read_csv(archivo_csv)

        # Mostrar dimensiones
        num_filas, num_columnas = df.shape
        st.success(f"✅ El archivo contiene **{num_filas} filas** y **{num_columnas} columnas**.")

        # Vista previa
        st.subheader("🔍 Vista previa (primeras 10 filas):")
        st.dataframe(df.head(10))

        # --- Análisis de actores ---
        st.subheader("🎭 Actores con más apariciones")

        if 'cast' in df.columns:
            # Extraer y contar actores
            actores = df['cast'].dropna().astype(str).str.split(',')
            actores_flat = [actor.strip() for sublist in actores for actor in sublist]
            conteo_actores = pd.Series(actores_flat).value_counts().head(10)

            # Mostrar tabla
            st.write("Top 10 actores con más apariciones:")
            st.dataframe(conteo_actores.rename_axis("Actor").reset_index(name="Número de apariciones"))

            # Gráfico
            fig, ax = plt.subplots(figsize=(8, 5))
            conteo_actores.sort_values().plot(kind='barh', ax=ax, color='skyblue')
            ax.set_xlabel("Número de apariciones")
            ax.set_title("🎬 Top 10 actores con más apariciones")
            st.pyplot(fig)

        else:
            st.warning("El archivo debe contener una columna llamada 'cast' con los nombres de actores.")
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")

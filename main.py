import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="CSV Analyzer - Actores", layout="centered")
st.title("🎬 Análisis de actores con más apariciones")

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
        st.subheader("🎭 Top 10 actores con más apariciones")

        if 'cast' in df.columns and 'title' in df.columns:
            # Procesar nombres de actores
            actores = df['cast'].dropna().astype(str).str.split(',')
            actores_flat = [actor.strip() for sublist in actores for actor in sublist]
            conteo_actores = pd.Series(actores_flat).value_counts().head(10)

            st.write("Haz clic sobre un actor para ver en qué producciones aparece:")

            # Mostrar nombres de actores como enlaces interactivos
            for actor in conteo_actores.index:
                if st.button(actor):
                    st.subheader(f"🎥 Producciones con {actor}:")
                    mask = df['cast'].dropna().astype(str).str.contains(actor)
                    peliculas = df.loc[mask, 'title'].dropna().unique()
                    for titulo in peliculas:
                        st.markdown(f"- {titulo}")

            # Mostrar tabla y gráfico
            df_resultado = pd.DataFrame({
                "Actor": conteo_actores.index,
                "Número de apariciones": conteo_actores.values
            })
            st.dataframe(df_resultado)

            # Gráfico
            fig, ax = plt.subplots(figsize=(8, 5))
            conteo_actores.sort_values().plot(kind='barh', ax=ax, color='skyblue')
            ax.set_xlabel("Número de apariciones")
            ax.set_title("🎬 Top 10 actores con más apariciones")
            st.pyplot(fig)

        else:
            st.warning("El archivo debe contener las columnas 'cast' y 'title' para generar este análisis.")
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")

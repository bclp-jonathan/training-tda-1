import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración inicial
st.set_page_config(page_title="Análisis de Actores - Netflix", layout="centered")
st.title("🎬 Análisis de actores con más apariciones en Netflix")

st.write("Este análisis se realiza automáticamente sobre el archivo `netflix_titles.csv` en el repositorio.")

# Ruta al archivo de datos
archivo = "netflix_titles.csv"

if os.path.exists(archivo):
    try:
        df = pd.read_csv(archivo)

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

            # Mostrar nombres de actores como botones
            for actor in conteo_actores.index:
                if st.button(actor):
                    st.subheader(f"🎥 Producciones con {actor}:")
                    try:
                        mask = df['cast'].dropna().astype(str).str.contains(actor, regex=False)
                        peliculas = df.loc[mask, 'title'].dropna().unique()
                        if len(peliculas) > 0:
                            for titulo in peliculas:
                                st.markdown(f"- {titulo}")
                        else:
                            st.info("No se encontraron producciones para este actor.")
                    except Exception as e:
                        st.error(f"❌ Error al procesar la búsqueda de este actor: {e}")

            # Mostrar tabla de actores y conteo
            df_resultado = pd.DataFrame({
                "Actor": conteo_actores.index,
                "Número de apariciones": conteo_actores.values
            })
            st.dataframe(df_resultado)

            # Gráfico de barras
            fig, ax = plt.subplots(figsize=(8, 5))
            conteo_actores.sort_values().plot(kind='barh', ax=ax, color='skyblue')
            ax.set_xlabel("Número de apariciones")
            ax.set_title("🎬 Top 10 actores con más apariciones en Netflix")
            st.pyplot(fig)

        else:
            st.warning("El archivo debe contener las columnas 'cast' y 'title' para generar este análisis.")
    except Exception as e:
        st.error(f"❌ Error al leer o procesar `netflix_titles.csv`: {e}")
else:
    st.error("❌ El archivo `netflix_titles.csv` no se encontró en el repositorio.")

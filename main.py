import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="Visor de CSV con Análisis", layout="centered")
st.title("📄 Cargador y analizador de archivos CSV")

st.write("Sube un archivo CSV para visualizar los datos y responder preguntas clave sobre el contenido.")

# Cargador de archivos
archivo_csv = st.file_uploader("Selecciona un archivo CSV", type="csv")

if archivo_csv is not None:
    try:
        # Leer CSV
        df = pd.read_csv(archivo_csv)

        # Mostrar dimensiones
        num_filas, num_columnas = df.shape
        st.success(f"✅ El archivo contiene **{num_filas} filas** y **{num_columnas} columnas**.")

        # Vista previa
        st.subheader("🔍 Vista previa (primeras 10 filas):")
        st.dataframe(df.head(10))

        # --- Análisis de duraciones por género ---
        st.subheader("🎞️ Comparativa: Duración promedio por género")

        # Validar columnas necesarias
        if 'genre' in df.columns and 'duration' in df.columns:
            # Limpiar y convertir duración a numérico
            df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
            df_clean = df.dropna(subset=['genre', 'duration'])

            # Agrupar por género y calcular promedio
            top_genres = df_clean['genre'].value_counts().head(7).index.tolist()
            df_top = df_clean[df_clean['genre'].isin(top_genres)]
            df_promedios = df_top.groupby('genre')['duration'].mean().sort_values()

            # Gráfico
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=df_promedios.values, y=df_promedios.index, palette='coolwarm', ax=ax)
            ax.set_xlabel("Duración promedio (minutos)")
            ax.set_ylabel("Género")
            ax.set_title("Duración promedio por género más popular")

            st.pyplot(fig)

        else:
            st.warning("El archivo debe contener las columnas 'genre' y 'duration' para generar el gráfico.")
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")

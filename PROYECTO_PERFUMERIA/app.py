import streamlit as st
import pandas as pd
import joblib

# ==============================
# CONFIGURACION DE LA PAGINA
# ==============================
st.set_page_config(
    page_title="Perfume Price AI",
    page_icon="💎",
    layout="wide"
)

# ==============================
# DISEÑO VISUAL
# ==============================
st.markdown("""
<style>

[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
}

[data-testid="stMetricValue"] {
    color: #D4AF37 !important;
}

.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}

.main-title {
    font-size: 45px;
    font-weight: bold;
    color: #D4AF37;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #C0C0C0;
}

.card {
    background-color: #1C1F26;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #D4AF37;
}

.price {
    font-size: 40px;
    color: #D4AF37;
    font-weight: bold;
    text-align: center;
}

.stSelectbox label {
    color: #FFFFFF !important;
}

.stWidgetLabel p {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# TITULO
# ==============================
st.markdown(
    '<div class="main-title">💎 PERFUME PRICE AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Sistema inteligente de predicción de precios de perfumes</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ==============================
# INFORMACION DEL PROYECTO
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🤖 Machine Learning")
    st.write("Modelo de aprendizaje automático para estimar precios.")

with col2:
    st.markdown("### 📊 Ciencia de Datos")
    st.write("Procesamiento y análisis de datos de perfumes.")

with col3:
    st.markdown("### 💰 Predicción")
    st.write("Estimación de precios en pesos colombianos.")

st.divider()

# ==============================
# CARGAR DATOS Y MODELO
# ==============================
df = pd.read_csv("datos/datos_limpios.csv")
modelo = joblib.load("resultados/modelo_perfumes.pkl")

# Estadisticas del dataset
total_perfumes = len(df)
precio_promedio = df["precio"].mean()
precio_maximo = df["precio"].max()

st.divider()

st.markdown("## 📊 Estadísticas del dataset")

col1, col2, col3 = st.columns(3)

col1.metric("Perfumes analizados", total_perfumes)
col2.metric("Precio promedio", f"${precio_promedio:,.0f} COP")
col3.metric("Precio máximo", f"${precio_maximo:,.0f} COP")

marcas = sorted(df["marca"].unique())
categorias = sorted(df["categoria"].unique())

# ==============================
# FORMULARIO
# ==============================
st.markdown("## 🛍️ Consultar precio estimado")

st.write(
    "Selecciona la marca y la categoría del perfume "
    "para obtener una estimación mediante Machine Learning."
)

col1, col2 = st.columns(2)

with col1:
    marca = st.selectbox("🏷️ Marca del perfume", marcas)

with col2:
    categoria = st.selectbox("📂 Categoría del perfume", categorias)

st.write("")

if st.button("✨ ESTIMAR PRECIO", use_container_width=True):

    datos = pd.DataFrame({
        "marca": [marca],
        "categoria": [categoria]
    })

    prediccion = modelo.predict(datos)[0]

    st.divider()

    st.markdown("## 📈 Resultado de la predicción")

    st.markdown(
        f"""
        <div class="card">
            <p style="text-align:center;color:#C0C0C0;">
                Precio estimado
            </p>
            <div class="price">
                ${prediccion:,.0f} COP
            </div>
            <p style="text-align:center;color:#FFFFFF;">
                Marca: {marca}
            </p>
            <p style="text-align:center;color:#FFFFFF;">
                Categoría: {categoria}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Esta estimación es generada por un modelo de Machine Learning "
        "entrenado con los datos recopilados y procesados."
    )

# ==============================
# PIE DE PAGINA
# ==============================
st.divider()

st.markdown(
    """
    <p style="text-align:center;color:#888888;">
    Proyecto académico de Ciencia de Datos con Python |
    Machine Learning aplicado a la estimación de precios de perfumes
    </p>
    """,
    unsafe_allow_html=True
)
"""
✏️ Reconocimiento de Dígitos — Tema amarillo pastel
"""

import os
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ── Fix FileNotFoundError: crea la carpeta prediction si no existe ─────────────
os.makedirs("prediction", exist_ok=True)

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Reconocimiento de Dígitos",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — tema amarillo pastel
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background-color: #fffde7; color: #333333; }

[data-testid="stSidebar"] {
    background-color: #fff9c4 !important;
    border-right: 1px solid #f9a825;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f57f17 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="stSidebar"] label {
    color: #4a5568 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

h1 {
    color: #f57f17 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}
h2, h3 { color: #e65100 !important; font-weight: 600 !important; }

.stButton > button {
    background: #f9a825 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    width: 100% !important;
    transition: background 0.2s ease !important;
}
.stButton > button:hover {
    background: #f57f17 !important;
    box-shadow: 0 2px 12px rgba(249,168,37,0.35) !important;
}

[data-testid="metric-container"] {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-top: 3px solid #f9a825;
    border-radius: 8px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(249,168,37,0.1);
}
[data-testid="metric-container"] label {
    color: #f57f17 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #333333 !important;
    font-weight: 700 !important;
    font-size: 1.55rem !important;
}

.header-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-left: 5px solid #f9a825;
    border-radius: 8px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 1px 6px rgba(249,168,37,0.12);
}

.result-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-left: 5px solid #f9a825;
    border-radius: 8px;
    padding: 24px 32px;
    margin-top: 20px;
    text-align: center;
}

.result-digit {
    font-size: 5rem;
    font-weight: 700;
    color: #f57f17;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}

.info-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: #fffde7;
    border: 1px solid #ffe082;
    border-radius: 6px;
    margin-bottom: 8px;
}

hr { border-color: #ffe082 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIÓN DE PREDICCIÓN
# ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    return tf.keras.models.load_model("model/handwritten.h5")

def predictDigit(image):
    model      = cargar_modelo()
    image      = ImageOps.grayscale(image)
    img        = image.resize((28, 28))
    img        = np.array(img, dtype='float32') / 255
    img        = img.reshape((1, 28, 28, 1))
    pred       = model.predict(img)
    result     = np.argmax(pred[0])
    confidence = float(pred[0][result]) * 100
    return result, confidence

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✏️ Reconocimiento de Dígitos")
    st.divider()

    st.markdown("### PROPIEDADES DEL TABLERO")

    st.markdown("#### Dimensiones")
    canvas_width  = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero",  200, 600, 300, 50)

    st.markdown("#### Herramienta")
    drawing_mode = st.selectbox(
        "Herramienta de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    st.markdown("#### Estilo")
    stroke_width = st.slider("Ancho de línea", 1, 30, 15)
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")
    bg_color     = st.color_picker("Color de fondo", "#000000")

    st.divider()
    st.markdown("### ACERCA DE")
    st.markdown("""
    <p style="color:#6b7280; font-size:0.85rem; line-height:1.7;">
    Esta aplicación evalúa la capacidad de una <strong>Red Neuronal Artificial</strong>
    para reconocer dígitos escritos a mano.<br><br>
    Basado en el desarrollo de <em>Vinay Uniyal</em>.
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">✏️ Reconocimiento de Dígitos escritos a mano</h1>
    <p style="margin:6px 0 0 0; color:#f57f17; font-size:0.97rem;">
        Dibuja un dígito en el tablero y presiona <strong>Predecir</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL — dos columnas
# ─────────────────────────────────────────────
col_canvas, col_resultado = st.columns([3, 2], gap="large")

with col_canvas:
    st.markdown("### 🎨 Tablero de dibujo")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"canvas_{canvas_width}_{canvas_height}",
    )
    predecir = st.button("🔍 Predecir dígito", use_container_width=True)

with col_resultado:
    st.markdown("### 📊 Resultado")

    if not predecir:
        for icono, titulo, desc in [
            ("✏️", "Dibuja",    "Traza un dígito del 0 al 9 en el tablero."),
            ("⚙️", "Configura", "Ajusta trazo y colores en el panel lateral."),
            ("🔍", "Predice",   "Pulsa 'Predecir dígito' para ver el resultado."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.3rem;">{icono}</span>'
                f'<div><strong style="color:#e65100;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; color:#6b7280; font-size:0.88rem;">{desc}</p>'
                f'</div></div>', unsafe_allow_html=True)

    if predecir:
        if canvas_result.image_data is not None:
            with st.spinner("Analizando imagen..."):
                input_numpy_array = np.array(canvas_result.image_data)
                input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
                img_path = os.path.join("prediction", "img.png")
                input_image.save(img_path)
                img = Image.open(img_path)
                res, confidence = predictDigit(img)

            st.markdown(f"""
            <div class="result-card">
                <p style="color:#f57f17; font-weight:600; font-size:0.9rem;
                          text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
                    Dígito reconocido
                </p>
                <div class="result-digit">{res}</div>
                <p style="color:#6b7280; font-size:0.9rem; margin-top:12px;">
                    Confianza: <strong style="color:#f57f17;">{confidence:.1f}%</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.metric("🏆 Dígito",    str(res))
            c2.metric("📈 Confianza", f"{confidence:.1f}%")
        else:
            st.warning("⚠️ Por favor dibuja un dígito en el tablero antes de predecir.")

plt.close("all")

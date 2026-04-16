"""
🎨 Tablero para Dibujo — Tema amarillo pastel
"""

import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tablero para Dibujo",
    page_icon="🎨",
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

.header-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-left: 5px solid #f9a825;
    border-radius: 8px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 1px 6px rgba(249,168,37,0.12);
}

.canvas-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-radius: 8px;
    padding: 20px 24px;
    box-shadow: 0 1px 6px rgba(249,168,37,0.1);
}

hr { border-color: #ffe082 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — propiedades configurables
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎨 Tablero para Dibujo")
    st.divider()

    st.markdown("### PROPIEDADES DEL TABLERO")

    st.markdown("#### Dimensiones del Tablero")
    canvas_width  = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero",  200, 600, 300, 50)

    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)

    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")
    bg_color     = st.color_picker("Color de fondo", "#000000")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">🎨 Tablero para dibujo</h1>
    <p style="margin:6px 0 0 0; color:#f57f17; font-size:0.97rem;">
        Configura las propiedades del tablero en el panel lateral
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CANVAS
# ─────────────────────────────────────────────
st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

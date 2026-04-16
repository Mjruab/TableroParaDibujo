import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ── Función de predicción ──────────────────────────────────────────────────────
def predictDigit(image):
    model = tf.keras.models.load_model("model/handwritten.h5")
    image = ImageOps.grayscale(image)
    img = image.resize((28, 28))
    img = np.array(img, dtype='float32')
    img = img / 255
    img = img.reshape((1, 28, 28, 1))
    pred = model.predict(img)
    result = np.argmax(pred[0])
    return result

# ── Configuración de la página ─────────────────────────────────────────────────
st.set_page_config(
    page_title='Reconocimiento de Dígitos escritos a mano',
    layout='wide'
)

st.title('Reconocimiento de Dígitos escritos a mano')
st.subheader("Dibuja el dígito en el panel y presiona 'Predecir'")

# ── Sidebar: propiedades configurables del tablero ─────────────────────────────
with st.sidebar:
    st.subheader("Propiedades del Tablero")

    # Dimensiones del tablero
    st.subheader("Dimensiones del Tablero")
    canvas_width  = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero",  200, 600, 300, 50)

    # Herramienta de dibujo
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Ancho de línea
    stroke_width = st.slider('Selecciona el ancho de línea', 1, 30, 15)

    # Colores
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")
    bg_color     = st.color_picker("Color de fondo", "#000000")

    st.divider()
    st.title("Acerca de:")
    st.text("En esta aplicación se evalúa")
    st.text("la capacidad de un RNA de reconocer")
    st.text("dígitos escritos a mano.")
    st.text("Basado en desarrollo de Vinay Uniyal")

# ── Canvas ─────────────────────────────────────────────────────────────────────
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",   # clave dinámica
)

# ── Botón de predicción ────────────────────────────────────────────────────────
if st.button('Predecir'):
    if canvas_result.image_data is not None:
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('prediction/img.png')
        img = Image.open("prediction/img.png")
        res = predictDigit(img)
        st.header('El Dígito es: ' + str(res))
    else:
        st.header('Por favor dibuja en el canvas el dígito.')

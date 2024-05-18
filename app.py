import streamlit as st
from stvoice import my_component

# Título de la aplicación
st.title("Aplicación de Transcripción de Voz")

# Instrucciones
st.write("""
    Presiona el botón de abajo para activar el micrófono. Habla y tu voz será convertida a texto.
""")

# Insertar el componente personalizado
transcription = my_component(name="Transcriptor de Voz")

# Mostrar la transcripción
if transcription:
    st.write("Texto transcrito:")
    st.write(transcription)

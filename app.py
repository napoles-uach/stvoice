import streamlit as st
from streamlit_voice import voice

# Título de la aplicación
st.title("Aplicación de Transcripción de Voz")

# Instrucciones
st.write("""
    Presiona el botón de abajo para activar el micrófono. Habla y tu voz será convertida a texto.
""")

# Insertar el componente personalizado
transcription = voice(name="Transcriptor de Voz")

# Mostrar la transcripción si está disponible
if transcription:
    st.write("Texto transcrito:")
    st.write(transcription)

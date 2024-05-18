import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os

st.title("Aplicación de Transcripción de Voz")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)
    audio.export("temp.wav", format="wav")
    
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

# Función para manejar el procesamiento del audio
def audio_receiver_factory():
    def audio_receiver(audio_data):
        # Guardar el audio recibido
        audio_data = audio_data.tobytes()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wf:
            wf.write(audio_data)
            wf.flush()
            audio_path = wf.name
        
        # Transcribir el audio
        transcription = transcribe_audio(audio_path)
        st.session_state.transcription = transcription
        
        # Eliminar archivos temporales
        os.remove(audio_path)
        os.remove("temp.wav")

    return audio_receiver

# Configuración del receptor de audio
try:
    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"audio": True, "video": False},
        ),
        audio_receiver_factory=audio_receiver_factory,
        async_processing=True,
    )

    # Mostrar la transcripción si está disponible
    if 'transcription' in st.session_state:
        st.write("Texto transcrito:")
        st.write(st.session_state.transcription)

except TypeError as e:
    st.error(f"Error en la aplicación: {str(e)}")

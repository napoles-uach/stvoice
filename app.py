import streamlit as st
from twilio.rest import Client
from pydub import AudioSegment
import speech_recognition as sr
import os

# Leer credenciales de Twilio desde secrets
ACCOUNT_SID = st.secrets["twilio"]["account_sid"]
AUTH_TOKEN = st.secrets["twilio"]["auth_token"]
TWILIO_PHONE_NUMBER = st.secrets["twilio"]["phone_number"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(message, to):
    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to)

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)
    audio.export("temp.wav", format="wav")
    
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

st.title("Aplicación de Transcripción de Voz")

if 'audio_file' not in st.session_state:
    st.session_state['audio_file'] = None

uploaded_file = st.file_uploader("Sube un archivo de audio", type=["wav", "mp3"])

if uploaded_file:
    st.session_state['audio_file'] = uploaded_file
    st.audio(uploaded_file)

if st.session_state['audio_file']:
    file_path = f"uploaded_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Transcribiendo audio...")
    transcription = transcribe_audio(file_path)
    st.write("Texto transcrito:")
    st.write(transcription)
    
    os.remove(file_path)
    os.remove("temp.wav")

    recipient_number = st.text_input("Número de teléfono para enviar la transcripción:")
    if st.button("Enviar SMS"):
        send_sms(transcription, recipient_number)
        st.success("Transcripción enviada exitosamente.")


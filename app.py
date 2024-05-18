import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import pydub
import speech_recognition as sr
import tempfile
import os
from collections import deque
import threading

def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.
    """
    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)
    token = client.tokens.create()
    return token.ice_servers

st.title("Aplicación de Transcripción de Voz")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

frames_deque_lock = threading.Lock()
frames_deque: deque = deque([])

def queued_audio_frames_callback(frames: List[av.AudioFrame]) -> av.AudioFrame:
    with frames_deque_lock:
        frames_deque.extend(frames)

    # Return empty frames to be silent.
    new_frames = []
    for frame in frames:
        input_array = frame.to_ndarray()
        new_frame = av.AudioFrame.from_ndarray(
            np.zeros(input_array.shape, dtype=input_array.dtype),
            layout=frame.layout.name,
        )
        new_frame.sample_rate = frame.sample_rate
        new_frames.append(new_frame)

    return new_frames

# Configuración del receptor de audio
webrtc_ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    queued_audio_frames_callback=queued_audio_frames_callback,
    rtc_configuration={"iceServers": get_ice_servers()},
    media_stream_constraints={"audio": True, "video": False},
)

status_indicator = st.empty()

if not webrtc_ctx.state.playing:
    st.write("Inicie la grabación para empezar.")
else:
    status_indicator.write("Grabando audio...")

    if len(frames_deque) > 0:
        audio_frames = []
        with frames_deque_lock:
            while len(frames_deque) > 0:
                frame = frames_deque.popleft()
                audio_frames.append(frame)

        sound_chunk = pydub.AudioSegment.empty()
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound

        if len(sound_chunk) > 0:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sound_chunk.export(f.name, format="wav")
                audio_file = f.name

            st.write("Transcribiendo audio...")
            transcription = transcribe_audio(audio_file)
            st.write("Texto transcrito:")
            st.write(transcription)

            # Eliminar archivos temporales
            os.remove(audio_file)

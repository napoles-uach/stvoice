import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io
import base64

st.title("Speech to Text App")

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

# JavaScript to record audio
st.markdown("""
<script>
var my_div = document.createElement('div');
my_div.innerHTML = '<button id="record" type="button">Start Recording</button>';
document.body.appendChild(my_div);

var record = document.getElementById('record');

record.onclick = function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = function() {
                const base64String = reader.result;
                const audio = new Audio(base64String);
                audio.play();
                var my_audio = base64String.split(",")[1];
                var my_input = document.createElement('input');
                my_input.type = 'hidden';
                my_input.id = 'my_audio';
                my_input.value = my_audio;
                document.body.appendChild(my_input);
                var my_form = document.createElement('form');
                my_form.method = 'post';
                my_form.action = '/audio';
                var my_submit = document.createElement('input');
                my_submit.type = 'submit';
                my_form.appendChild(my_submit);
                document.body.appendChild(my_form);
                my_submit.click();
            };
        });

        setTimeout(() => {
            mediaRecorder.stop();
        }, 3000);
    });
}
</script>
""", unsafe_allow_html=True)

st.markdown("""
<form method="post" action="/audio">
    <input type="hidden" id="my_audio" name="my_audio">
    <button type="submit">Submit</button>
</form>
""", unsafe_allow_html=True)

# Handle the audio file submission
if st.experimental_get_query_params():
    my_audio = st.experimental_get_query_params().get("my_audio", None)
    if my_audio:
        audio_data = base64.b64decode(my_audio[0])
        audio_file = io.BytesIO(audio_data)
        text = audio_to_text(audio_file)
        st.write("Transcribed Text:", text)

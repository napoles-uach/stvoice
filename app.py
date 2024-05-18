import streamlit as st
import streamlit.components.v1 as components

# Título de la aplicación
st.title("Aplicación de Transcripción de Voz")

# Instrucciones
st.write("""
    Presiona el botón de abajo para activar el micrófono. Habla y tu voz será convertida a texto.
""")

# Insertar el componente personalizado
components.html("""
<!DOCTYPE html>
<html>
<head>
    <title>Transcripción de Voz</title>
</head>
<body>
    <h2>Presiona el botón y habla:</h2>
    <button onclick="startDictation()">Iniciar</button>
    <p id="result"></p>
    <script>
        function startDictation() {
            if (window.hasOwnProperty('webkitSpeechRecognition')) {
                var recognition = new webkitSpeechRecognition();

                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.lang = "en-US";
                recognition.start();

                recognition.onresult = function(e) {
                    document.getElementById('result').innerHTML = e.results[0][0].transcript;
                    sendToStreamlit(e.results[0][0].transcript);
                    recognition.stop();
                };

                recognition.onerror = function(e) {
                    recognition.stop();
                }
            }
        }

        function sendToStreamlit(text) {
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = 'data:text/plain,' + encodeURIComponent(text);
            document.body.appendChild(iframe);

            iframe.onload = function() {
                setTimeout(function() {
                    iframe.remove();
                }, 1000);
            };
        }
    </script>
</body>
</html>
""", height=300)

# Capturar el resultado de JavaScript y mostrarlo en Streamlit
if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""

if st.button("Actualizar Transcripción"):
    st.session_state["transcript"] = st.experimental_get_query_params().get("text", [""])[0]

st.write("Texto transcrito:")
st.write(st.session_state["transcript"])

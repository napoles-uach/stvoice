import streamlit as st
import streamlit.components.v1 as components

# Título de la aplicación
st.title("Aplicación de Transcripción de Voz")

# Instrucciones
st.write("""
    Presiona el botón de abajo para activar el micrófono. Habla y tu voz será convertida a texto.
""")

# Definir el contenido HTML con JavaScript para la transcripción de voz
_COMPONENT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
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

                recognition.lang = "es-ES";
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
"""

# Insertar el contenido HTML en la aplicación de Streamlit
components.html(_COMPONENT_HTML, height=300)

# Capturar la transcripción desde los parámetros de URL
transcription = st.experimental_get_query_params().get("text", [""])[0]

# Mostrar la transcripción si está disponible
if transcription:
    st.write("Texto transcrito:")
    st.write(transcription)
    # Aquí puedes añadir el procesamiento adicional del texto
    processed_text = transcription.upper()  # Ejemplo de procesamiento: convertir a mayúsculas
    st.write("Texto procesado:")
    st.write(processed_text)


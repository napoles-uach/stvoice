import streamlit as st
import replicate
import os
from transformers import AutoTokenizer
from streamlit_mic_recorder import mic_recorder, speech_to_text
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Arctic avatar",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Avatar animation function
def avatar(text='', lang='en-US'):
    try:
        texto_usuario = text

        # Generación de los keyframes para la animación CSS.
        keyframes_waiting = """
            0% { background-image: url('https://raw.githubusercontent.com/napoles-uach/streamlit_avatar/main/artic_1.png'); }
            50% { background-image: url('https://raw.githubusercontent.com/napoles-uach/streamlit_avatar/main/artic_1.png'); }
            100% { background-image: url('https://raw.githubusercontent.com/napoles-uach/streamlit_avatar/main/artic_closed_eyes.png'); }
        """

        keyframes_speaking = "".join([f"{i*10}% {{background-image: url('https://raw.githubusercontent.com/napoles-uach/streamlit_avatar/main/artic_{i%9 + 1}.png');}}\n" for i in range(10)])

        # Construcción del HTML para el avatar animado.
        html_str = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Animated Speaking Avatar</title>
            <style>
                body {{
                    background: white;
                    color: black;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    overflow: hidden;
                }}
                .avatar {{
                    width: 600px;
                    height: 600px;
                    background-size: cover;
                    background-image: url('https://raw.githubusercontent.com/napoles-uach/streamlit_avatar/main/artic_1.png'); /* Imagen de fondo predeterminada */
                    animation: waitingAnimation 3s steps(2, end) infinite; /* Duración ajustada */
                    z-index: 1;
                }}
                @keyframes waitingAnimation {{
                    {keyframes_waiting}
                }}
                @keyframes speakAnimation {{
                    {keyframes_speaking}
                }}
                .snowflake {{
                    position: absolute;
                    top: -1px;
                    width: 10px;
                    height: 10px;
                    background: white;
                    border-radius: 50%;
                    opacity: 0.8;
                    animation: fall linear infinite;
                    z-index: 2;
                }}
                @keyframes fall {{
                    0% {{ transform: translateY(0); opacity: 0.8; }}
                    100% {{ transform: translateY(100vh); opacity: 0.2; }}
                }}
            </style>
        </head>
        <body>
            <div id="snowflakes"></div>
            <div class="avatar" id="avatar"></div>
            <script>
                document.addEventListener('DOMContentLoaded', (event) => {{
                    var avatar = document.getElementById("avatar");

                    function setAnimation(animationName, duration, steps) {{
                        avatar.style.animation = 'none'; // Detener la animación actual
                        void avatar.offsetWidth; // Reiniciar el flujo de CSS
                        avatar.style.animation = `${{animationName}} ${{duration}}s steps(${{steps}}, end) infinite`;
                    }}

                    var texto = `{texto_usuario}`;
                    var utterance = new SpeechSynthesisUtterance(texto);
                    utterance.lang = "{lang}"; // Configurar el idioma deseado
                    utterance.onstart = function(event) {{
                        var duration = Math.max(texto.length / 50, 2);  // Duración basada en la longitud del texto
                        setAnimation('speakAnimation', duration, 10);
                    }};
                    utterance.onend = function(event) {{
                        setTimeout(() => {{ setAnimation('waitingAnimation', 3, 2); }}, 500);  // Transición más lenta a la animación de espera
                    }};
                    speechSynthesis.speak(utterance);

                    // Crear copos de nieve
                    function createSnowflake() {{
                        var snowflake = document.createElement("div");
                        snowflake.classList.add("snowflake");
                        snowflake.style.left = Math.random() * 100 + "vw";
                        snowflake.style.animationDuration = (Math.random() * 5 + 5) + "s";
                        snowflake.style.width = (Math.random() * 5 + 5) + "px";
                        snowflake.style.height = snowflake.style.width;
                        document.getElementById("snowflakes").appendChild(snowflake);

                        // Eliminar copo de nieve después de que caiga
                        setTimeout(() => {{
                            snowflake.remove();
                        }}, parseFloat(snowflake.style.animationDuration) * 1000);
                    }}

                    // Crear múltiples copos de nieve
                    setInterval(createSnowflake, 200);
                }});
            </script>
        </body>
        </html>
        """

        # Renderizar el HTML en Streamlit
        components.html(html_str, height=600)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Set assistant icon to Snowflake logo
icons = {"assistant": "./Snowflake_Logomark_blue.svg", "user": "⛷️"}

# App title
#st.set_page_config(page_title="Snowflake Arctic")

# Replicate Credentials
with st.sidebar:
    st.title('Arctic avatar with voice 🗣️')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your Replicate API token.', icon='⚠️')
            st.markdown("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")

    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    st.subheader("Adjust model parameters")
    with st.expander('Model Parameters'):
        temperature = st.slider('temperature', min_value=0.01, max_value=5.0, value=0.3, step=0.01)
        top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    
    st.subheader("Voice Input")
    #mic = mic_recorder(key="mic_input")
    voice_prompt = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')
    if voice_prompt:
        st.session_state.voice_prompt = voice_prompt

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]

# Display or clear chat messages
#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]

st.sidebar.button('Clear chat history', on_click=clear_chat_history)
#st.sidebar.caption('Built by [Snowflake](https://snowflake.com/) to demonstrate [Snowflake Arctic](https://www.snowflake.com/blog/arctic-open-and-efficient-foundation-language-models-snowflake). App hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Model hosted by [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct).')
#st.sidebar.caption('Build your own app powered by Arctic and [enter to win](https://arctic-streamlit-hackathon.devpost.com/) $10k in prizes.')

@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text to the model."""
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)

# Function for generating Snowflake Arctic response
def generate_arctic_response():
    prompt = []
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("user\n" + dict_message["content"] + "")
        else:
            prompt.append("assistant\n" + dict_message["content"] + "")
    
    prompt.append("assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.button('Clear chat history', on_click=clear_chat_history, key="clear_chat_history")
        st.stop()

    response = ""
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                                  input={"prompt": prompt_str,
                                         "prompt_template": r"Be brief in the following request and use no more than 20 words:, {prompt}",
                                         "temperature": temperature,
                                         "top_p": top_p,
                                         "max_new_tokens": 50,
                                         }):
        response += str(event)
        yield str(event)
    return response

# User-provided prompt via chat input or voice
#st.header("Chat with Snowflake Arctic")
#text_prompt = st.chat_input(disabled=not replicate_api, key="text_input")

#if text_prompt or st.session_state.get("voice_prompt"):
#    user_prompt = text_prompt if text_prompt else st.session_state.pop("voice_prompt", "")
        
#    st.session_state.messages.append({"role": "user", "content": user_prompt})
#    with st.chat_message("user", avatar="⛷️"):
#        st.write(user_prompt)

#    if st.session_state.messages[-1]["role"] != "assistant":
#        with st.chat_message("assistant"):
#            response_stream = generate_arctic_response()
#            full_response = ''.join(response_stream)
#            avatar(full_response)
#            st.write(full_response)
#        st.session_state.messages.append({"role": "assistant", "content": full_response})

# User-provided prompt via chat input or voice
#st.header("Chat with Snowflake Arctic")
text_prompt = st.chat_input(disabled=not replicate_api, key="text_input")

if text_prompt or st.session_state.get("voice_prompt"):
    user_prompt = text_prompt if text_prompt else st.session_state.pop("voice_prompt", "")
        
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if st.session_state.messages[-1]["role"] != "assistant":
        response_stream = generate_arctic_response()
        full_response = ''.join(response_stream)
        avatar(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    avatar()

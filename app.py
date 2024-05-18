
#import streamlit as st
#from streamlit_mic_recorder import mic_recorder, speech_to_text
#from streamlit_avatar import avatar

#lang = "en-EN"



#state = st.session_state

#if 'text_received' not in state:
#    state.text_received = []

#c1, c2 = st.columns(2)
#with c1:
#    st.write("Convert speech to text:")
#with c2:
#    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

#if text:
#    state.text_received.append(text)
#    #text = st.chat_input("Say something",key=0)
#    avatar(text)

#for text in state.text_received:
#    st.text(text)


import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text
from streamlit_avatar import avatar
import replicate

lang = "en-EN"
state = st.session_state

if 'text_received' not in state:
    state.text_received = []
if 'llm_response' not in state:
    state.llm_response = ""

# Columnas para interfaz
c1, c2 = st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

# Procesar el texto recibido
if text:
    state.text_received.append(text)
    avatar(text)  # Mostrar el avatar diciendo lo que acabas de decir

    # Enviar el texto al LLM
    input = {
        "prompt": text,
        "temperature": 0.2
    }
    
    llm_response = ""
    try:
        for event in replicate.stream(
            "snowflake/snowflake-arctic-instruct",
            input=input
        ):
            llm_response += event.get('text', '')
    except Exception as e:
        st.error(f"Error interacting with LLM: {e}")
    
    state.llm_response = llm_response

# Mostrar el texto recibido y la respuesta del LLM
st.write("Tus frases:")
for text in state.text_received:
    st.text(text)

st.write("Respuesta del LLM:")
st.text(state.llm_response)

# Mostrar el avatar diciendo la respuesta del LLM
if state.llm_response:
    avatar(state.llm_response, lang=lang)

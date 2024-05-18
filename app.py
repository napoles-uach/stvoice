
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
import replicate
import json

def stream_llm_responses(prompt_str, temperature=0.7, top_p=0.9):
    responses = []
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                                  input={"prompt": prompt_str,
                                         "prompt_template": r"{prompt}",
                                         "temperature": temperature,
                                         "top_p": top_p,
                                         }):
        responses.append(str(event))
    return ' '.join(responses)

# Uso de la función
prompt = "Write a joke"
response = stream_llm_responses(prompt)
st.write(response)

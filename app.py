
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
from streamlit_mic_recorder import speech_to_text
from streamlit_avatar import avatar
import replicate
import json

import replicate

input = {
    "prompt": "write a joke",
    "temperature": 0.2
}


output=replicate.stream(
    "snowflake/snowflake-arctic-instruct",
    input=input
)
ans=[]
for event in replicate.stream(
    "snowflake/snowflake-arctic-instruct",
    input=input
):
    st.text(event)#, end="")
    ans.append(str(event))
st.write(ans)
##=> "Fizz Buzz is a common programming problem that involves ...

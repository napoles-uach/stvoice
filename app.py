
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


import os
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from streamlit_avatar import avatar
from transformers import AutoTokenizer
import replicate

def main():
    """Execution starts here."""
    if not get_replicate_api_token():
        st.error("Missing Replicate API token. Please set it in Streamlit secrets.")
        return

    display_sidebar_ui()
    init_chat_history()
    display_chat_messages()
    get_and_process_prompt()

def get_replicate_api_token():
    try:
        os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_API_TOKEN']
        return True
    except KeyError:
        return False

def display_sidebar_ui():
    with st.sidebar:
        st.title('Snowflake Arctic')
        st.subheader("Adjust model parameters")
        st.slider('temperature', min_value=0.01, max_value=5.0, value=0.3,
                                step=0.01, key="temperature")
        st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01,
                          key="top_p")

        st.button('Clear chat history', on_click=clear_chat_history)

        st.sidebar.caption('Build your own app powered by Arctic and [enter to win](https://arctic-streamlit-hackathon.devpost.com/) $10k in prizes.')

        st.subheader("About")
        st.caption('Built by [Snowflake](https://snowflake.com/) to demonstrate [Snowflake Arctic](https://www.snowflake.com/blog/arctic-open-and-efficient-foundation-language-models-snowflake). App hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Model hosted by [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct).')

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]
    st.session_state.chat_aborted = False

def init_chat_history():
    """Create a st.session_state.messages list to store chat messages"""
    if "messages" not in st.session_state:
        clear_chat_history()

def display_chat_messages():
    # Set assistant icon to Snowflake logo
    icons = {"assistant": "./Snowflake_Logomark_blue.svg", "user": "⛷️"}

    # Display the messages
    for message in st.session_state.messages:
        avatar_path = icons.get(message["role"], None)
        if avatar_path:
            with st.chat_message(message["role"], avatar=avatar_path):
                st.write(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])

@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text
    text to the Model. Eventually we will replace this with ArcticTokenizer
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def check_safety(disable=False) -> bool: 
    # Disabled for now due to unavailability of LlamaGuard deployment
    return True

def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)

def abort_chat(error_message: str):
    """Display an error message requiring the chat to be cleared. 
    Forces a rerun of the app."""
    assert error_message, "Error message must be provided."
    error_message = f":red[{error_message}]"
    if st.session_state.messages[-1]["role"] != "assistant":
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        st.session_state.messages[-1]["content"] = error_message
    st.session_state.chat_aborted = True
    st.rerun()

def get_and_process_prompt():
    """Get the user prompt and process it"""
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="./Snowflake_Logomark_blue.svg"):
            response = generate_arctic_response()
            st.write(response)
            avatar(response)  # Hacer que el avatar hable la respuesta

    if st.session_state.chat_aborted:
        st.button('Reset chat', on_click=clear_chat_history, key="clear_chat_history")
        st.chat_input(disabled=True)
    elif prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

def generate_arctic_response():
    """String generator for the Snowflake Arctic response."""
    prompt = []
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("user\n" + dict_message["content"] + "")
        else:
            prompt.append("assistant\n" + dict_message["content"] + "")
    
    prompt.append("assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)

    num_tokens = get_num_tokens(prompt_str)
    max_tokens = 1500
    
    if num_tokens >= max_tokens:
        abort_chat(f"Conversation length too long. Please keep it under {max_tokens} tokens.")
    
    st.session_state.messages.append({"role": "assistant", "content": ""})
    for event_index, event in enumerate(replicate.stream("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}",
                                  "temperature": st.session_state.temperature,
                                  "top_p": st.session_state.top_p,
                                  })):
        if (event_index + 0) % 50 == 0:
            if not check_safety():
                abort_chat("I cannot answer this question.")
        st.session_state.messages[-1]["content"] += str(event)
        yield str(event)

    # Final safety check...
    if not check_safety():
        abort_chat("I cannot answer this question.")

if __name__ == "__main__":
    state = st.session_state

    if 'text_received' not in state:
        state.text_received = []

    c1, c2 = st.columns(2)
    with c1:
        st.write("Convert speech to text:")
    with c2:
        text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

    if text:
        state.text_received.append(text)
        st.session_state.messages.append({"role": "user", "content": text})
        st.rerun()

    for text in state.text_received:
        st.text(text)

    main()

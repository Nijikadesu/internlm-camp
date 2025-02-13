import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
api_key = os.getenv("internlm_api_key")
model="internlm2.5-latest"

client = OpenAI(api_key=api_key, base_url=base_url)

st.set_page_config(page_title="llama_index_demo", page_icon="🦜🔗")
st.title("llama_index_demo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])

def response_gernerator(msg):
    response = client.chat.completions.create(
        model=model,
        messages=[msg]
    )

    return response.choices[0].message.content

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    user_msg = {"role": "user", "content": prompt}

    st.session_state.messages.append(user_msg)

    response = response_gernerator(user_msg)

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

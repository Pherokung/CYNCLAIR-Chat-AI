import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.embeddings import OpenAIEmbeddings

from functions.ensemble import ensemble_retriever_from_docs
from functions.full_chain import create_full_chain, ask_question
from functions.loader import load_md_files
from functions.default_sidebar import default_sidebar

from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
)
page_name = "Chatbot"
default_sidebar(page_name)

st.title("CVE Chatbot 🤖")

load_dotenv()


def show_ui(qa, prompt_to_user="How may I help you?"):
    

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "AI", "content": prompt_to_user}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "User", "content": prompt})
        with st.chat_message("User"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "AI":
        with st.chat_message("AI"):
            with st.spinner("Thinking..."):
                response = ask_question(qa, prompt)
                st.markdown(response.content)
        message = {"role": "AI", "content": response.content}
        st.session_state.messages.append(message)


@st.cache_resource
def get_retriever(openai_api_key=None):
    docs = load_md_files()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
    return ensemble_retriever_from_docs(docs, embeddings=embeddings)


def get_chain(openai_api_key=None, huggingfacehub_api_token=None):
    ensemble_retriever = get_retriever(openai_api_key=openai_api_key)
    chain = create_full_chain(ensemble_retriever,
                              openai_api_key=openai_api_key,
                              chat_memory=StreamlitChatMessageHistory(key="langchain_messages"))
    return chain


def run():
    ready = True

    openai_api_key = st.session_state.get("OPENAI_API_KEY")
    huggingfacehub_api_token = st.session_state.get("HUGGINGFACEHUB_API_TOKEN")

    with st.sidebar:
        if not openai_api_key:
            openai_api_key = os.environ['OPENAI_API_KEY']
        if not huggingfacehub_api_token:
            huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

    if not openai_api_key:
        st.warning("Missing OPENAI_API_KEY")
        ready = False
    if not huggingfacehub_api_token:
        st.warning("Missing HUGGINGFACEHUB_API_TOKEN")
        ready = False

    if ready:
        chain = get_chain(openai_api_key=openai_api_key, huggingfacehub_api_token=huggingfacehub_api_token)
        st.subheader("Suggestion Questions (You can copy the questions)")
        st.code("Hello!, What can you do for me", language='markdown')
        st.code("We found evidence of a website breach involving SQL injection \non a PHP website. Are there any related CVE incidents?", language='markdown')
        st.code("Give me some details about CVE-2023-7110", language='markdown')
        st.code("What is the publish and last update date of that CVE?", language='markdown')
        
        
        show_ui(chain, "What would you like to know?")
    else:
        st.stop()

def Report():
    text = "under construction"
    st.markdown(text)

run()
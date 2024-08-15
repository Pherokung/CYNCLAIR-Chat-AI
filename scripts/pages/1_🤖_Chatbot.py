import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.embeddings import OpenAIEmbeddings

from ensemble import ensemble_retriever_from_docs
from full_chain import create_full_chain, ask_question
from loader import load_md_files
from loader import list_md_files

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
)
st.title("CVE Chatbot 🤖")

load_dotenv()


def show_ui(qa, prompt_to_user="How may I help you?"):
    

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "AI", "content": prompt_to_user}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["role"] + ": " + message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "User", "content": prompt})
        with st.chat_message("User"):
            st.write("User" + ": " + prompt)

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
        st.subheader("Ask me questions about CVE Database")
        show_ui(chain, "What would you like to know?")
    else:
        st.stop()

def Report():
    text = "under construction"
    st.markdown(text)

run()
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.embeddings import OpenAIEmbeddings

from functions.ensemble import ensemble_retriever_from_docs
from functions.full_chain import create_full_chain, ask_question
from functions.loader import load_md_files

st.set_page_config(page_title="Report", page_icon="📝")

st.markdown("# Report")

load_dotenv()


def show_ui(qa, prompt_to_user="I can provide a report outline if you give me the chat history."):
    with st.chat_message("AI"):
        st.write("AI: " + prompt_to_user)
    
    with st.chat_message("AI"):
        with st.spinner("Thinking..."):
            prompt = "Show me the report outline in the template provided"
            response = ask_question(qa, prompt)
            st.write("AI: " + response.content)

@st.cache_resource
def get_retriever(openai_api_key=None):
    docs = load_md_files() 
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
    return ensemble_retriever_from_docs(docs, embeddings=embeddings)


def get_chain(openai_api_key=None, huggingfacehub_api_token=None):
    ensemble_retriever = get_retriever(openai_api_key=openai_api_key)
    chain = create_full_chain(ensemble_retriever,
                              openai_api_key=openai_api_key,
                              chat_memory=StreamlitChatMessageHistory(key="langchain_messages"),
                              mode="Reportbot")
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
        st.subheader("I can provide a report outline based on the chat history.")
        show_ui(chain, "I recieved the chat history. I am writing the report.")
    else:
        st.stop()

run()
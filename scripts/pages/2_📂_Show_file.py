import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.embeddings import OpenAIEmbeddings

from ensemble import ensemble_retriever_from_docs
from full_chain import create_full_chain, ask_question
from loader import load_md_files
from loader import list_md_files

st.set_page_config(page_title="Database", page_icon="📂")

st.markdown("# Show Files")
#st.sidebar.header("Show Files")
st.write(
    """This demo shows files that exist in the database"""
)

def show_file():
    paths = list(list_md_files())

    file_path = st.selectbox("Select a data file to view", paths, index=None)

    if file_path:
        with open(file_path,"r") as f:
            md_content = f.read()
            st.markdown(md_content)

show_file()
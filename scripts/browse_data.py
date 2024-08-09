import streamlit as st

from loader import list_md_files

paths = list(list_md_files())

file_path = st.selectbox("Select a data file to view", paths, index=None)

if file_path:
    with open(file_path,"r") as f:
        md_content = f.read()
        st.markdown(md_content)
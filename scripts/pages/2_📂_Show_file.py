import streamlit as st

from functions.loader import list_md_files

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
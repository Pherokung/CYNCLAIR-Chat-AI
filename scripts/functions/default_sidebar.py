import streamlit as st

def default_sidebar(page_name):
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap: 10px;">
            <img src="https://podsawee.com/cygentic_logo.png" style="width: 50px;">
            <h1>Cygentic</h1>
        </div>
        <div style="text-align: center;">
            <h4>Page: {page_name}</h4>
            <hr>
            <p><strong>Developed By</strong>: GMFAI Team</p>
            <p>
                <a href="https://podsawee.com" target="_blank">Podsawee W.</a> |
                <a href="https://www.linkedin.com/in/leonaruebet/" target="_blank">Naruebet A.</a> |
                <a href="https://linkedin.com" target="_blank">Nattgarni A.</a>
            </p>
        </div>
        """, unsafe_allow_html=True
        )
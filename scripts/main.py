import streamlit as st
from PIL import Image
import os

from functions.default_sidebar import default_sidebar

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

page_name = "Home Page"
default_sidebar(page_name)

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    <div style="display: flex; justify-content: center;">
        <img src="https://podsawee.com/cygentic_logo.png" style="width: 300px;">
    </div>
    <div style="text-align: center;">
        <h1>Cygentic</h1>
        <h3>To provide peace of mind by protecting enterprises</h3>
    </div>
    <div style="text-align: center;">
        <p>
            Welcome to our platform where you can explore various features and services.
            Our goal is to provide the best solutions tailored to your needs.
        </p>
    </div>
    """, unsafe_allow_html=True
)

if st.button("Get Started With ChatBot", key='center_button'):
    st.markdown('<meta http-equiv="refresh" content="0; url=/Chatbot">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center;">
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

import streamlit as st
import logging
import base64
from scripts.auth import get_authenticator
from typing import Any

st.set_page_config(page_title="Personal Coach", page_icon="🤖")

def get_img_as_base64(file_path: str) -> str:
    """Read an image file and return its Base64-encoded string."""
    with open(file_path, "rb") as f:
        data: bytes = f.read()
    return base64.b64encode(data).decode()

# Encode the background image
img: str = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")

def load_css() -> None:
    """
    Load the CSS file, replace the {{bg_img}} placeholder with the Base64 image,
    and apply the CSS to the app.
    """
    with open("styles/styles.css") as css_file:
        css: str = css_file.read()
    # Replace the placeholder with the actual Base64 image data
    css = css.replace("{{bg_img}}", f"data:image/jpg;base64,{img}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

# -------------------- Prompt User to Log In -------------------- #
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.error("Please log in first.")
    st.stop()

# Protected content for authenticated users
st.success(f"Welcome {st.session_state['name']}!")
st.write("Protected content here.")

# -------------------- Chatbot Functionality -------------------- #
st.title("Personal Coach")
st.write("Ask me your training-related questions!")

query: str = st.text_input("Enter your question:")

if st.button("Submit Query"):
    logging.info(f"User queried: {query}")
    response: str = "Response placeholder"  # TODO: Connect to chatbot logic
    st.write(response)

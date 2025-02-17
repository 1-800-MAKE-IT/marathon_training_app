import streamlit as st
import logging
import base64
from scripts.auth import get_authenticator
from typing import Any

st.set_page_config(page_title="Personal Coach", page_icon="🤖")

#____________________ PAGE CONFIG _____________________#

# Function to encode the image as Base64
@st.cache_data
def get_img_as_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        data: bytes = f.read()
    return base64.b64encode(data).decode()

# Encode the background image
img: str = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")

# Apply the background image via CSS
page_bg_img: str = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(
        rgba(255, 255, 255, 0.5), /* Adjust transparency */
        rgba(255, 255, 255, 0.5)
    ),
    url("data:image/jpg;base64,{img}");
    background-size: cover;           /* Ensures the image covers the entire area */
    background-repeat: no-repeat;     /* Prevents tiling */
    background-position: center top;  /* Aligns the image to the top center */
    background-attachment: scroll;    /* Image scrolls with content */
    height: 100vh;                    /* Ensures the container fills the full viewport */
    margin: 0;                        /* Removes any default margin causing gaps */
    padding: 0;                       /* Removes padding inside the container */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Additional inline CSS to force font color to black and input boxes to be white
st.markdown(
    """
    <style>
    /* Force all text to be black */
    * {
        color: black !important;
    }
    /* Style input boxes, text areas, and select elements */
    input, textarea, select {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#____________________ PROMPT USER TO LOG IN _____________________#

# Ensure authentication status is checked
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.error("Please log in first.")
    st.stop()

# Protected content for authenticated users
st.success(f"Welcome {st.session_state['name']}!")
st.write("Protected content here.")

#____________________ CHATBOT FUNCTIONALITY  _____________________#

# Chatbot Page
st.title("Personal Coach")
st.write("Ask me your training-related questions!")

query: str = st.text_input("Enter your question:")

if st.button("Submit Query"):
    logging.info(f"User queried: {query}")
    response: str = "Response placeholder"  # TODO: Connect to chatbot logic
    st.write(response)

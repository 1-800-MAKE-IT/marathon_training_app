import streamlit as st
import logging
import base64
from scripts.auth import login
from scripts.auth import get_authenticator


st.set_page_config(page_title="Personal Coach", page_icon="🤖")

#____________________ PAGE CONFIG _____________________#

# Function to encode the image as Base64
@st.cache_data
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode the background image
img = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")

# Apply the background image via CSS
page_bg_img = f"""
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

#____________________ PROMPT USER TO LOG IN _____________________#

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.error("Please log in first.")
    st.stop()

st.write("Protected content here.")
#____________________ CHATBOT FUNCTIONALITY  _____________________#

# Chatbot Page
st.title("Personal Coach")
st.write("Ask me your training-related questions!")

query = st.text_input("Enter your question:")

if st.button("Submit Query"):
    logging.info(f"User queried: {query}")
    response = "Response placeholder"  # TODO: Connect to chatbot logic
    st.write(response)
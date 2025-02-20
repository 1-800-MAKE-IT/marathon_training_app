import streamlit as st
import logging
import base64
from scripts.auth import get_authenticator
from typing import Any

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="Performance Entry", page_icon="📝")

def get_img_as_base64(file_path: str) -> str:
    """
    Reads the image from file_path and returns its Base64-encoded string.
    """
    with open(file_path, "rb") as f:
        data: bytes = f.read()
    return base64.b64encode(data).decode()

# Load and encode the background image.
img: str = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")

def load_css() -> None:
    """
    Loads the CSS file, replaces the background image placeholder with the Base64 image,
    and applies the CSS to the app.
    """
    with open("styles/styles.css") as css_file:
        css: str = css_file.read()
    # Replace the placeholder with the actual Base64 image string.
    css = css.replace("{{bg_img}}", f"data:image/jpg;base64,{img}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load the external CSS.
load_css()

# ------------------------------
# Prompt User to Log In
# ------------------------------
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.error("Please log in first.")
    st.stop()

# Protected content for authenticated users.
st.success(f"Welcome {st.session_state['name']}!")
st.write("Protected content here.")

# ------------------------------
# Performance Entry Functionality
# ------------------------------
st.title("Performance Entry")
st.write("Log your recent training performance.")

user: str = st.text_input("Username:")
distance: str = st.text_input("Distance (e.g., 10km):")
time: str = st.text_input("Time (e.g., 55:00):")
condition: str = st.text_input("Condition (e.g., Sunny):")
injuries: str = st.text_input("Injuries (if any):")
notes: str = st.text_area("Notes:")

if st.button("Save Data"):
    logging.info(f"Attempting to save data for user: {user}")
    try:
        # TODO: Connect to backend data storage logic
        st.success("Data saved successfully!")
        logging.info(f"Data saved successfully for user: {user}")
    except Exception as e:
        st.error("Failed to save data.")
        logging.error(f"Error saving data for user: {user}: {e}")

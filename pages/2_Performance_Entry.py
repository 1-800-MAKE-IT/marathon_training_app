import streamlit as st
import logging
import base64
from scripts.auth import get_authenticator
from typing import Any

#____________________ PAGE CONFIG _____________________#

st.set_page_config(page_title="Performance Entry", page_icon="📝")

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

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

#____________________ DATA ENTRY FUNCTIONALITY  _____________________#

# Performance Entry Page
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

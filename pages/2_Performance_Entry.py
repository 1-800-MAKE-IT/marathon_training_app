import streamlit as st
import logging
import base64

st.set_page_config(page_title="Performance Entry", page_icon="📝")

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

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

# Performance Entry Page
st.title("Performance Entry")
st.write("Log your recent training performance.")

user = st.text_input("Username:")
distance = st.text_input("Distance (e.g., 10km):")
time = st.text_input("Time (e.g., 55:00):")
condition = st.text_input("Condition (e.g., Sunny):")
injuries = st.text_input("Injuries (if any):")
notes = st.text_area("Notes:")

if st.button("Save Data"):
    logging.info(f"Attempting to save data for user: {user}")
    try:
        # TODO: Connect to backend data storage logic
        st.success("Data saved successfully!")
        logging.info(f"Data saved successfully for user: {user}")
    except Exception as e:
        st.error("Failed to save data.")
        logging.error(f"Error saving data for user: {user}: {e}")
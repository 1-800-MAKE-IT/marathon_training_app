import streamlit as st
import base64

# Set up page configuration
st.set_page_config(page_title="Home 🏠", page_icon="🏠", layout="wide")

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

# Main app title and description
st.title("Marathon Training App")
st.markdown("""
An AI-powered tool to help you plan, track, and optimize your marathon training journey!
""")
st.markdown("""
**IMPORTANT NOTE:** Please do not enter ANY sensitive data or Personally Identifiable Information (PII). Use a fully anonymized username when prompted.
""")

st.markdown("""
Use the sidebar to navigate:
- **Personal Coach**: Ask questions and get insights.
- **Performance Entry**: Log your training progress.
""")

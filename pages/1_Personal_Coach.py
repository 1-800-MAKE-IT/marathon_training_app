import streamlit as st
import logging
import base64


st.set_page_config(page_title="Personal Coach", page_icon="🤖")

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
        rgba(255, 255, 255, 0.5), /* Adjust overlay transparency */
        rgba(255, 255, 255, 0.5)
    ),
    url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: scroll; /* Ensures the image scrolls with content */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Chatbot Page
st.title("Personal Coach")
st.write("Ask me your training-related questions!")

query = st.text_input("Enter your question:")

if st.button("Submit Query"):
    logging.info(f"User queried: {query}")
    response = "Response placeholder"  # TODO: Connect to chatbot logic
    st.write(response)
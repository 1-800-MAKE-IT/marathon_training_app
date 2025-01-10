import streamlit as st
import logging
#from scripts.chatbot import get_response  # Import chatbot logic
#from scripts.data_storage import save_user_data, get_user_data  # Import data management logic
# Set up page configuration
st.set_page_config(page_title="Marathon Training App", layout="wide")

# Configure logging (restricted to backend, not displayed to users)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
    ]
)

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

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
- **Chatbot**: Ask questions and get insights.
- **Performance Entry**: Log your training progress.
""")

# Add navigation to multi-page functionality (pages are defined in the `pages` directory)
st.sidebar.title("Navigation")
st.sidebar.info("Choose a page:")
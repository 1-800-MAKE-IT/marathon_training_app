import streamlit as st
import logging
#from scripts.chatbot import get_response  # Import chatbot logic
#from scripts.data_storage import save_user_data, get_user_data  # Import data management logic


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()         # Print logs to console
    ]
)

#set title and add disclaimer
st.set_page_config(page_title="Training Buddy", layout="centered")
st.title("Marathon Training App")
st.markdown("An AI-powered tool to help you plan, track, and optimize your marathon training journey!.")
st.markdown("IMPORTANT NOTE: Please do not enter ANY Personally Identifiable Information (PII). When prompted for a username, please ensure to use an anonymised one, and never enter ANY sensitive data.")


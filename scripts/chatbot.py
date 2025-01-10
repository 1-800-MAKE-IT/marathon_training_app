import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()         # Print logs to console
    ]
)

st.title("Chatbot")

# Input for user query
query = st.text_input("Ask a question about your training:")
if st.button("Submit Query"):
    # Placeholder: Display response
    st.write("Response goes here.")
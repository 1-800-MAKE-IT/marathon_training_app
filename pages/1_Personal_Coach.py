import streamlit as st
import logging


st.set_page_config(page_title="Personal Coach", page_icon="🤖")

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
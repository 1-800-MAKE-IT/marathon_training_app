import streamlit as st
import logging

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Chatbot Page
st.title("Chatbot")
st.write("Ask your training-related questions!")

query = st.text_input("Enter your question:")

if st.button("Submit Query"):
    logging.info(f"User queried: {query}")
    response = "Response placeholder"  # TODO: Connect to chatbot logic
    st.write(response)
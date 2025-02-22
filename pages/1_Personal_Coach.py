import streamlit as st
import logging
import base64
from scripts.auth import get_authenticator
from typing import Any, Tuple
from scripts.create_database import generate_data_store
from scripts.query_data import query_vector_db


# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="Personal Coach", page_icon="🤖")

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
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False  # Set initial authentication status

# Display login prompt if not authenticated
if not st.session_state["authentication_status"]:
    st.error("Please log in first.")
    st.stop()

# Display protected content for authenticated users
if st.session_state["authentication_status"]:
    st.success(f"Welcome {st.session_state['name']}!")
    st.write("Protected content here.")

    # ------------------------------
    # Chatbot Functionality
    # ------------------------------
    st.title("Personal Coach")
    st.write("Ask me your training-related questions!")

    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display past chat messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input for chat
    query: str = st.chat_input("Ask a question...")

    if query:
        logging.info(f"User queried: {query}")

        # Append user query to chat history
        st.session_state["messages"].append({"role": "user", "content": query})

        # Call model and get response
        response: str = generate_data_store()

        if response != "Complete":
            st.error("Error: Unable to fetch data. Please try again.")
        else:
            # Call model and get response
            error_code, bot_response = query_vector_db(query)  

            # Append bot response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": bot_response})

            # Display bot response
            with st.chat_message("assistant"):
                st.write(bot_response)

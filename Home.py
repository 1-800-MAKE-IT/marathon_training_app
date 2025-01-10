import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

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

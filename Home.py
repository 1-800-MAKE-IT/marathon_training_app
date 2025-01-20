import streamlit as st
import base64
from scripts.arxiv_scraper import fetch_arxiv_papers, get_directory_size
import logging
from scripts.auth import get_authenticator

# ========================
# 1. Page Configuration
# ========================
# Set up the page with a title, icon, and layout style
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Load a custom CSS file for styling the page
def load_css():
    with open("styles/styles.css") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

load_css()

# ========================
# 2. Set Background Image
# ========================
# Function to encode the background image to Base64 format
@st.cache_data
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode and apply the background image
img = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(
        rgba(255, 255, 255, 0.5),
        rgba(255, 255, 255, 0.5)
    ),
    url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center top;
    background-attachment: scroll;
    height: 100vh;
    margin: 0;
    padding: 0;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ========================
# 3. Login Authentication
# ========================
# Initialize the authenticator and prompt the user to log in
authenticator = get_authenticator()
authenticator.login(location='main', key='Login')

# Handle different authentication states
if st.session_state['authentication_status']:
    # Display a welcome message for authenticated users
    st.success(f"Welcome {st.session_state['name']}")

    # ========================
    # 4. Main App Content
    # ========================
    # Add titles and descriptions
    st.title("Marathon Training App")
    st.markdown("""
    An AI-powered tool to help you plan, track, and optimize your marathon training journey!
    """)
    st.markdown("""
    **IMPORTANT NOTE:** Please do not enter ANY sensitive data or Personally Identifiable Information (PII).
    Use a fully anonymized username when prompted.
    """)
    st.markdown("""
    Use the sidebar to navigate:
    - **Personal Coach**: Ask questions and get insights.
    - **Performance Entry**: Log your training progress.
    """)

    # ========================
    # 5. Update Academic Research
    # ========================
    # Section for fetching academic papers from arXiv
    st.title("Update Academic Research")
    st.markdown("""
    Fetch the latest marathon-related academic papers from arXiv and update the database.
    """)

    # Display current storage usage
    current_size = get_directory_size("data")
    max_size_mb = 700
    st.info(f"Current Storage Usage: {current_size:.2f} MB / {max_size_mb} MB")

    # Input for the number of papers to fetch
    num_papers = st.number_input(
        "Number of papers to fetch:", min_value=1, max_value=50, value=10, step=1
    )

    # Button to trigger fetching academic papers
    if st.button("Update Academic Data"):
        try:
            # Fetch papers using the fetch_arxiv_papers function
            papers = fetch_arxiv_papers(
                query="marathon training",
                max_results=num_papers,
                max_storage_mb=max_size_mb
            )

            # Provide feedback to the user based on the results
            if len(papers) == 0:
                st.warning(
                    "No new papers fetched. Storage limit may have been reached."
                )
            else:
                st.success(f"Successfully fetched {len(papers)} papers.")
                updated_size = get_directory_size("data/papers")
                st.info(f"Updated Storage Usage: {updated_size:.2f} MB / {max_size_mb} MB")

        except Exception as e:
            # Handle any errors and display appropriate messages
            st.error(f"An error occurred: {e}")
            logging.error(f"Exception in fetching academic data: {e}")

elif st.session_state['authentication_status'] is False:
    # Display an error if login credentials are invalid
    st.error("Invalid credentials")

else:
    # Prompt the user to log in
    st.warning("Please enter your username and password")

# ========================
# 6. Summary
# ========================
# This code integrates the fetch_arxiv_papers function to fetch and update academic research data.
# Key Features:
# - Login authentication to restrict access.
# - Base64 background image for a polished UI.
# - Storage usage check to ensure compliance with hosting constraints.
# - Dynamic feedback for updating research data.
#
# The rest of the homepage remains unchanged while seamlessly incorporating the new functionality.

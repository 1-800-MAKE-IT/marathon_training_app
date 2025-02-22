import streamlit as st
import base64
from scripts.arxiv_scraper import fetch_arxiv_papers, get_directory_size
import logging
from scripts.auth import get_authenticator
from typing import Any, List

# ========================
# 1. Page Configuration
# ========================
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

def get_img_as_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        data: bytes = f.read()
    return base64.b64encode(data).decode()

img: str = get_img_as_base64("styles/6xfSTbbCWr4WJTCdnRwiVT.jpg")

def load_css() -> None:
    with open("styles/styles.css") as css_file:
        css: str = css_file.read()
    # Replace the background image placeholder with the actual base64 string
    css = css.replace("{{bg_img}}", f"data:image/jpg;base64,{img}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

# ========================
# 3. Login Authentication
# ========================
authenticator: Any = get_authenticator()
authenticator.login(location='main', key='Login')

if st.session_state['authentication_status']:
    st.success(f"Welcome {st.session_state['name']}")

    # ========================
    # 4. Main App Content
    # ========================
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
    st.title("Update Academic Research")
    st.markdown("""
    Fetch the latest marathon-related academic papers from arXiv and update the database.
    """)
    current_size: float = get_directory_size("data")
    max_size_mb: int = 700
    st.info(f"Current Storage Usage: {current_size:.2f} MB / {max_size_mb} MB")
    num_papers: int = st.number_input("Number of papers to fetch:", min_value=1, max_value=100, value=10, step=1)
    
    if st.button("Update Academic Data"):
        try:
            papers: List[Any] = fetch_arxiv_papers(
                query="marathon training",
                max_results=num_papers,
                max_storage_mb=max_size_mb
            )
            if len(papers) == 0:
                st.warning("No new papers fetched. Storage limit may have been reached.")
            else:
                st.success(f"Successfully fetched {len(papers)} papers.")
                updated_size: float = get_directory_size("data/papers")
                #st.info(f"Updated Storage Usage: {updated_size:.2f} MB / {max_size_mb} MB")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logging.error(f"Exception in fetching academic data: {e}")

elif st.session_state['authentication_status'] is False:
    st.error("Invalid credentials")
else:
    st.warning("Please enter your username and password")

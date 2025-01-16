import streamlit as st
import base64
from scripts.arxiv_scraper import fetch_arxiv_papers, get_directory_size
import logging
from scripts.auth import get_authenticator


#____________________ PAGE CONFIG ____________________#
# Set up page configuration
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

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
        rgba(255, 255, 255, 0.5), /* Adjust transparency */
        rgba(255, 255, 255, 0.5)
    ),
    url("data:image/jpg;base64,{img}");
    background-size: cover;           /* Ensures the image covers the entire area */
    background-repeat: no-repeat;     /* Prevents tiling */
    background-position: center top;  /* Aligns the image to the top center */
    background-attachment: scroll;    /* Image scrolls with content */
    height: 100vh;                    /* Ensures the container fills the full viewport */
    margin: 0;                        /* Removes any default margin causing gaps */
    padding: 0;                       /* Removes padding inside the container */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#____________________ PROMPT USER TO LOGIN ____________________#

authenticator = get_authenticator()

name, status, user = authenticator.login('Login', 'main')
if status:
    st.success(f"Welcome {name}")
elif status is False:
    st.error("Invalid credentials")
else:
    st.warning("Enter login details")

#____________________ SHOW TITLE OF HOMEPAGE ____________________#


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
- **Personal Coach**: Ask questions and get insights.
- **Performance Entry**: Log your training progress.
""")

st.title("Update Academic Research")
st.markdown("""
Fetch the latest marathon-related academic papers from arXiv and update the database.
""")

# Display current storage usage
current_size = get_directory_size("data")
max_size_mb = 700
st.info(f"Current Storage Usage: {current_size:.2f} MB / {max_size_mb} MB")


#____________________ ALLOW USERS TO ADD NEWER RESEARCH ____________________#

#allow users to add more papers
num_papers = st.number_input("Number of papers to fetch:", min_value=1, max_value=50, value=10, step=1)

# Add a button to trigger the scraper
if st.button("Update Academic Data"):
    try:
        papers, updated_size = fetch_arxiv_papers(max_results=num_papers)
        if papers is None:
            st.warning(f"Storage limit reached. No new data fetched. Current usage: {current_size:.2f} MB.")
        else:
            st.success(f"Successfully fetched {len(papers)} papers.")
            st.info(f"Updated Storage Usage: {updated_size:.2f} MB / {max_size_mb} MB")
    except ValueError as ve:
        st.error("Unexpected return values from fetch_arxiv_papers.")
        logging.error(f"ValueError: {ve}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logging.error(f"Exception: {e}")
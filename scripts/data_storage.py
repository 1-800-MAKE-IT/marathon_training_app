import logging
from langchain.document_loaders import DirectoryLoader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()         # Print logs to console
    ]
)

def load_documents():
    """
    Load documents into Document datatype in langchain. document also includes metadata

    Returns:

    """
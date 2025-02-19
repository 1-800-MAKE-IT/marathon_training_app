import logging
import os
import shutil
from typing import List
import streamlit as st
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()          # Print logs to console
    ]
)

def load_documents(data_path: str = "data/PDFs") -> List[Document]:
    """
    Load documents into Document datatype in langchain. Document also includes metadata.
    TO DO - add additional metadata from json file.

    Parameters:
    - data_path (str): Path where data is located

    Returns:
    - List[Document]: List of langchain document objects containing documents and metadata
    """
    loader = DirectoryLoader(data_path, glob="*.pdf")
    documents: List[Document] = loader.load()
    
    logging.info(f"Downloaded {len(documents)} documents with metadata.")

    return documents

def split_text() -> List[Document]:
    """
    Gets chunks from documents.
    """
    documents: List[Document] = load_documents(data_path="data/PDFs")

    chunk_size: int = 1000
    chunk_overlap: int = 500

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True
    )

    chunks: List[Document] = text_splitter.split_documents(documents)

    logging.info(f"Downloaded {len(documents)} documents and split into {len(chunks)}. Chunk size: {chunk_size}, overlap: {chunk_overlap}")

    return chunks

def save_to_chroma(chunks: List[Document]) -> int:
    """
    Creates ChromaDB and saves chunks from documents.
    """

    chroma_path: str = "data/chroma"

    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    logging.info(f"Created and populated ChromaDB at path {chroma_path}")

    # Retrieve OpenAI API key from Streamlit secrets
    openai_api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]

    # Ensure API key is set as an environment variable 
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Initialize OpenAI embeddings
    openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    db = Chroma.from_documents(
        chunks, openai_embeddings, persist_directory=chroma_path
    )

    # Save database
    db.persist()

    logging.info(f"Saved {len(chunks)} chunks to {chroma_path}.")

    return 1

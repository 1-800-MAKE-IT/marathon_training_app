import logging
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()          # Print logs to console
    ]
)

def load_documents(data_path: str = "data/PDFs") -> List[Document] :
    """
    Load documents into Document datatype in langchain. Document also includes metadata.
    TO DO - add additional metadata from json file.

    Inputs:
    data_path (str) : path where data is located 

    Returns:
    Documents (list of langchain document objects) : documents and metadata
    """
    loader = DirectoryLoader(data_path, glob="*.pdf")
    documents: List[Document] = loader.load()
    
    logging.info(f'''Downloaded documents with metadata: {documents.metadata}''')

    return documents

def split_text() -> List[Document] :
    """
    Gets chunks
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

    logging.info(f'''Downloaded {len(documents)} documents and split into {len(chunks)}. Chunk_size was {chunk_size} and chunk overlap {chunk_overlap}''')

    return chunks

def save_to_chroma() -> int :
    
    
    chroma_path : str = "data/chroma"


    logging.info(f'''Created and populated chroma db at path {chroma_path} ''')

    


    return 1
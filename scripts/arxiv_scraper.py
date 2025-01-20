import os
import arxiv
import requests
import json
from PyPDF2 import PdfReader
from datetime import datetime
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("arxiv_scraper.log"),  # Save logs to a file
        logging.StreamHandler()         # Print logs to console
    ]
)

# ========================
# 1. Fetch Metadata and PDFs
# ========================
def fetch_arxiv_papers(query="marathon training", max_results=10, max_storage_mb=1000):
    """
    Fetch metadata and download PDFs from arXiv based on the query.

    Parameters:
    - query (str): Search query for arXiv (e.g., "marathon training").
    - max_results (int): Maximum number of papers to fetch.
    - save_dir (str): Directory to save downloaded PDFs and metadata.
    - max_storage_mb (int): Storage limit in MB to avoid exceeding hosting constraints.

    Returns:
    - papers (list): A list of dictionaries containing metadata for each fetched paper.
    """
    # Ensure the save directory exists (but doesn't overwrite or delete contents) regardless of whether we are on a Unix system or not
    save_dir = os.path.join("data", "papers")
    os.makedirs(save_dir, exist_ok=True)

    # Search for papers on arXiv based on the query
    search = arxiv.Search(
        query=query,  # The search term
        max_results=max_results,  # Limit the number of results
        sort_by=arxiv.SortCriterion.Relevance  # Sort results by relevance
    )

    papers = []  # List to store metadata for fetched papers

    for result in search.results():
        
        paper_id = result.entry_id.split('/')[-1]  # Extract unique paper ID
        paper_path = os.path.join(save_dir, f"{paper_id}.pdf")  # Define file path for the PDF

        # Skip if the PDF already exists to avoid re-downloading
        if os.path.exists(paper_path):
            logging.info(f"Paper {paper_id} already downloaded. Skipping.")
            continue

        # Check current storage usage to ensure we don't exceed the limit
        current_size = get_directory_size(save_dir)
        if current_size >= max_storage_mb:
            logging.warning("Storage limit reached. Aborting further downloads.")
            break  # Stop downloading when storage limit is reached

        # Download the PDF
        try:
            response = requests.get(result.pdf_url, timeout=10)  # Fetch the PDF from arXiv
            with open(paper_path, "wb") as f:
                f.write(response.content)  # Save the PDF to the specified directory

            # Append metadata for the successfully downloaded paper
            papers.append({
                "id": paper_id,
                "title": result.title,
                "abstract": result.summary,
                "authors": [author.name for author in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "source": paper_path  # Store the path to the downloaded PDF
            })

            logging.info(f"Downloaded paper: {result.title}")  # Log successful download

        except Exception as e:
            logging.error(f"Failed to download paper {paper_id}: {e}")  # Log download failures

    # Save metadata for all fetched papers into a JSON file
    metadata_path = os.path.join(save_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(papers, f, indent=2)  # Save metadata in a human-readable format

    return papers  # Return the metadata for all fetched papers


# ========================
# 2. Chunk and Embed Text
# ========================
def process_papers_for_embedding(papers, chunk_size=500, model_name="all-MiniLM-L6-v2", vector_db=None):
    """
    Process each paper: chunk the text, generate embeddings, and optionally store in a vector database.

    Parameters:
    - papers (list): List of paper metadata dictionaries.
    - chunk_size (int): Number of tokens per chunk.
    - model_name (str): Name of the embedding model (e.g., "all-MiniLM-L6-v2").
    - vector_db: Optional vector database object to store embeddings.
    """
    model = SentenceTransformer(model_name)  # Initialize the embedding model

    for paper in papers:

        try:
            pdf_path = paper["source"]  # Get the path to the PDF from the metadata

            # Chunk the text extracted from the PDF
            chunks = chunk_paper_text(pdf_path, chunk_size=chunk_size)

            # Process each chunk
            for idx, chunk in enumerate(chunks):
                embedding = model.encode(chunk)  # Generate embedding for the chunk

                # Create metadata for the chunk
                metadata = {
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "published": paper["published"],
                    "chunk_index": idx,  # Index of the chunk within the paper
                    "source": paper["source"]  # Path to the original PDF
                }

                # Store the chunk and its embedding in the vector database, if provided
                if vector_db:
                    vector_db.add_texts(
                        documents=[chunk],  # The chunked text
                        metadatas=[metadata],  # Metadata for the chunk
                        embeddings=[embedding]  # Precomputed embedding
                    )

            logging.info(f"Processed and embedded {len(chunks)} chunks for paper: {paper['title']}")

        except Exception as e:
            logging.error(f"Failed to process paper {paper['title']}: {e}")


# ========================
# 3. Chunk PDF Text
# ========================
def chunk_paper_text(pdf_path, chunk_size=500):
    """
    Extract text from a PDF and split it into smaller chunks.

    Parameters:
    - pdf_path (str): Path to the PDF file.
    - chunk_size (int): Number of tokens per chunk.

    Returns:
    - chunks (list): List of text chunks extracted from the PDF.
    """
    reader = PdfReader(pdf_path)  # Load the PDF file
    
    # Extract all text from the PDF
    full_text = " ".join([page.extract_text() for page in reader.pages])

    # Split the text into chunks of specified size
    words = full_text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return chunks  # Return the list of chunks


# ========================
# 4. Calculate Directory Size
# ========================
def get_directory_size(directory):
    """
    Calculate the total size of a directory in megabytes (MB).

    Parameters:
    - directory (str): Path to the directory.

    Returns:
    - total_size (float): Total size of the directory in MB.
    """
    total_size = 0

    # Walk through all files in the directory and sum their sizes
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)  # Full path to the file
            total_size += os.path.getsize(fp)  # Add file size to total

    return total_size / (1024 * 1024)  # Convert bytes to MB and return


# ========================
# Summary
# ========================
# This script handles the end-to-end process of fetching academic papers from arXiv, extracting and chunking
# their content, and generating embeddings for use in a vector database. It is designed to be robust, efficient,
# and compatible with dynamic environments like Streamlit hosting.


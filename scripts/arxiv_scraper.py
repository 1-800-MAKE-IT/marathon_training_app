import os
import arxiv
import requests
import json
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("arxiv_scraper.log"),  # Save logs to a file
        logging.StreamHandler()                   # Print logs to console
    ]
)

# ========================
# 1. Fetch Metadata and Download PDFs
# ========================
def fetch_arxiv_papers(query="marathon training guide", max_results=100, max_storage_mb=600):
    """
    Fetch metadata and download PDFs from arXiv based on the query.

    Parameters:
    - query (str): Search query for arXiv (e.g., "marathon training").
    - max_results (int): Maximum number of papers to fetch.
    - max_storage_mb (int): Storage limit in MB to avoid exceeding hosting constraints.

    Returns:
    - papers (list): A list of dictionaries containing metadata for each downloaded paper.
    """
    # Define the directory where PDFs will be saved
    pdf_dir = os.path.join("data", "PDFs")
    os.makedirs(pdf_dir, exist_ok=True)  # Ensure the PDF directory exists

    # Define the directory where metadata will be saved
    metadata_dir = os.path.join("data", "metadata")
    os.makedirs(metadata_dir, exist_ok=True)  # Ensure the metadata directory exists

    # Search for papers on arXiv based on the query
    search = arxiv.Search(
        query=query,                           # The search term
        max_results=max_results,               # Limit the number of results
        sort_by=arxiv.SortCriterion.Relevance  # Sort results by relevance
    )

    papers = []  # List to store metadata for downloaded papers

    for result in search.results():

        paper_id = result.entry_id.split('/')[-1]  # Extract unique paper ID
    
        title_string_with_spaces : str = result.title
        title_string_no_spaces : str = title_string_with_spaces.replace(" ", "_")

        paper_path = os.path.join(pdf_dir, f"{title_string_no_spaces}.pdf")  # Define file path for the PDF

        # Skip if the PDF already exists to avoid re-downloading
        if os.path.exists(paper_path):
            logging.info(f"Paper {paper_id} already downloaded. Skipping.")
            continue

        # Check current storage usage to ensure we don't exceed the limit
        current_size = get_directory_size(pdf_dir)
        if current_size >= max_storage_mb:
            logging.warning("Storage limit reached. Aborting further downloads.")
            break  # Stop downloading when storage limit is reached

        # Download the PDF from arXiv
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

    # Save metadata for all downloaded papers into a JSON file in the metadata directory
    metadata_path = os.path.join(metadata_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(papers, f, indent=2)  # Save metadata in a human-readable format

    return papers  # Return the metadata for all downloaded papers

# ========================
# 2. Calculate Directory Size
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
# This script handles the process of fetching academic papers from arXiv based on a query,
# downloading the PDFs to the 'data/PDFs' directory, and saving the metadata for each paper
# in the separate 'data/metadata' directory.
# It is designed to be robust and efficient, with logging for monitoring download progress and errors.

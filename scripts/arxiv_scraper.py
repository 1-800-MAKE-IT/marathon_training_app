import logging
import arxiv 
import json
import os 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("arxiv_scraper.log"),  # Save logs to a file
        logging.StreamHandler()         # Print logs to console
    ]
)

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)

    return total_size / (1024 * 1024)  # Convert to MB

def fetch_arxiv_papers(
    query="marathon",
    max_results=10,
    file_path="data/academic_data.json",
    max_size_mb=700
    ):
    """
    Fetch papers from arXiv and enforce storage limits.
    Returns the updated storage size after saving the papers.
    """

    logging.info(f"Fetching papers for query: {query}, (max results: {max_results})")

    # Check current storage size
    data_dir = os.path.dirname(file_path)
    current_size = get_directory_size(data_dir)

    #we are going to limit our storage of 
    if current_size >= max_size_mb:
        logging.warning(f"Storage limit exceeded: {current_size:.2f}MB (Limit: {max_size_mb}MB)")
        return None, current_size
    
    # Fetch papers from arXiv
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = {}
    fetched_count = 0
    for result in search.results():
        papers[result.entry_id] = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "abstract": result.summary,
            "link": result.entry_id,
            "pdf_link": result.pdf_url,
        }
        fetched_count += 1

    logging.info(f"Fetched {fetched_count} papers successfully.")

    # Save papers to JSON file
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists
    with open(file_path, "w") as f:
        json.dump(papers, f, indent=4)

    updated_size = get_directory_size(data_dir)
    logging.info(f"Saved fetched papers to {file_path}. Updated directory size: {updated_size:.2f} MB")

    return papers, updated_size

# Testing Functionality (Optional, for local testing only)
if __name__ == "__main__":
    try:
        logging.info("Starting arXiv data fetch script.")
        updated_papers = fetch_arxiv_papers()
        if updated_papers is None:
            logging.warning("Storage limit reached. No new data fetched.")
        else:
            logging.info(f"Successfully fetched and saved {len(updated_papers)} papers.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

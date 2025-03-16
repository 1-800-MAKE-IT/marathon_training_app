#force correct sqlite3 version
try:
    import pysqlite3
    import sys
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass

import logging
from typing import Tuple, List
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()          # Print logs to console
    ]
)

def query_vector_db(query_text: str) -> str:
    """
    Query the vector database for similar documents and generate a response.

    Parameters:
    - query_text (str): The query text for similarity search.

    Returns:
    - Tuple[int, str]: A tuple indicating success (1) or failure (0) and a formatted response.
    """
    logging.info(f"Querying vector database with query: {query_text}")

    chroma_path: str = "data/chroma"

    prompt_template = '''
    Answer the question based only on the following context:
    ---
    {context}
    ---
    Answer the question based on the above context:
    {question}
    '''

    # Prepare database
    logging.info(f"Preparing database at path: {chroma_path}")
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Embed the query (ensure query_embedding is a list of lists)
    query_embedding = embedding_function.embed_query(query_text)

    logging.info(f"Query embedding: {query_embedding}")

    
    # Perform the similarity search
    results: List[Tuple[Document, float]] = db.similarity_search_by_vector(query_embedding, n_results=5)

    logging.info(f"Performing similarity search for query: {query_text}")

    if len(results) == 0 or results[0][1] < 0.7:
        logging.info(f"No matching results found for query: {query_text}")
        return  "Unable to return matching results."

    logging.info(f"Found {len(results)} matching documents for query: {query_text}")

    # Concatenate context texts from all matching documents
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Create a prompt template using presets
    prompt_template = ChatPromptTemplate.from_template(prompt_template)

    # Format the prompt
    logging.info("Formatting prompt with context and query")
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Initialize a model and call it on our prompt
    logging.info("Initializing ChatOpenAI model")
    model = ChatOpenAI()
    response_text = model.predict(prompt)

    # Load sources
    logging.info("Loading sources from matched documents")
    sources = [doc.metadata.get("source", None) for doc, _score in results]

    # Format the response
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    logging.info(f"Query successful. Response generated for query: {query_text}")

    return formatted_response

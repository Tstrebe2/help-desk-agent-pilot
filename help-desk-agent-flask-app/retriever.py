# retriever.py
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path

_chroma_db_path = Path("../../datasets/help-desk-tickets/chroma_db").resolve()

def load_helpdesk_ticket_vector_store():
    """
    Load a vector store for EHR support tickets using Chroma.
    Raises an error if the directory does not exist.
    """
    if not _chroma_db_path.exists():
        raise FileNotFoundError(f"Chroma DB directory not found: {_chroma_db_path}")

    vector_store = Chroma(
        collection_name="helpdesk_tickets",
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=_chroma_db_path
    )
    return vector_store
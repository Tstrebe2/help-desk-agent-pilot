# retriever.py
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path

CHROMA_DB_PATH = Path("../../datasets/help-desk-tickets/chroma_db").resolve()

# Loads the vector store from the specified directory if it already exists
VECTOR_STORE = Chroma(
    collection_name="helpdesk_tickets",
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    persist_directory=CHROMA_DB_PATH
)
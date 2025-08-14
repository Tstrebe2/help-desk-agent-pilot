from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def load_chroma_db_retriever(chroma_db_path, collection_name):
    """
    Load a Chroma DB retriever for document retrieval.
    """
    if not chroma_db_path.exists():
        raise FileNotFoundError(f"Chroma DB directory not found: {chroma_db_path}")

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=chroma_db_path
    )
    return vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 3}
    )
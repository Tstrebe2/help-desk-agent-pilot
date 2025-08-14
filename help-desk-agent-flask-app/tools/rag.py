from operator import itemgetter
import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import convert_runnable_to_tool
from retrievers.chroma_db import load_chroma_db_retriever

def document_formatter(documents):
    """
    Format the retrieved documents for the prompt.

    Args:
        documents: The list of LangChain Document objects to format.

    Returns:
        The formatted document string.
    """
    formatted_docs = []

    for doc in documents:
        ticket_id = doc.metadata.get('TicketID', 'Unknown TicketID')
        url = f"/ticket/{ticket_id}"
        page_content = doc.page_content
        formatted_doc = f"**TicketID:** [{ticket_id}]({url})\n\n{page_content}"
        formatted_docs.append(formatted_doc)
    return "\n\n".join(formatted_docs)

def get_rag_chain(retriever):
    """
    Create a RAG chain for document retrieval and question answering.

    Args:
        retriever: The document retriever to use.

    Returns:
        The RAG chain.
    """
    rag_chain = itemgetter("question") | retriever | RunnableLambda(document_formatter)
    return rag_chain

def create_rag_tool_from_runnable():
    """
    Create a RAG tool for document retrieval and ticket citation
    """
    chroma_db_path = Path("../../datasets/help-desk-tickets/chroma_db").resolve()
    collection_name = "helpdesk_tickets"
    retriever = load_chroma_db_retriever(chroma_db_path, collection_name)

    config_path = Path("../help-desk-agent-flask-app/configs/rag_tool.yaml").resolve()
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    tool_config = config['tool_config']
    args_schema = tool_config['args_schema']

    class RAGToolArgsSchema(BaseModel):
        question: str = Field(description=args_schema['question_description'])

    rag_chain = get_rag_chain(retriever)

    rag_tool = convert_runnable_to_tool(
        rag_chain,
        name=tool_config['name'],
        description=tool_config['description'],
        args_schema=RAGToolArgsSchema,
    )
    return rag_tool
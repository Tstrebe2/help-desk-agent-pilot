
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import convert_runnable_to_tool
from pydantic import BaseModel, Field
from retriever import VECTOR_STORE

class InputSchema(BaseModel):
    question: str = Field(
        description=(
            "A natural language question about electronic health record (EHR) system "
            "tickets or issues, such as 'What is causing pharmacy work stoppages?'"
        )
    )

def get_top_k_documents(query: str):
    """Retrieve the top-k documents based on the hyde query."""
    top_k_documents = VECTOR_STORE.similarity_search(query, k=3)
    return top_k_documents

def format_documents(documents):
    """
    Format retrieved docs so that each begins with [TicketID],
    followed by EHR fields like Facility, EHRModule, etc.
    Ensures that TicketID is exposed in exactly bracketed form.
    """
    formatted = []
    for doc in documents:
        tid = doc.metadata.get("TicketID", "UNKNOWN_ID")
        content = doc.page_content
        formatted.append(f"TicketID: [{tid}]\n{content}")
    return "\n\n".join(formatted)

def get_rag_tool():
    """
    Create a RAG tool that uses the GoogleGenerativeAI model to generate responses
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)

    hyde_template = (
    "Based on the question: {question} "
    "Write a passage that could contain the answer to the question: " 
    )
    hyde_prompt = PromptTemplate(
        input_variables=["question"],
        template=hyde_template
    )

    get_top_k_documents_rl = RunnableLambda(get_top_k_documents)
    format_documents_rl = RunnableLambda(format_documents)

    hyde_chain = hyde_prompt | llm | StrOutputParser()
    retreival_chain = get_top_k_documents_rl | format_documents_rl | StrOutputParser()
    rag_chain = hyde_chain | retreival_chain

    rag_tool = convert_runnable_to_tool(
        runnable=rag_chain,
        name="ehr_ticket_rag_retriever",
        description=(
            "Useful for answering questions about EHR system issues using information extracted from support tickets. "
            "Given a question, it generates a hypothesis passage, retrieves relevant tickets, and formats their contents."
        ),
        args_schema=InputSchema
    )
    return rag_tool
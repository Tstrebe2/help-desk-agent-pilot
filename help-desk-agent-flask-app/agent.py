# agent.py
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_tool import get_rag_tool

def create_agent():
    """
    Create a ReACT agent that uses the RAG tool for answering questions
    about EHR support tickets.
    """
    # Define the system prompt for the agent
    system_prompt = """
    You are a support assistant for EHR support tickets. Tools retrieve actual ticket records, and Ticket IDs are shown in square brackets — e.g. [c27b6138].

    When answering a user's question:
    - Summarize the explanation using Ticket IDs only in square brackets, never full metadata dump.
    - For example: “The issue appears in [c27b6138], [48cf2892], [0dd06ea2] — it's related to delays in the Pharmacy module…”
    - Always include at least one bracketed TicketID if relevant.
    - If no ticket matches, say “I couldn't find any relevant ticket for that question.”

    - Provide answers that are strictly based on ticket data. Do NOT hallucinate Ticket IDs.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=1.0)
    rag_tool = get_rag_tool()
    return create_react_agent(model=llm, tools=[rag_tool], state_modifier=system_prompt)

REACT_AGENT = create_agent()
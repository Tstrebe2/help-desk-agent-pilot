# agent.py
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_tool import get_rag_tool
from ticket_citation_tool import ticket_citation_tool

def create_agent_with_memory():
    """
    Create a ReACT agent that uses the RAG tool for answering questions
    about EHR support tickets.
    """
    # Define the system prompt for the agent
    system_prompt = (
    "You are a helpful assistant for the Department of Veterans Affairs (VA) employees. "
    "Your job is to help answer VA employees with questions about issues related to the "
    "electronic health record modernization (EHRM) enterprise rollout. Whenever you use "
    "ticket information (by description, issue summary, or content), you **must** call the "
    "`ticket_citation_tool` with the relevant `ticket_id` to generate a hyperlink. "
    "You **must not** refer to ticket info without hyperlinking. If you do not have enough "
    "information, let the user know that you need more details or to clarify the question."
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=1.0)
    rag_tool = get_rag_tool()
    tools = [rag_tool, ticket_citation_tool]
    memory = MemorySaver()
    agent = create_react_agent(
        model=llm, 
        tools=tools, 
        prompt=system_prompt,
        checkpointer=memory,
    )
    return agent
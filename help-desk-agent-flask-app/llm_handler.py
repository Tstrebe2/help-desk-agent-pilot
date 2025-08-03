# llm_handler.py
from agent import REACT_AGENT

def get_agent_response(prompt):
    response = REACT_AGENT.invoke({"messages": [("user", prompt)]})
    return response['messages'][-1].content
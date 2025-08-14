# llm_handler.py
from agents.react_agent import create_react_agent_with_tools

_config = {"configurable": {"thread_id": "tim-session-1"}}
_react_agent = create_react_agent_with_tools()

def get_agent_response(prompt):

    events = _react_agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        stream_mode="values",
        config=_config,
    )

    last_message = None
    
    for event in events:
        if "messages" in event:
            # Multiple messages might appear, take the latest
            for msg in event["messages"]:
                if msg.type == "ai":
                    last_message = msg.content

    return last_message if last_message else "No response from agent."
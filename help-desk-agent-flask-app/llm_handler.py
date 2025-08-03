# llm_handler.py
from agent import create_agent_with_memory

_react_agent = create_agent_with_memory()

def get_agent_response(prompt):
    config = {"configurable": {"thread_id": "tim-session-1"}}

    events = _react_agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        stream_mode="values",
        config=config,
    )

    last_message = None
    
    for event in events:
        if "messages" in event:
            # Multiple messages might appear, take the latest
            for msg in event["messages"]:
                if msg.type == "ai":
                    last_message = msg.content

    return last_message if last_message else "No response from agent."
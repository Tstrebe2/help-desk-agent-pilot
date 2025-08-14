import yaml
from pathlib import Path
from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import MessagesState
from tools.database import create_db_toolkit
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableBinding
from functools import partial
from tools.rag import create_rag_tool_from_runnable

# Nodes
def remove_old_messages(state: MessagesState) -> dict:
    """
    Remove old messages junk from the state.
    """
    messages_to_remove = []

    for message in state['messages']:
        if message.type == "tool" or (message.type == "ai" and message.tool_calls):
            messages_to_remove.append(RemoveMessage(message.id))
    return {"messages": messages_to_remove}

def assistant(state: MessagesState, 
              system_prompt: dict,
              dialect: str,
              top_k: int,
              llm_with_tools: RunnableBinding) -> dict:
    
    system_message = (system_prompt['type'], system_prompt['content'])

    messages_to_send = ChatPromptTemplate.from_messages([
        system_message,
        MessagesPlaceholder("history"),
    ]).format_messages(
        history=state["messages"], 
        dialect=dialect, 
        top_k=top_k,
    )

    messages = llm_with_tools.invoke(messages_to_send)
    return {"messages": messages}

def create_react_agent_with_tools():
    config_path = Path("../help-desk-agent-flask-app/configs/react_agent.yaml").resolve()
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    model_config = config['model_config']
    dialect = "SQLite"
    top_k = 5
    system_prompt = config['system_prompt']
    
    db_path = '../../datasets/help-desk-tickets/sqlite_db/help_desk_agent.sqlite3'
    llm = init_chat_model(**model_config)
    toolkit = create_db_toolkit(db_path, llm)
    rag_tool = create_rag_tool_from_runnable()
    tools = toolkit.get_tools() + [rag_tool]
    llm_with_tools = llm.bind_tools(tools)

    builder = StateGraph(MessagesState)
    builder.add_node("remove_old_messages", partial(remove_old_messages))
    builder.add_node(
        "assistant", 
        partial(
            assistant, 
            system_prompt=system_prompt, 
            dialect=dialect, 
            top_k=top_k, 
            llm_with_tools=llm_with_tools
        )
    )
    builder.add_node("tools", ToolNode(tools=tools))

    builder.add_edge(START, "remove_old_messages")
    builder.add_edge("remove_old_messages", "assistant")
    builder.add_conditional_edges(
        "assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile(checkpointer=MemorySaver())
    return react_graph
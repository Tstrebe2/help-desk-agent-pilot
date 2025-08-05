# ticket_citation_tool.py
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class TicketCitationToolArgsSchema(BaseModel):
    ticket_id: str = Field(
        description=(
            "The TicketID for the ticket you would like to obtain a hyperlink to for citation purposes."
        )
    )

@tool(args_schema=TicketCitationToolArgsSchema)
def ticket_citation_tool(ticket_id: str) -> str:
    """
    Tool to format a url reference to a ticket.
    """
    return f'<a href="/ticket/{ticket_id}">[{ticket_id}]</a>'
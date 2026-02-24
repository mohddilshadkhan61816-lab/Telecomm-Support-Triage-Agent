from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QueryRequest(BaseModel):
    customer_id: str = Field(..., example="CUST-12345")
    customer_name: str = Field(..., example="John Doe")
    query_text: str = Field(..., example="My internet is completely down and my business is losing money!")

class TicketResponse(BaseModel):
    ticket_id: str
    customer_id: str
    query_text: str
    category: str
    priority: str
    priority_score: int
    automated_response: str
    timestamp: datetime
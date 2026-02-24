import uuid
from datetime import datetime
from typing import List
from .models import TicketResponse

class TicketDatabase:
    def __init__(self):
        self.tickets: List[TicketResponse] = []

    def add_ticket(self, customer_id: str, query_text: str, triage_data: dict) -> TicketResponse:
        ticket = TicketResponse(
            ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            customer_id=customer_id,
            query_text=query_text,
            category=triage_data["category"],
            priority=triage_data["priority"],
            priority_score=triage_data["priority_score"],
            automated_response=triage_data["automated_response"],
            timestamp=datetime.now()
        )
        self.tickets.append(ticket)
        return ticket

    def get_all_tickets_sorted(self) -> List[TicketResponse]:
        # Sort by priority score (highest first), then by timestamp (oldest first)
        return sorted(self.tickets, key=lambda x: (-x.priority_score, x.timestamp))

db = TicketDatabase()
from fastapi import FastAPI, HTTPException
from .models import QueryRequest, TicketResponse
from .triage_engine import TriageEngine
from .database import db
from typing import List

app = FastAPI(
    title="Telecom Support Triage Agent",
    description="An API that automatically categorizes and prioritizes telecom support queries.",
    version="1.0.0"
)

# Initialize the engine
engine = TriageEngine()

@app.get("/", summary="Welcome Page")
async def root():
    return {
        "message": "Welcome to the Telecom Support Triage Agent API!",
        "status": "online",
        "documentation_url": "http://localhost:8000/docs"
    }

@app.post("/submit_query", response_model=TicketResponse, summary="Submit a new customer query")
async def submit_query(request: QueryRequest):
    """
    Accepts a customer query, analyzes it for category and urgency, 
    generates an auto-response, and creates a support ticket.
    """
    if not request.query_text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")

    # 1. Analyze the text
    triage_results = engine.analyze_query(request.query_text)
    
    # 2. Save to database
    ticket = db.add_ticket(
        customer_id=request.customer_id,
        query_text=request.query_text,
        triage_data=triage_results
    )
    
    return ticket

@app.get("/agent_dashboard", response_model=List[TicketResponse], summary="Get prioritized queue")
async def get_triage_queue():
    """
    Returns all active tickets, sorted with the most critical issues at the top 
    so human agents know exactly what to work on first.
    """
    return db.get_all_tickets_sorted()
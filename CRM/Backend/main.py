from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import database
import email_service

app = FastAPI(title="CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    customer_name: str
    email: str
    phone: Optional[str] = None
    service: Optional[str] = None
    message: Optional[str] = None

class StatusUpdate(BaseModel):
    status: str

@app.post("/webhook/meta")
async def meta_webhook(lead: Lead):
    # Insert via stored procedure
    database.call_stored_procedure("InsertMetaLead", (
        lead.customer_name,
        lead.email,
        lead.phone,
        lead.service,
        lead.message
    ))
    
    # Trigger Welcome Email (status New)
    email_service.trigger_status_email(lead.customer_name, lead.email, "New")
    
    return {"message": "Lead captured successfully"}

@app.get("/leads")
async def get_leads(status: str = "All"):
    results = database.call_stored_procedure("FetchLeadsByStatus", (status,))
    return results if results is not None else []

@app.put("/leads/{lead_id}/status")
async def update_lead_status(lead_id: int, update: StatusUpdate):
    # Get lead info first to trigger email
    lead_query = "SELECT customer_name, email FROM leads WHERE lead_id = %s"
    lead_info = database.execute_query(lead_query, (lead_id,), fetch=True)
    
    if not lead_info:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Update via stored procedure
    database.call_stored_procedure("UpdateLeadStatus", (lead_id, update.status))
    
    # Trigger appropriate email
    email_service.trigger_status_email(
        lead_info[0]['customer_name'], 
        lead_info[0]['email'], 
        update.status
    )
    
    return {"message": f"Status updated to {update.status}"}

@app.get("/notifications")
async def get_notifications():
    query = "SELECT * FROM notifications ORDER BY created_at DESC LIMIT 50"
    return database.execute_query(query, fetch=True) or []

@app.put("/notifications/{notif_id}/read")
async def mark_notification_read(notif_id: int):
    query = "UPDATE notifications SET is_read = TRUE WHERE notification_id = %s"
    database.execute_query(query, (notif_id,))
    return {"message": "Notification marked as read"}

@app.get("/stats")
async def get_dashboard_stats():
    query = "SELECT status, COUNT(*) as count FROM leads GROUP BY status"
    return database.execute_query(query, fetch=True) or []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

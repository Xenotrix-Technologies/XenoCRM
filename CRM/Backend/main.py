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

class EmailSend(BaseModel):
    to_email: str
    subject: str
    body: str

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

@app.get("/leads/{lead_id}")
async def get_lead(lead_id: int):
    lead = database.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

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

@app.get("/leads/{lead_id}/emails")
async def get_lead_emails(lead_id: int):
    emails = database.get_lead_emails(lead_id)
    return emails if emails else []

@app.post("/emails/sync")
async def sync_emails():
    # Trigger manual sync
    email_service.fetch_emails()
    return {"message": "Email sync triggered"}

@app.post("/emails/send")
async def send_custom_email(email_data: EmailSend):
    success = email_service.send_email(
        email_data.to_email,
        email_data.subject,
        email_data.body
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    return {"message": "Email sent successfully"}

import asyncio

@app.on_event("startup")
async def startup_event():
    # Run email fetcher in background
    async def periodic_fetch():
        while True:
            try:
                print("Fetching emails...")
                email_service.fetch_emails()
            except Exception as e:
                print(f"Error in background fetch: {e}")
            await asyncio.sleep(60) # Fetch every minute

    asyncio.create_task(periodic_fetch())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

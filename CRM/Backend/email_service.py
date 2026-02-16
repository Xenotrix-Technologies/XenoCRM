import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import database

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

import imaplib
import email
from email.header import decode_header
import datetime

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

def send_email(to_email, subject, body):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("Email configuration missing. Skipping email send.")
        print(f"To: {to_email}, Subject: {subject}, Body: {body}")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        # LOG EMAIL TO DB
        # Find lead_id for the recipient
        lead_query = "SELECT lead_id FROM leads WHERE email = %s"
        lead_result = database.execute_query(lead_query, (to_email,), fetch=True)
        if lead_result:
            lead_id = lead_result[0]['lead_id']
            database.log_email(lead_id, SMTP_USER, to_email, subject, body, 'Outbound')
            
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def trigger_status_email(customer_name, to_email, status):
    # Fetch template from DB
    query = "SELECT subject, body FROM email_templates WHERE status = %s"
    template = database.execute_query(query, (status,), fetch=True)
    
    if template:
        subject = template[0]['subject']
        body = template[0]['body'].replace("{name}", customer_name)
        return send_email(to_email, subject, body)
    
    print(f"No email template found for status: {status}")
    return False

# EMAIL FETCHING DISABLED - Leads now come from Google Forms
# Uncomment this function if you need to re-enable email-based lead capture
"""
def fetch_emails():
    if not SMTP_USER or not SMTP_PASSWORD:
        return
        
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(SMTP_USER, SMTP_PASSWORD)
        mail.select("inbox")
        
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        
        for e_id in email_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    from_email = email.utils.parseaddr(msg.get("From"))[1]
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                        
                    # MATCH TO LEAD
                    lead_query = "SELECT lead_id FROM leads WHERE email = %s"
                    lead_result = database.execute_query(lead_query, (from_email,), fetch=True)
                    
                    if lead_result:
                        lead_id = lead_result[0]['lead_id']
                        database.log_email(lead_id, from_email, SMTP_USER, subject, body, 'Inbound')
                        
                        # Create Notification
                        notif_msg = f"New email from {from_email}"
                        database.execute_query("INSERT INTO notifications (message, is_read) VALUES (%s, FALSE)", (notif_msg,))
                        
    except Exception as e:
        print(f"Error fetching emails: {e}")
"""


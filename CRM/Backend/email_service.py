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

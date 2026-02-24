import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_google_form_webhook():
    payload = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "company": "Test Co",
        "message": "Interested in CRM services",
        "service": "Web Development"
    }
    
    print("Testing Google Form Webhook (New Lead)...")
    try:
        response = requests.post(f"{BASE_URL}/webhook/google-forms", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_duplicate_lead():
    payload = {
        "name": "John Doe Duplicate",
        "email": "johndoe@example.com", # Same email
        "phone": "0987654321",
        "company": "Other Co",
        "message": "Still interested",
        "service": "Consulting"
    }
    
    print("\nTesting Duplicate Lead (Same Email)...")
    try:
        response = requests.post(f"{BASE_URL}/webhook/google-forms", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_google_form_webhook()
    test_duplicate_lead()

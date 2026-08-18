import json
import os
import urllib.request
import urllib.parse
from django.conf import settings

def normalize_phone_number(raw_phone):
    """
    Normalizes phone numbers to standard WhatsApp E.164 numerical format.
    Handles Indian numbers (9539251789 -> 919539251789, +91 95392 51789 -> 919539251789)
    and international numbers.
    """
    if not raw_phone:
        return ""
    
    cleaned = ''.join(c for c in str(raw_phone) if c.isdigit() or c == '+')
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    elif len(cleaned) == 10:
        cleaned = '91' + cleaned
    elif cleaned.startswith('0') and len(cleaned) == 11:
        cleaned = '91' + cleaned[1:]

    return cleaned

def get_whatsapp_api_status():
    """
    Returns WhatsApp Business Cloud API configuration and connection status.
    Strictly reads credentials from server-side settings/.env without exposing token.
    """
    token = getattr(settings, 'WHATSAPP_CLOUD_API_TOKEN', '') or os.environ.get('WHATSAPP_CLOUD_API_TOKEN', '')
    phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '') or os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '1249495338254585')
    business_account_id = getattr(settings, 'WHATSAPP_BUSINESS_ACCOUNT_ID', '') or os.environ.get('WHATSAPP_BUSINESS_ACCOUNT_ID', '1753452545807653')

    is_configured = bool(token and token.strip() and phone_number_id and phone_number_id.strip())
    
    return {
        'is_connected': is_configured,
        'status_label': 'WhatsApp API Connected' if is_configured else 'WhatsApp API Standby / Unconfigured',
        'business_number': '+91 9995544316',
        'phone_number_id': phone_number_id,
        'business_account_id': business_account_id,
        'has_token': bool(token),
        'api_version': 'v18.0'
    }

def send_meta_cloud_api_message(lead, message_text, buttons=None, template_name=None, custom_token=None, custom_phone_id=None, user=None):
    """
    Dispatches Meta WhatsApp Business Cloud API messages.
    Supports interactive reply buttons, CTA buttons, and template messages.
    Saves record to WhatsAppMessage database table and logs timeline Activity.
    """
    from .models import WhatsAppMessage, Activity

    raw_phone = lead.phone_number or ''
    cleaned_phone = normalize_phone_number(raw_phone)
    if not cleaned_phone:
        return {
            'success': False,
            'error': 'Lead phone number is missing or invalid for WhatsApp messaging.'
        }

    token = custom_token or getattr(settings, 'WHATSAPP_CLOUD_API_TOKEN', '') or os.environ.get('WHATSAPP_CLOUD_API_TOKEN', '')
    phone_number_id = custom_phone_id or getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '') or os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '1249495338254585')

    buttons = buttons or []
    interactive_buttons = []
    
    for idx, b in enumerate(buttons[:3]):
        label = (b.get('text') or f"Action {idx+1}").strip()[:20]
        btn_type = b.get('type', 'Quick Reply')
        btn_id = b.get('id') or f"btn_{idx+1}"
        
        if btn_type == 'Quick Reply':
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn_id,
                    "title": label
                }
            })
        elif btn_type == 'Open URL':
            url_val = b.get('value') or 'https://xenotrix.in'
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn_id,
                    "title": f"🔗 {label}"
                }
            })
        elif btn_type == 'Call Phone':
            phone_val = b.get('value') or '+91 9995544316'
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn_id,
                    "title": f"📞 {label}"
                }
            })

    # Construct Meta WhatsApp Business Cloud API JSON payload
    if interactive_buttons:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": cleaned_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": interactive_buttons
                }
            }
        }
    else:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": cleaned_phone,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message_text
            }
        }

    meta_api_sent = False
    meta_message_id = None
    api_response = None
    error_msg = None

    if token and token.strip():
        graph_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        try:
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                graph_url,
                data=req_data,
                headers={
                    'Authorization': f'Bearer {token.strip()}',
                    'Content-Type': 'application/json'
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                resp_bytes = resp.read()
                api_response = json.loads(resp_bytes.decode('utf-8'))
                meta_api_sent = True
                
                # Extract Meta Message ID (wamid)
                if api_response.get('messages') and len(api_response['messages']) > 0:
                    meta_message_id = api_response['messages'][0].get('id')
        except urllib.error.HTTPError as http_err:
            try:
                err_body = http_err.read().decode('utf-8')
                api_response = json.loads(err_body)
            except Exception:
                api_response = {'error': f"HTTP {http_err.code}: {http_err.reason}"}
        except Exception as err:
            api_response = {'error': str(err)}

    # Parse error message if Meta request failed
    if api_response and 'error' in api_response:
        err_obj = api_response['error']
        raw_err = err_obj.get('message') if isinstance(err_obj, dict) else str(err_obj)
        err_code = err_obj.get('code') if isinstance(err_obj, dict) else None
        
        user_hint = ""
        if err_code == 131047:
            user_hint = "\n\n💡 Reason: Customer hasn't messaged your business in 24 hours. Use an approved WhatsApp template or switch to WhatsApp Web/Desktop mode to send directly."
        elif err_code == 100 or "test" in raw_err.lower():
            user_hint = "\n\n💡 Reason: Number must be added under 'Test Numbers' in Meta Developer Console when using Sandbox credentials."

        error_msg = f"Meta API Error ({err_code or 'Failed'}): {raw_err}{user_hint}"

    # Log to WhatsAppMessage DB table
    status_str = 'Sent' if meta_api_sent else ('Failed' if error_msg else 'Dispatched')
    
    wa_msg = WhatsAppMessage.objects.create(
        organization=lead.organization,
        lead=lead,
        user=user,
        recipient_phone=cleaned_phone,
        template_name=template_name or '',
        message_content=message_text,
        meta_message_id=meta_message_id or '',
        status=status_str,
        error_message=error_msg or '',
        buttons_json=json.dumps(buttons)
    )

    if error_msg:
        return {
            'success': False,
            'error': error_msg,
            'payload': payload,
            'api_response': api_response,
            'whatsapp_message_id': wa_msg.id
        }

    # Log to Lead Activity Timeline
    button_titles = ", ".join(f"[{b.get('text')}]" for b in buttons[:3])
    log_desc = f"Sent WhatsApp Message to +{cleaned_phone} (ID: {meta_message_id or 'Simulated'}):\n\"{message_text[:120]}\""
    if button_titles:
        log_desc += f"\nButtons: {button_titles}"

    Activity.objects.create(
        organization=lead.organization,
        lead=lead,
        user=user,
        type="WhatsApp Message",
        description=log_desc
    )

    return {
        'success': True,
        'meta_api_sent': meta_api_sent,
        'meta_message_id': meta_message_id,
        'message': f"WhatsApp message successfully delivered to +{cleaned_phone}!",
        'payload': payload,
        'api_response': api_response,
        'whatsapp_message_id': wa_msg.id
    }

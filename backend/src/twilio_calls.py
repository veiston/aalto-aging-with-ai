"""
Twilio - Call Handling
Manages incoming/outgoing calls for elderly person

This module reads Twilio credentials from environment variables when available.
Do NOT commit real secrets. Use `.env` (local) and `.env.example` as a template.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_twilio_client(account_sid: str = None, auth_token: str = None):
    """Initialize Twilio client using env vars if not provided.

    Returns a `twilio.rest.Client` instance or `None` if credentials or library missing.
    """
    sid = account_sid or os.environ.get("TWILIO_ACCOUNT_SID")
    token = auth_token or os.environ.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        print("Twilio credentials not found in environment. Returning None.")
        return None

    try:
        from twilio.rest import Client
        return Client(sid, token)
    except Exception:
        print("Twilio library not available or failed to initialize. Install `twilio`.")
        return None

def receive_call(twilio_client, call_sid: str) -> dict:
    """
    Handle incoming call from elderly person
    Extract audio stream and metadata
    """
    # call = twilio_client.calls(call_sid).fetch()
    # return {
    #     "from": call.from_,
    #     "to": call.to,
    #     "status": call.status
    # }
    
    # Placeholder
    return {
        "from": "+358501234567",
        "to": "+358901234567",
        "status": "in-progress"
    }

def make_reminder_call(twilio_client, phone: str, message: str) -> str:
    """Make outgoing reminder call"""
    # call = twilio_client.calls.create(
    #     to=phone,
    #     from_="+358...",
    #     twiml=f'<Response><Say>{message}</Say></Response>'
    # )
    # return call.sid
    
    # Placeholder
    return "CALL_SID_12345"

def transfer_to_family(twilio_client, call_sid: str, family_phone: str):
    """Connect call to trusted family member"""
    # twilio_client.calls(call_sid).update(
    #     twiml=f'<Response><Dial>{family_phone}</Dial></Response>'
    # )
    pass

if __name__ == "__main__":
    # Test: call handling
    client = setup_twilio_client("ACCOUNT_SID", "AUTH_TOKEN")
    
    call = receive_call(client, "CALL_SID")
    print("Incoming call from:", call["from"])
    
    reminder_sid = make_reminder_call(client, "+358501234567", "Time for medication")
    print("Reminder call sent:", reminder_sid)
